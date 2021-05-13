"""
Grammar class used only in the parser. This productions differs in the construction from the other on the aspects:

this is uses sets instead of lists. It makes ir more complicated to understand, but easier to
execute tha algorithm because of the naturality of sets.
"""

class ParserGrammar:
    def __init__(self, grammar_str):
        self.grammar_str = '\n'.join(filter(None, grammar_str.splitlines()))
        self.productions = {}
        self.start = None
        self.terminals = set()
        self.non_terminals = set()

        for production in list(filter(None, grammar_str.splitlines())):
            head, _, bodies = production.partition(' -> ')

            if not head.isupper():
                raise Exception(
                    f'\'{head} -> {bodies}\': Head \'{head}\' is not capitalized to be treated as a nonterminal.')

            if not self.start:
                self.start = head

            self.productions.setdefault(head, set())
            self.non_terminals.add(head)
            bodies = {tuple(body.split()) for body in ' '.join(bodies.split()).split('|')}

            for body in bodies:
                if '&' in body and body != ('&',):
                    raise Exception(f'\'{head} -> {" ".join(body)}\': Null symbol \'&\' is not allowed here.')

                self.productions[head].add(body)

                for symbol in body:
                    if not symbol.isupper() and symbol != '&':
                        self.terminals.add(symbol)
                    elif symbol.isupper():
                        self.non_terminals.add(symbol)

        self.symbols = self.terminals | self.non_terminals

    def __str__(self):
        """
                :return: str com a representação dos dados do objeto; NÃO segue o padrão dos arquivos '.jff'.
                """
        return f"Símbolo inicial: {self.start}\n" \
               f"Não terminais: {self.non_terminals}\n" \
               f"Terminais: {self.terminals}\n" \
               f"Produções: {self.productions}\n"