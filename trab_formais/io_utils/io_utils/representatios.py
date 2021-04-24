from django.templatetags.static import static


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
                # TODO: checar se todas os símbolos fazem parte do conjunto de terminais ou não terminais
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


class GLC:
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
        # # verifica se há apenas um símbolo inicial
        # if str(meta_data[0]) == "" or len([str(nonTerminal) for nonTerminal in meta_data[0].split(",")]) > 1:
        #     raise Exception(self.ERRO_1)
        # self.start_symbol = str(meta_data[0])
        # # verifica se há pelo menos um símbolo
        # self.non_terminals = [str(symbol) for symbol in meta_data[1].split(",")]
        # if self.start_symbol not in self.non_terminals:
        #     raise Exception(self.ERRO_2_1 + self.start_symbol + self.ERRO_2_2)
        # # verifica se nenhum dos símbolos não terminais pertence ao conjunto de terminais
        # self.terminals = [str(symbol) for symbol in meta_data[2].split(",")]
        # for symbol in self.non_terminals:
        #     if symbol in self.terminals:
        #         raise Exception(self.ERRO_3_1 + symbol + self.ERRO_3_2)
        # # cria as produções
        # self.productions = dict()
        # for production in productions:
        #     try:
        #         head, body = [str(p) for p in production.split("->")]
        #         if head == "":
        #             line = str(4 + productions.index(production))
        #             raise Exception(self.ERRO_5 + line + ")")
        #         # TODO: checar se todas os símbolos fazem parte do conjunto de terminais ou não terminais
        #     except:
        #         line = str(4 + productions.index(production))
        #         raise Exception(self.ERRO_4 + line + ")")
        #     # TODO: implementar a detecção de encolhimento de sentença
        #     body = [str(b) for b in body.split("|")]
        #     if len(body) < 1 or body[0] == "":
        #         line = str(4 + productions.index(production))
        #         raise Exception(self.ERRO_6 + line + ")")
        #     if head in self.productions.keys():
        #         line = str(4 + productions.index(production))
        #         raise Exception(self.ERRO_7 + line + ")")
        #     # adiciona essa regra de produção ao dicionário de produções
        #     self.productions.update({head: body})
        # self.production_heads = list(self.productions.keys())

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

    def eliminate_left_recursion(self, grammar):
        # https: // www.youtube.com / watch?v = dWmFd16GJEA

        resulting_grammar = str()

        header = str()
        heads = list()

        for line in grammar.splitlines():
            if '->' in line:
                symbol = line[0]
                line = line.replace(' ', '')
                productions = line.split('->')[1].split('|')
                left_recursions = [p for p in productions if p[0] == symbol]
                non_left_recursions = [p for p in productions if p[0] != symbol]

                d = {"symbol": symbol,
                     "productions": productions,
                     "left_recursions": left_recursions,
                     "non_left_recursions": non_left_recursions}

            heads.append(d)

        heads = self.eliminate_direct_recursion(heads, grammar)
        # heads = self.eliminate_indirect_recursions(heads)
        return heads

    @staticmethod
    def eliminate_direct_recursion(heads, grammar):
        for head in heads:
            new_productions = list()
            if head['left_recursions']:
                # print([(nlr + f'{head["symbol"]}\'') for nlr in head['non_left_recursions']])

                new_productions.append([(nlr + f'{head["symbol"]}\'') for nlr in head['non_left_recursions']])
                new_productions.append([(lr[1:] + f'{head["symbol"]}\'') for lr in head['left_recursions']])
                new_productions[1].append('&')

                print(new_productions[0])
                print(new_productions[1])

                head['productions'] = new_productions[0]
                head['left_recursions'] = list()
                head['non_left_recursions'] = new_productions[0]

                new_head = {"symbol": f'{head}\'',
                            "productions": new_productions[1],
                            "left_recursions": list(),
                            "non_left_recursions": new_productions[1]}
                heads.append(new_head)

        return heads

    @staticmethod
    def eliminate_indirect_recursions(heads):
        return heads


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
            Escreve o objeto em um arquivo de nome 'filename'
        string_in_file_format()
            Retorna o objeto codificado em uma string seguindo o formato de arquivo '.jff'
        get_states_as_viz_nodes()
            Retorna os estados em uma lista de dicionários({id, label})
        get_transitions_as_viz_edges()
            Retorna as transições em uma lista de dicionários({from, to, label})
        determinize()
            Determiniza o AF caso o mesmo seja um AFND
        determinize_with_epsilon()
            Determiniza o AF se o mesmo for um AFND com &-transições
        determinize_without_epsilon()
            Determiniza o AF se o mesmo for um AFND sem &-transições
        define_new_states()
            Define novos estados para o AF se baseando em uma lista passada como parâmetro.
        calculate_epsilon_set()
            Retorna um dicionário de lista que simula a função &-fecho para cada estado do AF


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
            reachable_states = sorted([str(reachable_state) for reachable_state in reachable_states.split("-")])
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
               f"É AFND: {self.is_afnd}\n" \
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

    def get_states_as_vis_nodes(self):
        """
        :return: list
            lista de dicionários contendo os dados necessários para criar nodes no viz.
        """
        nodes = list()

        for state in self.states:
            color_options = {'border': '#004582',
                             'background': '#91D4ED'}
            state_label = state

            if state == self.start_state:
                state_label = '->' + state
                color_options = {'border': '#F25D00',
                                 'background': '#EEB679'}

            if state in self.accept_states:
                state_label = '*' + state
                color_options = {'border': '#008239',
                                 'background': '#91EDAC'}

            nodes.append({'id': self.states.index(state),
                          'label': state_label,
                          'color': color_options})
        return nodes

    def get_transitions_as_vis_edges(self):
        """
        :return: list
            lista de dicionários contendo os dados necessários para criar transições no viz.
        """
        edges_control = list()
        edges = list()
        for init_state, transitions in self.transition_table.items():
            for symbol, reachable_states in transitions.items():
                for index, state in enumerate(reachable_states):
                    factor = 0
                    if index == 0:
                        factor = 0
                    elif index % 2 == 0:
                        factor = index * 0.2
                    else:
                        factor = index * 0.2 * (-1)

                    have_ocurred = edges_control.count([state, init_state])

                    if have_ocurred > 0:
                        factor = factor + have_ocurred * 0.2

                    edges_control.append([init_state, state])

                    edges.append({
                        'from': init_state,
                        'to': state,
                        'label': symbol,
                        'smooth': {'type': 'curvedCCW', 'roundness': factor},
                        'color': '#6b705c'
                    })
        return edges

    def determinize(self):
        """
        :return:
        """
        if not self.is_afnd:
            pass
        if '&' in self.alphabet:
            self.determinize_with_epsilon()
        else:
            self.determinize_without_epsilon()

    def determinize_with_epsilon(self):
        """
        :return:
        """
        # calcula o epsilon fecho
        epsilon_set = self.calculate_epsilon_set()
        states_to_define = [epsilon_set[self.start_state]]
        # calcula as transicoes para cada estado em states_to_define, enquanto houver
        new_accept_states, new_transition_table = self.define_new_states(states_to_define, dict(), epsilon_set)
        # remove o '&' do alfabeto
        self.alphabet.remove('&')
        # mudar o conjunto de estados de aceitação
        self.accept_states = new_accept_states
        # mudar o estado inicial
        self.start_state = get_name(epsilon_set[self.start_state])
        # mudar a tabela de transicoes
        self.transition_table = new_transition_table
        # atualizar a lista de statos
        self.states = list(self.transition_table.keys())
        # atualizar o numero de estados
        self.n_states = len(self.states)

    def determinize_without_epsilon(self):
        """
        :return:
        """
        states_to_define = []
        # primeiro percorre para obter novos estados e os adiciona em states_to_define
        for transitions in self.transition_table.values():
            new_states = [state for state in transitions.values() if len(state) > 1 and state not in states_to_define]
            if new_states:
                states_to_define.extend(new_states)
        # define todos os estados em states_to_define, e adiciona novos a lista caso necessário
        new_accept_states, _ = self.define_new_states(states_to_define, self.transition_table, dict())
        # atualiza refrencias a nomes antigos no dicionario
        for origin_state, transitions in self.transition_table.items():
            for symbol, destiny_states in transitions.items():
                if len(destiny_states) > 1:
                    self.transition_table[origin_state][symbol] = [get_name(destiny_states)]
        # atualizar a lista de estados de aceitação
        self.accept_states.extend(new_accept_states)
        # atualizar a lista de estados
        self.states = list(self.transition_table.keys())
        # atualizar o numero de estados
        self.n_states = len(self.states)

    def define_new_states(self, states_to_define, transition_table, epsilon_set):
        """
        :return: list
            lista contendo, na seguinte ordem: [0]conjunto de novos estados de aceitação; [1]nova tabela de transições.
        """
        new_accept_states = list()
        while states_to_define:
            new_origin_state = sorted(states_to_define.pop(0))
            new_origin_state_name = get_name(new_origin_state)
            is_accept_state = False
            transitions = dict()
            for symbol in self.alphabet:
                new_state = list()
                for state in new_origin_state:
                    # checa se new_origin_state é um estado de aceitação
                    if state in self.accept_states and not is_accept_state:
                        is_accept_state = True
                    if symbol in self.transition_table[state].keys():
                        # adiciona o epsilon fecho de cada estado se for AFND com &-transições
                        if '&' in self.alphabet:
                            for s in self.transition_table[state][symbol]:
                                # eventualmente pode acabar adicionando estados repetidos
                                new_state.extend(epsilon_set[s])
                            continue
                        # eventualmente pode acabar adicionando estados repetidos
                        new_state.extend(self.transition_table[state][symbol])
                if new_state:
                    # retira elementos repetidos e ordena a lista que contém os estados que compoe o novo estado
                    new_state = sorted(list(set(new_state)))
                    new_state_name = get_name(new_state)
                    # checar se new_state já foi definido; se não, adicioná-lo a lista para definição
                    if new_state_name not in transition_table.keys() and new_state not in states_to_define:
                        states_to_define.append(new_state)
                    # adicionar entrada a transitions
                    transitions.update({symbol: [new_state_name]})
            if is_accept_state and new_origin_state_name not in new_accept_states:
                new_accept_states.append(new_origin_state_name)
            # adicionar a nova linha à nova tabela de transição
            transition_table.update({new_origin_state_name: transitions})
        return [new_accept_states, transition_table]

    def calculate_epsilon_set(self) -> dict:
        """
        :return: dict
            dicionário de listas que simula a funcao &-fecho dos estados do AF.
        """
        epsilon_set = dict()
        for origin_state, transitions in self.transition_table.items():
            # adiciona o proprio estado ao seu &-fecho
            reachable_states = [origin_state]
            if '&' in transitions.keys():
                states_to_check = transitions['&']
                # checa todos os estados alcancaveis a partir de origin_state enquanto ouver estado em states_to_check
                while states_to_check:
                    s = states_to_check.pop(0)
                    reachable_states.append(s)
                    if '&' in self.transition_table[s].keys():
                        for state in self.transition_table[s]['&']:
                            if state not in states_to_check and state not in reachable_states:
                                states_to_check.append(state)
            epsilon_set.update({origin_state: reachable_states})
        return epsilon_set


