from .representatios import AF, GR, GLC

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

def read_glc_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        meta_data, productions = read_gr_lines(lines)
    return GLC(meta_data, productions)


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
            line = lines[i].replace(" ","").strip()
            i += 1
            if line!="" :
                meta_data.append(line)

        while i < len(lines):
            line = lines[i].replace(" ", "").strip()
            #print(line)
            i += 1
            if line != "":
                productions.append(line)
        # meta_data = [lines[x].replace(" ", "").strip() for x in range(3)]
        # productions = [lines[x].replace(" ", "").strip() for x in range(3, len(lines))]
    except:
        raise Exception(ERROR + "GR.")
    return meta_data, productions
