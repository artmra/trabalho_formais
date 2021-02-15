class GR:
    def __init__(self, meta_data, productions):
        # checks the presence of an start_symbol
        if str(meta_data[0]) == "":
            raise Exception("There is no start symbol.")
        self.start_symbol = str(meta_data[0])
        self.non_terminals = [str(symbol) for symbol in meta_data[1].split(",")]
        # checks if the start_symbol belongs to the non_terminals
        if self.start_symbol not in self.non_terminals:
            raise Exception("Start symbol doesn't belong to non teminals.")
        self.terminals = [str(symbol) for symbol in meta_data[2].split(",")]
        # create the productions
        self.productions = dict()
        for production in productions:
            head, body = [str(p) for p in production.split("->")]
            body = [str(b) for b in body.split("|")]
            if head in self.productions.keys():
                raise Exception("Must be only one line for each 'production head'.")
            self.productions.update({head: body})
        self.production_heads = list(self.productions.keys())

    def __str__(self):
        return f"Start symbol: {self.start_symbol}\n" \
               f"Non terminals: {self.non_terminals}\n" \
               f"Terminals: {self.terminals}\n" \
               f"Productions: {self.productions}\n" \
               f"Production heads: {self.production_heads}"

    def write_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(self.string_in_file_format())

    def string_in_file_format(self):
        productions = ""
        # format the production dict entries to the file format
        for head, body in self.productions.items():
            body_str = " | ".join(body)
            productions = productions + f"{head} -> {body_str}\n"
        return f"{self.start_symbol}\n" \
               f"{','.join(self.non_terminals)}\n" \
               f"{','.join(self.terminals)}\n" \
               f"{productions}"


class AF:
    def __init__(self, meta_data, transitions):
        self.n_states = int(meta_data[0])
        # always store state and symbols as string
        if str(meta_data[1]) == "":
            raise Exception("There is no start state.")
        self.start_state = str(meta_data[1])
        self.transition_table = {self.start_state: dict()}
        self.accept_states = [str(state) for state in meta_data[2].split(",")]
        self.alphabet = [str(symbol) for symbol in meta_data[3].split(",")]
        # if '&' is in alphabet, this AF is an AFND
        self.is_afnd = "&" in self.alphabet
        for transition in transitions:
            origin_state, symbol, reachable_states = [str(t) for t in transition.split(",")]
            if symbol not in self.alphabet:
                raise Exception(f"The transition by '{symbol}' isn't possible because the symbol doesn't "
                                f"belong to AF's alphabet.")
            # create origin_state's 'line' in the transition_table
            if origin_state not in self.transition_table.keys():
                self.transition_table.update({origin_state: dict()})
            # update the transition of origin_state's 'line'
            state_transitions_by = self.transition_table[origin_state]
            reachable_states = [str(reachable_state) for reachable_state in reachable_states.split("-")]
            new_transition = {symbol: reachable_states}
            state_transitions_by.update(new_transition)
            self.is_afnd = self.is_afnd or len(state_transitions_by[symbol]) > 1
            # adds eventual dead states in the transition table. May help in automaton minimization algorithm
            # implementation in the future
            for state in reachable_states:
                if state not in self.transition_table.keys():
                    self.transition_table.update({state: dict()})

        self.states = list(self.transition_table.keys())
        if self.n_states != len(self.states):
            raise Exception("Number of states value different from the real number of lines.")

    def __str__(self):
        return f"Number of states: {self.n_states}\n" \
               f"Initial state: {self.start_state}\n" \
               f"Accept states: {self.accept_states}\n" \
               f"Transition table: {self.transition_table}\n" \
               f"Is AFND: {self.is_afnd}\n" \
               f"State names: {self.states}"

    def write_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(self.string_in_file_format())

    def string_in_file_format(self):
        transition_table_as_string = ""
        # format the transition_table dict entries to the file format
        for origin_state, transitions in self.transition_table.items():
            if bool(transitions):
                for symbol, destiny_states in transitions.items():
                    destiny_states_as_string = destiny_states[0]
                    if len(destiny_states) > 1:
                        for i in range(1, len(destiny_states)):
                            destiny_state = destiny_states[i]
                            destiny_states_as_string = destiny_states_as_string + f"-{destiny_state}"
                    transition_table_as_string = transition_table_as_string + \
                                                 f"{origin_state},{symbol},{destiny_states_as_string}\n"
        return f"{self.n_states}\n" \
               f"{self.start_state}\n" \
               f"{','.join(self.accept_states)}\n" \
               f"{','.join(self.alphabet)}\n" \
               f"{transition_table_as_string}"

