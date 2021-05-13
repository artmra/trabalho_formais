from .parserGrammar import ParserGrammar


def first_follow(G):
    def union(set_1, set_2):
        #merges the two sets and returns if the length has changed or not (if the set was updated)
        set_1_len = len(set_1)
        set_1 |= set_2

        return set_1_len != len(set_1)

    # creates the 'first' set to all symbols
    first = {symbol: set() for symbol in G.symbols}
    # adds to the 'first' set of all terminals, themselves
    first.update((terminal, {terminal}) for terminal in G.terminals)
    # creates the 'follow' set for all non terminals
    follow = {symbol: set() for symbol in G.non_terminals}
    # add end of sentence to follow of the start symbol
    follow[G.start].add('$')

    ## while there are symbols to add
    while True:
        updated = False

        for head, bodies in G.productions.items():
            for body in bodies:
                for symbol in body:
                    if symbol != '&':
                        updated |= union(first[head], first[symbol] - set('&'))

                        if '&' not in first[symbol]:
                            break
                    else:
                        updated |= union(first[head], set('&'))
                else:
                    updated |= union(first[head], set('&'))

                aux = follow[head]
                for symbol in reversed(body):
                    if symbol == '&':
                        continue
                    if symbol in follow:
                        updated |= union(follow[symbol], aux - set('&'))
                    if '&' in first[symbol]:
                        aux = aux | first[symbol]
                    else:
                        aux = first[symbol]

        if not updated:
            return first, follow