class ER:
    """
    Classe usada para representar uma Expressão Regular
    """

    ERRO_1 = "Formato de expressão incorreto"

    def __init__(self, expression):
        self.expression = expression

        # verifica se as aberturas e fechamentos de parênteses estão ok
        if not (self.is_parenthesis_ok() and self.is_symbols_ok()):
            raise Exception(self.ERRO_1)

    def is_parenthesis_ok(self):
        """
        :return: Bool
            True: caso os parêntesis estejam organizados de maneira adequada
            False: em caso de erro na organização dos parêntesis
        """
        while True:
            stack = []

            for c in self.expression:
                if c == "(":
                    stack.append(c)
                elif c == ")":
                    if not stack:
                        stack.append(c)
                        continue
                    else:
                        stack.pop()

            if not stack:
                return True
            return False

    def is_symbols_ok(self):
        """
        :return: Bool
            True: se não houver organização incorreta de símbolos
            False: se houver organização incorreta
        """
        non_accepted_order = ['||', '|*', '*+', '+*', '+?', '?+']
        for sym in non_accepted_order:
            if sym in self.expression:
                return False
        return True

    def write_to_file(self, filename):
        """
        :param filename: str
            nome do arquivo no qual a er deve ser escrita.
        :return:
        """
        with open(filename, "w") as file:
            print(self.expression, file=file)

    @staticmethod
    def concatenate(expression1, expression2):
        """
        :params expression1, expression2: str
            expressões a serem concatenadas.
        :return: str
            resultado da concatenação das expressões.
        """
        return expression1 + expression2

    @staticmethod
    def union(expression1, expression2):
        """
        :params expression1, expression2: str
            expressões a serem unidas.
        :return: str
            resultado da união das expressões.
        """
        return '(' + expression1 + ')|(' + expression2 + ')'

    @staticmethod
    def star(expression):
        """
        :params expression: str
            expressão a ser convertida para fecho.
        :return: str
            fecho da expressão de entrada.
        """
        return '(' + expression + ')*'


def get_name(states_list):
    """
    :return: string
        string contendo um novo nome para um conjunto de estados.
    """
    if len(states_list) > 1:
        return '{' + ';'.join(states_list) + '}'
    return states_list[0]
