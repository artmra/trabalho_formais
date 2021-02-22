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
    ERRO_1 = "O número de estados(linha 1) deve ser inteiro e maior que 0."
    ERRO_2 = "Não há estado inicial(linha 2)."
    ERRO_3 = "Não pode haver mais de um estado inicial(linha 2)."
    ERRO_4 = "Por questões de legibilidade, nomes de estados não podem ser símbolos do alfabeto.(linha "
    ERRO_5 = "Se presentes, as linhas de transição devem conter 3 elementos separados por \",\".(linha "
    ERRO_6_1 = "O símbolo \""
    ERRO_6_2 = "\" não pertence ao alfabeto definido.(linha "

    def __init__(self, meta_data, transitions):
        # lê o numero de estados
        try:
            self.n_states = int(meta_data[0])
            if self.n_states <= 0:
                raise Exception(self.ERRO_1)
        except ValueError:
            raise Exception(self.ERRO_1)
        # NOTA: Estados e símbolos sempre são salvos como strings
        # verifica se há apenas um estado inicial
        start_state = str(meta_data[1])
        if start_state == "":
            raise Exception(self.ERRO_2)
        if ',' in start_state:
            raise Exception(self.ERRO_3)
        self.start_state = start_state
        # cria a lista de estados de aceitação
        self.accept_states = [str(state) for state in meta_data[2].split(",")]
        # cria a lista contendo os símbolos do alfabeto
        self.alphabet = [str(symbol) for symbol in meta_data[3].split(",")]
        if self.start_state in self.alphabet:
            raise Exception(self.ERRO_4 + "2)")
        for state in self.accept_states:
            if state in self.alphabet:
                raise Exception(self.ERRO_4 + "3)")
        # se '&' 'pertencer' ao alfabeto, esse AF é um AFND
        self.is_afnd = "&" in self.alphabet
        # inicializa a tabela de transições com o estado inicial e os estados de aceitação
        self.transition_table = {self.start_state: dict()}
        for state in self.accept_states:
            self.transition_table.update({state: dict()})
        # adiciona as transições definidas a partir da linha 5 a tabela de transições
        for transition in transitions:
            try:
                origin_state, symbol, reachable_states = [str(t) for t in transition.split(",")]
            except:
                line = str(5 + transitions.index(transition))
                raise Exception(self.ERRO_5 + line + ")")
            if symbol not in self.alphabet:
                line = str(5 + transitions.index(transition))
                raise Exception(self.ERRO_6_1 + symbol + self.ERRO_6_2 + line + ")")
            # cria a linha de 'origin_state' na tabela, se não houver
            if origin_state not in self.transition_table.keys():
                self.transition_table.update({origin_state: dict()})
            # atualiza as transições de 'origin_state'
            state_transitions_by = self.transition_table[origin_state]
            reachable_states = [str(reachable_state) for reachable_state in reachable_states.split("-")]
            for state in reachable_states:
                if state in self.alphabet:
                    line = str(5 + transitions.index(transition))
                    raise Exception(self.ERRO_4 + line + ")")
            new_transition = {symbol: reachable_states}
            state_transitions_by.update(new_transition)
            self.is_afnd = self.is_afnd or len(state_transitions_by[symbol]) > 1
            # adiciona estados que ainda não pertencem a tabela de transição. Esse passo garante que eventuais estados
            # mortos sejam adicionados a tabela, o que pode ajudar na implementação futura da minimização de AF.
            for state in reachable_states:
                if state not in self.transition_table.keys():
                    self.transition_table.update({state: dict()})

        self.states = list(self.transition_table.keys())
        # atualiza o número de estados. Não reclama se for diferente.
        self.n_states = len(self.states)

    def __str__(self):
        return f"Número de estados: {self.n_states}\n" \
               f"Estado Inicial: {self.start_state}\n" \
               f"Estados de aceitação: {self.accept_states}\n" \
               f"Tabela de transições: {self.transition_table}\n" \
               f"É AFND: { self.is_afnd}\n" \
               f"Nomes dos estados: {self.states}"

    def write_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(self.string_in_file_format())

    def string_in_file_format(self):
        transition_table_as_string = ""
        # Formata as entradas do dicionário para o formato do arquivo .jff
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
