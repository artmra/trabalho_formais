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