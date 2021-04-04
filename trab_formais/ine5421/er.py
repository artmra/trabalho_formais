class ER:
    """
    Classe usada para representar uma Expressão Regular

    Attributes
    ----------
    expression: str
        Expressão regular

    Methods
    -------
    is_parenthesis_ok()
        Retorna true caso os parêntesis estejam organizados de forma correta e false caso contrário
    is_symbols_ok()
        Retorna true caso a disposição dos símbolos faça sentido e false caso contrário
    write_to_file(str=filename)
        Método para escrever a ER em um arquivo de path 'filename'
    concatenate(str=expression1, str=expression2)
        Retorna a concatenação dos parâmetros 'expression1' e 'expression2'
    union(str=expression1, str=expression2)
        Retorna a união dos parâmetros 'expression1' e 'expression2'
    star(expression)
        Retorna o fecho da ER de entrada 'expression'
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
