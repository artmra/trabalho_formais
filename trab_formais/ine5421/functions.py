from representatios import AF


def read_af(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        meta_data = [lines[x].replace(" ", "").strip() for x in range(4) if lines[x] != ""]
        transitions = [lines[x].replace(" ", "").strip() for x in range(4, len(lines))]
    return AF(meta_data, transitions)


def read_gr(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        lines = [line.strip().replace(" ", "").split("->") for line in lines]
    count = 0
    for x in lines:
        count += 1
        print("Line {}: {}".format(count, x))
