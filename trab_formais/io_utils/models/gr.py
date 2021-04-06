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
