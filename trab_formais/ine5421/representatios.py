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
        return f"{self.n_states}\n" \
               f"{self.start_state}\n" \
               f"{self.accept_states}\n" \
               f"{self.transition_table}\n" \
               f"is AFND: {self.is_afnd}\n" \
               f"states: {self.states}"

    def write_to_file(self, filename):
        transition_table_as_string = ""
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

        with open(filename, "w") as file:
            file.write(f"{self.n_states}\n"
                       f"{self.start_state}\n"
                       f"{','.join(self.accept_states)}\n"
                       f"{','.join(self.alphabet)}\n"
                       f"{transition_table_as_string}")
