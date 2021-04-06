class ER:
    """
    Classe usada para representar uma Expressão Regular
    """

    ERRO_1 = "Parêntensis ordenados de maneira incorreta"
    ERRO_2 = "Símbolo de final de expressão incorreto"
    ERRO_3 = "Sequência de símbolos incorreta ('||', '|*', '*+', '+*', '+?', '?+')"

    def __init__(self, expression):
        self.expression = expression
        self.alphabet = set(c for c in expression if c not in '#|*?()&')

        # verifica se as aberturas e fechamentos de parênteses estão ok
        try:
            self.is_parenthesis_ok()
            self.is_symbols_ok()
        except Exception as e:
            print(e)

    def is_parenthesis_ok(self):
        """
        :raise: ERRO_1 em caso de organização incorreta nos parêntesis
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

            if stack:
                raise Exception(self.ERRO_1)

    def is_symbols_ok(self):
        """
        :raise:
            ERRO_2 quando símbolo de fim de expressão não for '#'
            ERRO_3 quando houver sequência de símbolos incorreta na expressão
        """
        # primeiro confirma se o último caractere é '#'
        if self.expression.strip()[-1] not in '#':
            raise Exception(self.ERRO_2)
        non_accepted_order = ['||', '|*', '*+', '+*', '+?', '?+', '()']
        for sym in non_accepted_order:
            if sym in self.expression:
                raise Exception(self.ERRO_3)

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
        return '(' + expression1 + ')(' + expression2 + ')'

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

    def convert_to_af(self):
        """
        :return: AF
            AFD equivalente a esse ER.
        """
        import tree
        # cria uma árvore e realiza a conversão do ER para AFD
        t = tree.Tree(self.alphabet)
        af = t.make_tree(self.expression)
        # automato pronto
        return af