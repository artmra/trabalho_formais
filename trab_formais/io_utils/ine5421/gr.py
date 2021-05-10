from .grammar import Grammar

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
        example:
        ['S', 'S,A', 'a,b,&'] -> meta_data
        ['S->aA|a|&', 'A->bA|a'] -> productions

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

        self.symbols = self.terminals + self.non_terminals

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

    def first(string, gr, productions_dict):
        first_ = set()

        if string in gr.non_terminals:
            alternatives = productions_dict[string]

            for alternative in alternatives:
                first_2 = GR.first(alternative, gr, productions_dict)
                first_ = first_ | first_2

        elif string in gr.terminals:
            first_ = {string}

        elif string == '&':
            first_ = {'&'}

        else:
            first_2 = GR.first(string[0], gr, productions_dict)
            if '&' in first_2:
                i = 1
                while '&' in first_2:
                    first_ = first_ | (first_2 - {'&'})
                    if string[i:] in gr.terminals:
                        first_ = first_ | {string[i:]}
                        break
                    elif string[i:] == '':
                        first_ = first_ | {'&'}
                        break
                    first_2 = GR.first(string[i:], gr, productions_dict)
                    first_ = first_ | first_2 - {'&'}
                    i += 1
            else:
                first_ = first_ | first_2

        return first_

    def follow(nT, gr, productions_dict):
        # print("inside follow({})".format(nT))
        follow_ = set()
        # print("FOLLOW", FOLLOW)
        prods = productions_dict.items()
        if nT == gr.start_symbol:
            follow_ = follow_ | {'$'}
        for nt, rhs in prods:
            # print("nt to rhs", nt,rhs)
            for alt in rhs:
                for char in alt:
                    if char == nT:
                        following_str = alt[alt.index(char) + 1:]
                        if following_str == '':
                            if nt == nT:
                                continue
                            else:
                                follow_ = follow_ | GR.follow(nt, gr, productions_dict)
                        else:
                            follow_2 = GR.first(following_str, gr, productions_dict)
                            if '&' in follow_2:
                                follow_ = follow_ | follow_2 - {'&'}
                                follow_ = follow_ | GR.follow(nt, gr, productions_dict)
                            else:
                                follow_ = follow_ | follow_2
        # print("returning for follow({})".format(nT),follow_)
        return follow_

    def get_firsts_follows(self):
        terminals = self.terminals
        non_terminals = self.non_terminals
        starting_symbol = self.start_symbol

        productions = self.productions

        productions_dict = {}

        for nT in non_terminals:
            productions_dict[nT] = []

        for p in productions:
            for s in productions[p]:
                productions_dict[p].append(s)

        FIRST = {}
        FOLLOW = {}

        for non_terminal in non_terminals:
            FIRST[non_terminal] = set()

        for non_terminal in non_terminals:
            FOLLOW[non_terminal] = set()

        for non_terminal in non_terminals:
            FIRST[non_terminal] = FIRST[non_terminal] | GR.first(non_terminal, self, productions_dict)

        FOLLOW[starting_symbol] = FOLLOW[starting_symbol] | {'$'}
        for non_terminal in non_terminals:
            FOLLOW[non_terminal] = FOLLOW[non_terminal] | GR.follow(non_terminal, self, productions_dict)

        return FIRST, FOLLOW