from functions import read_af_string
from af import AF as automato


class Node:
    """
        Classe usada para representar Arvore de Aho

        Attributes
        ----------
        data: str
            Valor do nodo
        left: Node
            Filho esquerdo
        right: Node
            Filho direito
        firstpos: list
            lista de firstpos do node
        lastpos: list
            lista de lastpos do node
        nullable: bool
            boolean se o nodo é nullable ou não

        Methods
        -------

    """
    def __init__(self, data=None, left=None, right=None):
        self.data = data

        self.left = left
        self.right = right

        self.firstpos = list()
        self.lastpos = list()

        self.nullable = None


class Tree:
    """
        Classe usada para representar Arvore de Aho

        Attributes
        ----------
        alphabet: set
            set do alfabeto de entrada
        root: Node
            node raiz da arvore
        followpos_table: dict
            tabela de followpos dos nodos
        tree_list: list
            lista com nodos folhas com os alfabetos

        Methods
        -------
        make_tree(regex):
            Descrição
        split_tree(list=elements):
            Descrição 
        search_incomplete_nodes(Node=node, bool=tree_unfinished)
            Descrição
        split_elements(regex):
            Descrição
        get_internal_regex(regex):
            descrição
        set_leaf_nodes_values(Node=node, int=pos)
            descrição
        generate_first_last_pos(Node=node)
            descrição
        generate_followpos(Node=node)
            descrição
        optimize(Node=node)
            descrição
        post_order(Node=node)
            Coloca a arvore em post order no atributo tree_list
        create_af_from_tree(Node=node)
            Metodo que cria o AFD a partir dos followpos ja criados

    """
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.root = None
        self.followpos_table = dict()
        self.tree_list = list()

    def make_tree(self, regex):
        elements_list = self.split_elements(regex)
        if '|' in elements_list:
            self.root = Node('|', left=elements_list[0], right=elements_list[2])
            return
        self.root = self.split_tree(elements_list)

        tree_unfinished = True
        while tree_unfinished:
            self.root, tree_unfinished = self.search_incomplete_nodes(self.root, False)
        self.set_leaf_nodes_values(self.root, 1)

        self.optimize(self.root)
        self.generate_first_last_pos(self.root)

        self.generate_followpos(self.root)
        for i in range(len(self.followpos_table)):
            self.followpos_table[i + 1] = set(self.followpos_table[i + 1])

        self.post_order(self.root)

        return self.create_af_from_tree(self.root)

    def split_tree(self, elements):
        if len(elements) == 1:
            return Node('.', right=Node(elements[0]))
        if '|' in elements:
            return Node('|', left=Node(elements[0]), right=Node(elements[2]))
        if elements[-1] == '*':
            if len(elements) > 2:
                return Node('.', left=self.split_tree(elements[:-2]), right=Node('*', right=Node(elements[-2])))
            return Node('.', right=Node('*', right=Node(elements[-2])))

        return Node('.', left=self.split_tree(elements[:-1]), right=Node(elements[-1]))

    def search_incomplete_nodes(self, node, tree_unfinished):
        if node is None:
            return node, tree_unfinished

        if len(node.data) == 1:
            node.left, tree_unfinished = self.search_incomplete_nodes(node.left, tree_unfinished)
            node.right, tree_unfinished = self.search_incomplete_nodes(node.right, tree_unfinished)
            return node, tree_unfinished

        else:
            elements = self.split_elements(node.data)
            node = self.split_tree(elements)
            return node, True

    def split_elements(self, regex):
        elements_list = list()
        aux = 0
        for i in range(len(regex)):
            if (i + aux) == len(regex):
                break
            c = regex[i + aux]
            if c in self.alphabet or c in '#|&':
                elements_list.append(c)
            if c == '*':
                if len(elements_list[i - 1]) > 1 and len(elements_list) > 1:
                    elements_list[i - 1] = f'({elements_list[i - 1]})*'
                else:
                    elements_list.append('*')
            elif c == '(':
                elements_list.append(self.get_internal_regex(regex[i + aux + 1:]))
                aux += len(elements_list[-1]) + 1
        return elements_list

    @staticmethod
    def get_internal_regex(regex):
        internal_regex = str()
        stack = list()

        for c in regex:
            if c == '(':
                stack.append(c)
            elif c == ')':
                if not stack:
                    return internal_regex
                else:
                    stack.pop()
            internal_regex += c

    def set_leaf_nodes_values(self, node, pos):
        """Método utilizado para settar o valor dos nodos folha, que representam os elementos do alfabeto da ER"""
        if node is None:
            return pos

        if (node.left is None) and (node.right is None):
            node.firstpos.append(pos)
            node.lastpos.append(pos)
            node.nullable = False
            return pos + 1

        pos = self.set_leaf_nodes_values(node.left, pos)
        return self.set_leaf_nodes_values(node.right, pos)

    def generate_first_last_pos(self, node):
        if node is None:
            return

        if node.left is not None:
            self.generate_first_last_pos(node.left)
        if node.right is not None:
            self.generate_first_last_pos(node.right)

        if node.data == '&':
            node.nullable = True

        elif node.data == '|':
            node.nullable = node.left.nullable or node.right.nullable
            node.firstpos = node.left.firstpos + node.right.firstpos
            node.lastpos = node.left.lastpos + node.right.lastpos

        elif node.data == '.':
            if node.left is None:
                node.nullable = node.right.nullable
                node.firstpos = node.right.firstpos
                node.lastpos = node.right.lastpos
            elif node.right is None:
                node.nullable = node.left.nullable
                node.firstpos = node.left.nullable
                node.lastpos = node.left.lastpos
            else:
                node.nullable = node.left.nullable and node.right.nullable
                if node.left.nullable:
                    node.firstpos = node.left.firstpos + node.right.firstpos
                else:
                    node.firstpos = node.left.firstpos

                if node.right.nullable:
                    node.lastpos = node.left.lastpos + node.right.lastpos
                else:
                    node.lastpos = node.right.lastpos

        elif node.data == '*':
            node.nullable = True
            node.firstpos = node.right.firstpos
            node.lastpos = node.right.lastpos

    def generate_followpos(self, node):
        if node is None:
            return

        self.generate_followpos(node.left)
        self.generate_followpos(node.right)

        if node.data == '.':
            if node.left is not None:
                for i in node.left.lastpos:
                    if i not in self.followpos_table:
                        self.followpos_table[i] = node.right.firstpos
                    else:
                        self.followpos_table[i] += node.right.firstpos

        elif node.data == '*':
            for i in node.lastpos:
                if i not in self.followpos_table:
                    self.followpos_table[i] = node.firstpos
                else:
                    self.followpos_table[i] += node.firstpos

    # def order(self, node):
    #     if node is None:
    #         return
    #
    #     self.order(node.left)
    #     self.order(node.right)
    #     print(node.data)

    def optimize(self, node):
        if node is None:
            return

        if node.data == '|':
            if node.left.data == '.':
                node.left = node.left.right
            if node.right.data == '.':
                node.right = node.right.right

        elif node.data == '.' and node.left is None:
            node = node.right

        node.left = self.optimize(node.left)
        node.right = self.optimize(node.right)

        return node

    def post_order(self, node):
        """
        :return:
        """
        if node:
            self.post_order(node.left)
            self.post_order(node.right)
            if node.data in self.alphabet or node.data == '#':
                self.tree_list.append(node.data)

    def create_af_from_tree(self, node):
        """
        :param node: Node
            node raiz para inicializacao do metodo
        :return: string
            retorna o AF ja inicializado com os atributos necessarios
        """
        start_state = frozenset(node.firstpos)
        states = list()
        n_states = 1

        final_states = list()
        states_to_visit = [start_state]

        transitions = {}
        while states_to_visit:
            origin_state = states_to_visit.pop()
            string_origin_state = [str(i) for i in origin_state]
            string_origin_state = automato.get_name(string_origin_state)
            transitions[string_origin_state] = {}

            # Se estado possui a posiçaõ do elemento # então é um estado de aceitação
            # é somado mais um por causa do index começando por 0
            if (self.tree_list.index('#') + 1) in origin_state:
                    final_states.append(origin_state)

            for symbol in self.alphabet:
                # Ignora transição por epsilon
                if symbol == '&':
                    continue
                # Agrupa estados que possuem transição pelo mesmo simbolo
                same_transition = list()
                for state in origin_state:
                    # print(state)
                    if self.tree_list[state-1] == symbol:
                        same_transition.append(state)
                # print(same_transition)

                # Se não possui transição pelo simbolo, sai do loop
                if not same_transition:
                    continue

                new_state = frozenset()
                for pos in same_transition:
                    new_state |= (self.followpos_table.get(pos))
                # Se é um estado novo, adiciona a lista de estados
                if new_state not in states:
                    n_states += 1
                    states_to_visit.append(new_state)
                    states.append(new_state)
                # Formatando para string o novo estado
                string_new_state = [str(i) for i in new_state]
                string_new_state = automato.get_name(string_new_state)
                transitions[string_origin_state][symbol] = [string_new_state]

        # Formatando para string o estado inicial
        start_state = list(start_state)
        string_start_state = [str(i) for i in start_state]
        start_state_name = automato.get_name(string_start_state)
        # Formatando para string os estados finais
        list_final_states = list()
        for final_state in final_states:
            final_state_name = [str(i) for i in final_state]
            final_state_name = automato.get_name(final_state_name)
            if final_state_name not in list_final_states:
                list_final_states.append(final_state_name)
        # Seta os atributos do AFD
        af = automato(None, None)
        af.set_alphabet(self.alphabet)
        af.set_transistions(transitions)
        af.set_final_states(list_final_states)
        af.set_start_state(start_state_name)
        af.set_n_states(n_states)
        af.set_is_afnd(False)

        return af
