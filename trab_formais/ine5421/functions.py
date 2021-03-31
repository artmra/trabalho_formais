from .af import AF
from .gr import GR
from .er import ER

ERROR = "Número insuficiente de linhas para definir um "


def read_af_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        meta_data, transitions = read_lines_af(lines)
    return AF(meta_data, transitions)


def read_af_string(string):
    lines = string.splitlines()
    meta_data, transitions = read_lines_af(lines)
    return AF(meta_data, transitions)


def read_lines_af(lines):
    try:
        meta_data = [lines[x].replace(" ", "").strip() for x in range(4)]
        transitions = [lines[x].replace(" ", "").strip() for x in range(4, len(lines))]
    except:
        raise Exception(ERROR + "AF.")
    return meta_data, transitions


def read_gr_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        meta_data, productions = read_gr_lines(lines)
    return GR(meta_data, productions)


def read_gr_string(string):
    lines = string.splitlines()
    meta_data, productions = read_gr_lines(lines)
    return GR(meta_data, productions)


def read_gr_lines(lines):
    try:
        meta_data = []
        productions = []
        i = 0
        while len(meta_data) < 3:
            line = lines[i].replace(" ", "").strip()
            i += 1
            if line != "":
                meta_data.append(line)

        while i < len(lines):
            line = lines[i].replace(" ", "").strip()
            print(line)
            i += 1
            if line != "":
                productions.append(line)
        # meta_data = [lines[x].replace(" ", "").strip() for x in range(3)]
        # productions = [lines[x].replace(" ", "").strip() for x in range(3, len(lines))]
    except:
        raise Exception(ERROR + "GR.")
    return meta_data, productions


def convert_to_gr(af):
    nao_terminais = ','.join(map(str, af.states))
    simb_inicial = af.start_state
    terminais = ','.join(map(str, af.alphabet))
    metadata = [simb_inicial, nao_terminais, terminais]
    prod = []
    for origin, transitions in af.transition_table.items():
        transition = origin + " -> "
        idx = 1
        for symbol, states in transitions.items():
            for idx2, state in enumerate(states, start=1):
                if state in af.accept_states:
                    transition += "" + symbol
                else:
                    transition += "" + symbol + state
                if idx2 < len(states):
                    print(idx2)
                    print(states)
                    transition += " | "
            if idx < len(transitions):
                transition += " | "
            idx += 1
        prod.append(transition)
    return GR(metadata, prod)


def convert_to_af(self):
    # metadata = [numero de estados, estado inicial, [estados de aceitação], [alfabeto]]
    # transitions = [transicoes]
    estado_inicial = self.start_symbol
    alfabeto_list = self.terminals

    if "&" in alfabeto_list:
        alfabeto_list.remove("&")

    alfabeto = ','.join(map(str, alfabeto_list))
    estados = self.non_terminals
    # criado novo estado para o AF
    estados_aceitacao_list = ["F1"]

    # caso a gramatica aceite a palavra vazia, o estado inicial é de aceitação também
    if "&" in self.productions.get("S"):
        estados_aceitacao_list.append("S")

    estados_aceitacao = ','.join(map(str, estados_aceitacao_list))
    trans = []
    for k in self.productions.keys():
        for p in self.productions.get(k):
            ## transiçoes do tipo S -> aA
            if len(p) == 2:
                letter = p[0]
                state = p[1]
                ##transiçao "0,a,1"
                trans.append(k + "," + letter + "," + state)
                ## transiçoes do tipo S -> a
            else:
                if p != "&":
                    trans.append(k + "," + p + ",F1")

    meta = [len(estados), estado_inicial, estados_aceitacao, alfabeto]
    return AF(meta, trans)
