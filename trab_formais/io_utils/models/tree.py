from af import AF as automato


class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data

        self.left = left
        self.right = right

        self.firstpos = list()
        self.lastpos = list()

        self.nullable = None


class Tree:
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

        self.order(self.root)
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
            if c in self.alphabet or c in '#|':
                elements_list.append(c)
            if c == '*':
                if len(elements_list[i - 2]) > 1 and len(elements_list) > 1:
                    elements_list[i - 2] = f'({elements_list[i - 2]})*'
                else:
                    elements_list.append('*')
            elif c == '(':
                elements_list.append(self.get_internal_regex(regex[i + 1:]))
                aux += len(elements_list[i])

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

        if node.data == '|':
            node.nullable = node.left.nullable or node.right.nullable
            node.firstpos = node.left.firstpos + node.right.firstpos
            node.lastpos = node.left.lastpos + node.right.lastpos

        if node.data == '.':
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

        if node.data == '*':
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

    def order(self, node):
        if node is None:
            return

        self.order(node.left)
        self.order(node.right)

    def optimize(self, node):
        if node is None:
            return
        if node.data == '|':
            if node.left.data == '.':
                node.left = node.left.right
            if node.right.data == '.':
                node.right = node.right.right

        node.left = self.optimize(node.left)
        node.right = self.optimize(node.right)

        return node

    def post_order(self, node):
        if node:
            self.post_order(node.left)
            self.post_order(node.right)
            if node.data in self.alphabet or node.data == '#':
                self.tree_list.append(node.data)

    def create_af_from_tree(self, node):
        start_state = frozenset(node.firstpos)
        states = list()
        n_states = 0
        final_states = list()
        states_to_visit = [start_state]

        transitions = {}
        while states_to_visit:
            origin_state = states_to_visit.pop()
            string_origin_state = [str(i) for i in origin_state]
            string_origin_state = automato.get_name(string_origin_state)
            transitions[string_origin_state] = {}

            for symbol in self.alphabet:
                same_transition = list()
                for state in origin_state:
                    # if (state-1) < len(self.tree_list):
                    if self.tree_list[state - 1] == symbol:
                        same_transition.append(state)

                new_state = frozenset()
                for pos in same_transition:
                    new_state |= (self.followpos_table.get(pos))
                # Se estado possui a posiçaõ do elemento # então é um estado de aceitação
                # é somado mais um por causa do index começando por 0
                if (self.tree_list.index('#') + 1) in new_state:
                    final_states.append(new_state)
                # Se é um estado novo, adiciona a lista de estados
                if new_state not in states:
                    n_states += 1
                    states_to_visit.append(new_state)
                    states.append(new_state)

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
            list_final_states.append(final_state_name)

        af = automato(None, None)
        af.set_alphabet(self.alphabet)
        af.set_transistions(transitions)
        af.set_final_states(list_final_states)
        af.set_start_state(start_state_name)
        af.set_n_states(n_states)
        af.set_is_afnd(False)

        return af
