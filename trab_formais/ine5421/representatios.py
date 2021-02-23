class GR:
    """
    Classe usada para representar uma Gramática Regular

    Attributes
    ----------
    start_symbol: str
        Símbolo inicial.
    non_terminals: list
        Lista contendo os símbolos não terminais da gramática.
    terminals: list
        Lista contendo os símbolos terminais da gramática.
    productions: dict
        Dicionário de listas, no qual cada chave é uma sentença válida da GR e lista associada o corpo da produção.
    production_heads: list
        Lista contendo todas as chaves de 'productions'.

    Methods
    -------
    write_to_file(str=filename)
        Escreve o objeto em um arquivo de nome 'filename'.
    string_in_file_format()
        Retorna o objeto codificado em uma string seguindo o formato de arquivo '.jff'.


    """
    ERRO_1 = "Deve haver apenas um símbolo inicial.(linha 1)"
    ERRO_2_1 = "O símbolo inicial \""
    ERRO_2_2 = "\" não pertence ao conjunto de não terminais.(linha 2)"
    ERRO_3_1 = "O símbolo \""
    ERRO_3_2 = "\" não pode pertencer aos conjuntos de terminais e não-terminais simultaneamente.(linhas 2 e 3)"
    ERRO_4 = "Todas as produções devem separar a cabeça e corpo da produção com \"->\".(linha "
    # TODO: talvez esse caso nunca ocorra
    ERRO_5 = "As cabeças de produção não podem ser nulas.(linha "
    ERRO_6 = "Não pode haver encolhimento da sentença.(linha "
    ERRO_7 = "Todas as produções de uma \"cabeça de produção\" devem ser definidas em apenas uma linha. (linha "

    def __init__(self, meta_data, productions):
        """
        :param meta_data: list
            lista contendo, NA SEGUINTE ORDEM: símbolo inicial, símbolos não terminais, símbolos terminais.
        :param productions: list
            lista contendo as regras de produção da GR.
        :raise Exception:
            erro referente a falha no processo de leitura das informações da GR
        """
        # verifica se há apenas um símbolo inicial
        if str(meta_data[0]) == "" or len([str(nonTerminal) for nonTerminal in meta_data[0].split(",")]) > 1:
            raise Exception(self.ERRO_1)
        self.start_symbol = str(meta_data[0])
        # verifica se há pelo menos um símbolo
        self.non_terminals = [str(symbol) for symbol in meta_data[1].split(",")]
        if self.start_symbol not in self.non_terminals:
            raise Exception(self.ERRO_2_1 + self.start_symbol + self.ERRO_2_2)
        # verifica se nenhum dos símbolos não terminais pertence ao conjunto de terminais
        self.terminals = [str(symbol) for symbol in meta_data[2].split(",")]
        for symbol in self.non_terminals:
            if symbol in self.terminals:
                raise Exception(self.ERRO_3_1 + symbol + self.ERRO_3_2)
        # cria as produções
        self.productions = dict()
        for production in productions:
            try:
                head, body = [str(p) for p in production.split("->")]
                if head == "":
                    line = str(4 + productions.index(production))
                    raise Exception(self.ERRO_5 + line + ")")
            except:
                line = str(4 + productions.index(production))
                raise Exception(self.ERRO_4 + line + ")")
            # TODO: implementar a detecção de encolhimento de sentença
            body = [str(b) for b in body.split("|")]
            if len(body) < 1 or body[0] == "":
                line = str(4 + productions.index(production))
                raise Exception(self.ERRO_6 + line + ")")
            if head in self.productions.keys():
                line = str(4 + productions.index(production))
                raise Exception(self.ERRO_7 + line + ")")
            # adiciona essa regra de produção ao dicionário de produções
            self.productions.update({head: body})
        self.production_heads = list(self.productions.keys())

    def __str__(self):
        """
        :return: str com a representação dos dados do objeto; NÃO segue o padrão dos arquivos '.jff'.
        """
        return f"Símbolo inicial: {self.start_symbol}\n" \
               f"Não terminais: {self.non_terminals}\n" \
               f"Terminais: {self.terminals}\n" \
               f"Produções: {self.productions}\n" \
               f"Cabeças de produção: {self.production_heads}"

    def write_to_file(self, filename):
        """
        :param filename: str
            nome do arquivo no qual a gr deve ser escrita.
        :return:
        """
        with open(filename, "w") as file:
            file.write(self.string_in_file_format())

    def string_in_file_format(self):
        """
        :return: str
            string representando o formato a GR seguindo o formato dos arquivos '.jff'.
        """
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
    """
        Classe usada para representar um Autômato Finito

        Attributes
        ----------
        n_states: int
            Número de estados.
        start_state: str
            Estado inicial.
        accept_states: list
            Lista contendo os estados de aceitação.
        alphabet: list
            Lista contendo os símbolos do alfabeto.
        transition_table: dict
            Dicionário de dicionários, no qual cada par chave-valor emula uma linha na tabela de transições.
        is_AFND: bool
            Diz se o AF é não determinístico.
        states: list
            Lista contendo os nomes de todos os estados do AF.

        Methods
        -------
        write_to_file(str=filename)
            Escreve o objeto em um arquivo de nome 'filename'.
        string_in_file_format()
            Retorna o objeto codificado em uma string seguindo o formato de arquivo '.jff'.


        """
    ERRO_1 = "O número de estados deve ser inteiro e maior que 0.(linha 1)"
    ERRO_2 = "Não há estado inicial.(linha 2)"
    ERRO_3 = "Não pode haver mais de um estado inicial.(linha 2)"
    ERRO_4 = "Por questões de legibilidade, nomes de estados não podem ser símbolos do alfabeto.(linha "
    ERRO_5 = "Se presentes, as linhas de transição devem conter 3 elementos separados por \",\".(linha "
    ERRO_6_1 = "O símbolo \""
    ERRO_6_2 = "\" não pertence ao alfabeto definido.(linha "

    def __init__(self, meta_data, transitions):
        """
        :param meta_data: list
            lista contendo, NA SEGUINTE ORDEM: número de estados, estado inicial, estados de aceitação, alfabeto.
        :param transitions: list
            tabela de transição.
        :raise Exception:
            erro referente a falha no processo de leitura das informações do AF
        """
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
        """
        :return: str com a representação dos dados do objeto; NÃO segue o padrão dos arquivos '.jff'.
        """
        return f"Número de estados: {self.n_states}\n" \
               f"Estado Inicial: {self.start_state}\n" \
               f"Estados de aceitação: {self.accept_states}\n" \
               f"Tabela de transições: {self.transition_table}\n" \
               f"É AFND: { self.is_afnd}\n" \
               f"Nomes dos estados: {self.states}"

    def write_to_file(self, filename):
        """
        :param filename: str
            nome do arquivo no qual o af deve ser escrito.
        :return:
        """
        with open(filename, "w") as file:
            file.write(self.string_in_file_format())

    def string_in_file_format(self):
        """
        :return: str
            string representando o formato o AF seguindo o formato dos arquivos '.jff'.
        """
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
