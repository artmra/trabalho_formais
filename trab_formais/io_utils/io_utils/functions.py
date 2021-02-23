from .representatios import AF, GR

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
        try:
            meta_data = [lines[x].replace(" ", "").strip() for x in range(3)]
            productions = [lines[x].replace(" ", "").strip() for x in range(3, len(lines))]
        except:
            raise Exception(ERROR + "GR.")
    return GR(meta_data, productions)


def read_gr_string(string):
    lines = string.splitlines()
    try:
        meta_data = [lines[x].replace(" ", "").strip() for x in range(3)]
        productions = [lines[x].replace(" ", "").strip() for x in range(3, len(lines))]
    except:
        raise Exception(ERROR + "GR.")
    return GR(meta_data, productions)