class SLRParser:
    def __init__(self, G):
        # creates S' -> S
        self.G_prime = ParserGrammar(f"{G.start}' -> {G.start}\n{G.grammar_str}")
        self.max_G_prime_len = len(max(self.G_prime.productions, key=len))
        self.G_indexed = []

        for head, bodies in self.G_prime.productions.items():
            for body in bodies:
                self.G_indexed.append([head, body])

        self.first, self.follow = first_follow(self.G_prime)
        self.C = self.items(self.G_prime)
        self.action = list(self.G_prime.terminals) + ['$']
        self.goto = list(self.G_prime.non_terminals - {self.G_prime.start})
        self.parse_table_symbols = self.action + self.goto
        self.parse_table = self.build_parser_table()

    def CLOSURE(self, I):
        J = I

        while True:
            item_len = len(J)

            # for (each item A -> a.B<beta> in J)
            for head, bodies in J.copy().items():
                # for (each production B -> <gama> of G)
                for body in bodies.copy():

                    # if the body has a dot (its being checked)
                    if '.' in body[:-1]:
                        symbol_after_dot = body[body.index('.') + 1]

                        # if the symbol after the dot is a non terminal
                        if symbol_after_dot in self.G_prime.non_terminals:
                            # for all the production on which the symbol after dot is the head
                            for G_body in self.G_prime.productions[symbol_after_dot]:
                                J.setdefault(symbol_after_dot, set()).add(
                                    ('.',) if G_body == ('&',) else ('.',) + G_body)

            if item_len == len(J):
                return J

    def GOTO(self, I, X):
        goto = {}

        # for all productions
        for head, bodies in I.items():
            # get bodies from production head
            for body in bodies:
                # if the body has a dot not on the last position (if there is still symbols to be checked)
                if '.' in body[:-1]:
                    #get dot position
                    dot_position = body.index('.')

                    # if the symbol after the dot is the symbol being checked
                    if body[dot_position + 1] == X:
                        # change places for symbol and dot
                        replaced_dot_body = body[:dot_position] + (X, '.') + body[dot_position + 2:]

                        for closureHeads, closureBodies in self.CLOSURE({head: {replaced_dot_body}}).items():
                            goto.setdefault(closureHeads, set()).update(closureBodies)

        return goto

    def items(self, grammar):
        # C = CLOSURE({[S' -> .S]})
        C = [self.CLOSURE({grammar.start: {('.', grammar.start[:-1])}})]

        while True:
            item_len = len(C)

            # for (each set of items I in C)
            for I in C.copy():
                # for (each grammar symbol X)
                for X in grammar.symbols:
                    goto = self.GOTO(I, X)

                    # if GOTO(I,X) is not empty and not in C)
                    if goto and goto not in C:
                        # add GOTO(I,X) to C
                        C.append(goto)

            # until no new sets of items are added to C on a round
            if item_len == len(C):
                return C

    def build_parser_table(self):
        parse_table = {r: {c: '' for c in self.parse_table_symbols} for r in range(len(self.C))}

        for i, I in enumerate(self.C):
            for head, bodies in I.items():
                for body in bodies:
                    # if [A -> <alpha>.a<beta>] is in Ii (...)"
                    if '.' in body[:-1]:
                        symbol_after_dot = body[body.index('.') + 1]
                        # "(...) and GOTO(Ii, a) = Ij, then set ACTION[i,a] to "shift j". Here a must be a terminal"
                        if symbol_after_dot in self.G_prime.terminals:
                            s = f's{self.C.index(self.GOTO(I, symbol_after_dot))}'

                            if s not in parse_table[i][symbol_after_dot]:
                                if 'r' in parse_table[i][symbol_after_dot]:
                                    parse_table[i][symbol_after_dot] += '/'

                                parse_table[i][symbol_after_dot] += s
                    # if [A -> a.] is in Ii, then set ACTION[i,a] to "reduce A->a (...)"
                    elif body[-1] == '.' and head != self.G_prime.start:
                        # "(...) for all a in FOLLOW(A); here A may not be S' (G_prime.start)
                        for j, (G_head, G_body) in enumerate(self.G_indexed):
                            if G_head == head and (G_body == body[:-1] or G_body == ('&',) and body == ('.',)):
                                for f in self.follow[head]:
                                    if parse_table[i][f]:
                                        parse_table[i][f] += '/'

                                    parse_table[i][f] += f'r{j}'

                                break

                    # if [S' -> S.] is in Ii, then set ACTION[i,$] to "accept"
                    else:
                        parse_table[i]['$'] = 'acc'

            # The GOTO transitions for state i are constructed for all nonterminals A
            # using the rule: If GOTO(Ii, a) = ij, the GOTO[i,a] = j
            for A in self.G_prime.non_terminals:  # CASE 3
                j = self.GOTO(I, A)

                if j in self.C:
                    parse_table[i][A] = self.C.index(j)

        return parse_table

    def parse_string(self, w):
        buffer = f'{w} $'.split()
        pointer = 0
        a = buffer[pointer]
        stack = ['0']
        symbols = ['']
        accepted = False

        step = 0
        while True:
            s = int(stack[-1])
            step += 1

            #TODO traduzir erros
            if a not in self.parse_table[s]:
                raise Exception('Palavra Rejeitada!\nSimbolo desconhecido {}'.format(a))
                # message = f'ERROR: Simbolo desconhecido {a}'
                # return accepted, message

            elif not self.parse_table[s][a]:
                raise Exception('Palavra Rejeitada!\nEntrada não foi reconhecida {} {}'.format(s, a))
                # message = 'ERROR: Entrada não foi reconhecida input cannot be parsed by given productions'
                # return accepted, message

            # elif '/' in self.parse_table[s][a]:
            #     message = f'ERROR: reduce conflict at state {s}, symbol {a}'
            #     return accepted, message

            elif self.parse_table[s][a].startswith('s'):
                stack.append(self.parse_table[s][a][1:])
                symbols.append(a)
                pointer += 1
                a = buffer[pointer]

            elif self.parse_table[s][a].startswith('r'):
                head, body = self.G_indexed[int(self.parse_table[s][a][1:])]

                if body != ('&',):
                    stack = stack[:-len(body)]
                    symbols = symbols[:-len(body)]

                stack.append(str(self.parse_table[int(stack[-1])][head]))
                symbols.append(head)

            elif self.parse_table[s][a] == 'acc':
                accepted = True
                message = 'Palavra Aceita!'
                break

        return accepted, message