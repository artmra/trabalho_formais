from .representatios import AF, GR


def read_af(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        meta_data = [lines[x].replace(" ", "").strip() for x in range(4)]
        transitions = [lines[x].replace(" ", "").strip() for x in range(4, len(lines))]
    return AF(meta_data, transitions)


def read_gr(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        meta_data = [lines[x].replace(" ", "").strip() for x in range(3)]
        productions = [lines[x].replace(" ", "").strip() for x in range(3, len(lines))]
    return GR(meta_data, productions)
