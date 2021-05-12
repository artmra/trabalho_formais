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
            raise Exception(ERRO_1)
        self.start_symbol = str(meta_data[0])
        # verifica se há pelo menos um símbolo
        self.non_terminals = [str(symbol) for symbol in meta_data[1].split(",")]
        if self.start_symbol not in self.non_terminals:
            raise Exception(ERRO_2_1 + self.start_symbol + ERRO_2_2)
        # verifica se nenhum dos símbolos não terminais pertence ao conjunto de terminais
        self.terminals = [str(symbol) for symbol in meta_data[2].split(",")]
        for symbol in self.non_terminals:
            if symbol in self.terminals:
                raise Exception(ERRO_3_1 + symbol + ERRO_3_2)
        # cria as produções
        self.productions = dict()
        for production in productions:
            try:
                head, body = [str(p) for p in production.split("->")]
                if head == "":
                    line = str(4 + productions.index(production))
                    raise Exception(ERRO_5 + line + ")")
                # TODO: checar se todas os símbolos fazem parte do conjunto de terminais ou não terminais
            except:
                line = str(4 + productions.index(production))
                raise Exception(ERRO_4 + line + ")")
            # TODO: implementar a detecção de encolhimento de sentença
            body = [str(b) for b in body.split("|")]
            if len(body) < 1 or body[0] == "":
                line = str(4 + productions.index(production))
                raise Exception(ERRO_6 + line + ")")
            if head in self.productions.keys():
                line = str(4 + productions.index(production))
                raise Exception(ERRO_7 + line + ")")
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

    def eliminate_left_recursion(self):
        # elimina recursões diretas iniciais
        self.eliminate_direct_recursion()
        # elimina recursões indiretas, enquanto houver
        while self.eliminate_indirect_recursion():
            continue

    def eliminate_direct_recursion(self):
        # as novas regras de produção são armazenadas aqui
        new_prod_rules = dict()
        # para todas as produções, checa recursao direta e as resolve
        for head, body in self.productions.items():
            # eventuais recursividades diretas são adicionadas aqui
            recursive_prods = []
            # verifica recursividade direta para produções dessa regra
            for prod in body:
                # cabeças com menos 's não podem dar match nos n terminais com mais 's
                # por exemplo, A''ab começa com A' ou A''; logo, deve-se verificar se o
                # caractere após o a cabeça da produção não é um '
                if prod.startswith(head) and (len(prod) == len(head) or prod[len(head)] != "'"):
                    recursive_prods.append(prod)

            #retira eventuais duplicatas
            recursive_prods = list(set(recursive_prods))

            # se houver recursão direta faz as alterações do algoritmo da professora
            if recursive_prods:
                # gera o novo n-terminal
                new_non_terminal = head + "'"
                while new_non_terminal in self.non_terminals:
                    new_non_terminal = new_non_terminal + "'"
                # o adiciona a lista de n-terminais
                self.non_terminals.append(new_non_terminal)
                # obtem as producoes nas quais n ocorre recursao direta, e já as modifica
                # por exemplo, se a cabeça é A, a nova cabeca é A' e a prod era Dbc;
                # apos a linha abaixo a prod se torna DbcA'
                head_new_body = [p + new_non_terminal for p in body if p not in recursive_prods]

                # altera as producoes nas quais ocorre recursao direta
                # por exemplo, se a cabeca é A, a nova cabeca é A' e a prod era Abc;
                # apos a linha abaixo a prod se torna bcA'
                new_non_terminal_body = [p.replace(head, '', 1) + new_non_terminal for p in recursive_prods]

                # adiciona & para escape
                new_non_terminal_body.append('&')
                if '&' not in self.terminals:
                    self.terminals.append('&')

                # altera as regras de produção da cabeça atual
                self.productions[head] = list(set(head_new_body))

                # adiciona as novas regras de produção no dic auxiliar
                new_prod_rules.update({new_non_terminal: list(set(new_non_terminal_body))})

        # adiciona as novas regras de produção à lista de produções da gramática
        self.productions.update(new_prod_rules)
        self.production_heads = list(self.productions.keys())

    def eliminate_indirect_recursion(self):
        """
        :return: boolean
            não alguma recursão indireta tiver sido identificada retorna true; caso contrário, retorna false.
        """
        need_to_run_again = False
        # para todas as produções, checa recursao indireta e as transforma em recursao direta
        # EXEMPLO: S -> Abc | de | S
        production_heads = list()
        production_heads.extend(self.production_heads)
        while production_heads:
            exists_indirect_recursion = False
            head = production_heads.pop()
            body = self.productions[head]
            # novo body, no qual eventuais resursões diretas estarão
            new_body = []
            # verifica as produções
            for prod in body:
                first_symbol = self.start_with_nonTerminal(prod)
                # verifica se a produção começa com n-terminal
                # EXEMPLO: para Abc, first_symbol é A
                if first_symbol is not None and first_symbol != head:
                    # caso head apareca como primeiro simbolo em uma produção do primeiro simbolo, há recursão indireta
                    # e as produções do primeiro símbolo estarão em prods_to_add
                    # EXEMPLO: A -> Sfg | Sh | ij
                    prods_to_add = self.start_with(head, self.productions[first_symbol])
                    # verifica se existe alguma espécie de recursividade indireta
                    # (caso no qual a lista prod_to_add n é vazia)
                    if prods_to_add:
                        exists_indirect_recursion = True
                        # transforma a produção com recursividade indireta em produções com recursividade direta
                        # EXEMPLO: a seguinte linha transforma Abc em bc
                        prod_sufix = prod.replace(first_symbol, '', 1)
                        # EXEMPLO: a seguinte linha adiciona bc no final de todas as produções em prods_to_add
                        #          Sfgbc | Shbc | ijbc
                        new_body.extend([p + prod_sufix for p in prods_to_add])
                    else:
                        new_body.append(prod)
                else:
                    new_body.append(prod)
            # altera as produções da cabeça de produção head
            self.productions[head] = new_body
            if exists_indirect_recursion:
                need_to_run_again = True
                self.eliminate_direct_recursion()
        return need_to_run_again

    def start_with_nonTerminal(self, prod):
        """
        :return: string
            não terminal que inicia uma produção qualquer; caso a produção n começe com n-terminal, retorna None
        """
        self.non_terminals.sort(reverse=True, key=len)
        for non_terminal in self.non_terminals:
            if prod.startswith(non_terminal):
                return non_terminal
        return None

    def get_first_symbol(self, prod):
        """
        :return: string
            não terminal ou terminal que inicia uma produção qualquer;
        """
        gr_symbols = list(set(self.non_terminals).union(set(self.terminals)))
        # ordena a lista por tamanho
        gr_symbols.sort(reverse=True, key=len)
        for symbol in gr_symbols:
            if prod.startswith(symbol):
                return symbol

    def start_with(self, symbol, prod_body):
        """
        :return: list
            lista contendo todas as produçẽos, caso alguma começe com o símbolo; caso contrário, retorna uma lista vazia
        """
        for prod in prod_body:
            if prod.startswith(symbol) and (len(prod) == len(symbol) or prod[len(symbol)] != "'"):
                return prod_body
        return []

    def eliminar_n_determinismo(self):
        self.eliminar_n_determinismo_direto()
        n_prods = 0
        # roda enquanto novos n-terminais forem definidos e um loop n for identificado
        # apenas para garantir retorno, esse algoritmo considera que caso o loop execute mais
        # de 100 vezes há algum loop
        numero_execucoes = 0
        while n_prods != len(self.productions) and numero_execucoes != 100:
            n_prods = len(self.productions)
            self.eliminar_n_determinismo_direto(remover_indireto=True)
            numero_execucoes = numero_execucoes + 1

    def eliminar_n_determinismo_direto(self, remover_indireto=False):
        heads_to_check = list()
        # inicialmente checa os corpos das produções já existentes
        heads_to_check.extend(self.production_heads)
        # variável que será usada para identificar um possível loop. Não é um mecanismo muito robusto, pois apenas conta
        # ate determinado numero. Mesmo assim é o suficiente para pelo menos fazer o algoritmo retornar em caso de loop
        possivel_loop = 0
        while heads_to_check:
            possivel_loop = possivel_loop + 1
            head = heads_to_check.pop()
            body = self.productions[head]
            # se for verdadeiro tentará transformar o não determinismo indireto em direto
            if remover_indireto:
                # conjunto auxiliar no qual os potenciais n-determinismos diretos serão explicitados
                provisory_body = set()
                # deve percorrer body mudando o primeiro simbolo de cada produção pelas suas produções(se o mesmo for um n-terminal)
                for prod in body:
                    symbol = self.get_first_symbol(prod)
                    # se o simbolo for um n-terminal cria novas produções
                    if symbol in self.non_terminals and symbol != head:
                        # parte da produção original sem o n-terminal
                        sufix = prod.replace(symbol, '', 1)
                        # cria novas produções adicionando o sufixo da antiga às produções do n-terminal
                        provisory_body.update(set([p + sufix for p in self.productions[symbol]]))
                    else:
                        provisory_body.add(prod)
                # usa as produções alteradas para a eliminação de eventuais não determinismos diretos que foram gerados
                body = list(provisory_body)
            # dicionário de listas, no qual as produções de uma cabeça serão agrupadas com base no seu símbolo inicial
            prods_equi = dict()
            for prod in body:
                symbol = self.get_first_symbol(prod)
                if symbol in prods_equi.keys():
                    if len(symbol) == len(prod):
                        # prods de apenas um símbolos devem permanecer inalteradas
                        prods_equi.update({symbol + '_unitario': [prod]})
                    else:
                        # adiciona a lista das prods q começam com o mesmo simbolo, caso haja
                        prods_equi[symbol].append(prod)
                else:
                    if len(symbol) == len(prod):
                        # prods de apenas um símbolos devem permanecer inalteradas
                        prods_equi.update({symbol + '_unitario': [prod]})
                    else:
                        # cria uma nova lista, caso n exista
                        prods_equi.update({symbol: [prod]})
            # se o numero de entradas no dicionario prods_equi for menor q o de elementos no corpo, significa que houve
            # agrupamento, e devem ser criados novos n-terminais conforme o algoritmo da professora; caso não haja as
            # produções não são alteradas
            if len(prods_equi) < len(body):
                # novo corpo da cabeça atual
                new_body = list()
                # percorre e cria novos n-terminais para cada lista com mais de uma prod
                for symbol, prods in prods_equi.items():
                    if len(prods) == 1:
                        # não necessita criar um novo n-terminal
                        # é usado extend apenar pq nesse caso a lista tem apenas um elemento
                        new_body.extend(prods)
                        continue
                    # gera um novo n-terminal
                    new_non_terminal = head + "'"
                    while new_non_terminal in self.non_terminals:
                        new_non_terminal = new_non_terminal + "'"
                    # popula a lista(sem eventuais repeticoes) de produções do novo n-terminal
                    new_non_terminal_body = list(set([p.replace(symbol, '', 1) for p in prods]))
                    # adiciona a produção alterada ao novo corpo da cabeça atual
                    new_body.append(symbol+new_non_terminal)
                    #adiciona as novas regras de produção à gramática
                    self.productions.update({new_non_terminal: new_non_terminal_body})
                    self.production_heads = list(self.productions.keys())
                    self.non_terminals.append(new_non_terminal)
                    #adiciona o novo n-terminal a lista de cabecas a se checar
                    heads_to_check.append(new_non_terminal)
                # atualiza o corpo da cabeça atual, pois houveram mudanças
                self.productions[head] = new_body
            if possivel_loop == 100:
                break
