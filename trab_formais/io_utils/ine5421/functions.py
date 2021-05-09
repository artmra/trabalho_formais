from .af import AF
from .gr import GR
from .er import ER
import os

ERROR = "Número insuficiente de linhas para definir um "


def read_af_file(filename):
    with open(filename, "r") as file:
        lines = file.readline().split(os.linesep)
        meta_data, transitions = read_lines_af(lines)
    return AF(meta_data, transitions)


def read_af_string(string):
    lines = string.split(os.linesep)
    meta_data, transitions = read_lines_af(lines)
    return AF(meta_data, transitions)


def read_lines_af(lines):
    try:
        meta_data = [lines[x].replace(" ", "").replace("/r", "").strip() for x in range(4)]
        transitions = [lines[x].replace(" ", "").replace("/r", "").strip() for x in range(4, len(lines))]
    except:
        raise Exception(ERROR + "AF.")
    return meta_data, transitions


def read_gr_file(filename):
    with open(filename, "r") as file:
        lines = file.readline()
        lines = lines.split(os.linesep)
        meta_data, productions = read_gr_lines(lines)
    return GR(meta_data, productions)


def read_gr_string(string):
    lines = string.split(os.linesep)
    meta_data, productions = read_gr_lines(lines)
    return GR(meta_data, productions)


def read_gr_lines(lines):
    print("bl")
    try:
        meta_data = [lines[x].replace(" ", "").replace("/r", "").strip() for x in range(3)]
        transitions = [lines[x].replace(" ", "").replace("/r", "").strip() for x in range(3, len(lines))]
    except:
        raise Exception(ERROR + "GR.")
    return meta_data, transitions


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


def convert_to_af(gr):
    estado_inicial = gr.start_symbol
    alfabeto_list = gr.terminals

    if "&" in alfabeto_list:
        alfabeto_list.remove("&")

    alfabeto = ','.join(map(str, alfabeto_list))
    estados = gr.non_terminals
    # criado novo estado para o AF
    estados_aceitacao_list = ["F1"]

    # caso a gramatica aceite a palavra vazia, o estado inicial é de aceitação também
    if "&" in gr.productions.get("S"):
        estados_aceitacao_list.append("S")

    estados_aceitacao = ','.join(map(str, estados_aceitacao_list))
    trans = []
    for k in gr.productions.keys():
        for p in gr.productions.get(k):
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


def union_afs(af1, af2, inter):
    """Modifica a área de texto para uma AF resultado da união ou interseção
    da AF previamente contida pela área de texto e a AF recém selecionada em
    arquivo.
    Utiliza o algoritmo da Construção por Produto para união e interseção.
    Parameters
    ----------
    request : HttpRequest
        Requisição web feita pelo usuário através do navegador
    inter : bool
        Se `inter` for `True`, a interseção das AFs é feita ao invés da união
    """
    n_states = af1.n_states * af2.n_states
    start_state = af1.start_state + '-' + af2.start_state
    states = []
    for s1 in af1.states:
        for s2 in af2.states:
            states.append(s1 + '-' + s2)
    accept_states = []
    if inter:
        for s1 in af1.accept_states:
            for s2 in af2.accept_states:
                accept_states.append(s1 + '-' + s2)
    else:
        for acpt_states in af1.accept_states:
            for s in states:
                if s.split('-')[0] == acpt_states:
                    accept_states.append(s)
        for acpt_states in af2.accept_states:
            for s in states:
                if s.split('-')[1] == acpt_states:
                    accept_states.append(s)
        accept_states = list(dict.fromkeys(accept_states))
    alphabet = list(dict.fromkeys(af1.alphabet + af2.alphabet))
    transition_table = {}
    for s in states:
        for symbol in alphabet:
            try:
                new_transition_p1 = ''.join(af1.transition_table[s.split('-')[0]][symbol]) + '-'
                new_transition_p2 = ''.join(af2.transition_table[s.split('-')[1]][symbol])
                if s in transition_table:
                    transition_table[s].update({symbol: [new_transition_p1 + new_transition_p2]})
                else:
                    transition_table.update({s: {symbol: [new_transition_p1 + new_transition_p2]}})
            except KeyError:
                continue
    return AF(None, None, n_states, start_state, accept_states, alphabet, transition_table, False, states)


def read_er(expression):
    return ER(expression)

def read_pseudocode(pseudocode, af):
    words = pseudocode.split()

    dic = dict()

    for word in words:
        if af.recognize(word):
            s = ''
            for l in af.label_list[af.last_state]:
                if s == '':
                    s = l
                else:
                    s = s + " ou " + l
            dic[word] = s
        else:
            dic[word] = "Não reconhecido"
    # print(dic)

    return dic

def create_af_from_al(rules):
    tokens = dict()
    # lines = read_er(file_content.split(":")[1].strip())
    lines = rules.split(os.linesep)
    tokens = dict()
    # first = lines[0].split(';')[0]
    # second = lines[1].split(';')[0]
    for er_definition in lines:
        if er_definition == '':
            continue
        label, er_ = er_definition.split(';')
        # Cria er
        er = read_er(er_.split(":")[1].strip())
        # Converte para af
        af = er.convert_to_af()
        # Se preciso minimiza o af(esse processo já o determiniza, caso necessário)
        af.set_label_list(dict.fromkeys(af.accept_states, [label]))
        tokens.update({label: af})

    # realiza a união de todos os AFs
    labels = list(tokens.keys())
    final_af = tokens[labels.pop(0)]
    for label in labels:
        final_af.union_with(tokens[label])
    
    # print(final_af.label_list)
    # print(final_af)
    # print(final_af.label_list[])
    
    return final_af

    # print(labels)
    # print(final_af.recognize('def'))
    # print(final_af.recognize('name'))
    # TODO: Realiza a união dos afs
    # TODO: Relaciona os estados de aceitação aos labels de alguma forma
    # TODO: Retorna o af
