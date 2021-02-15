from functions import read_af, read_gr


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    # af1 = read_af("test-files/conversao_e_io/teste1-af.jff")
    # af1.write_to_file("test-files/resultados-testes/teste1-af-resultado.jff")
    # af1 = read_af("test-files/conversao_e_io/teste2-af.jff")
    # af1.write_to_file("test-files/resultados-testes/teste2-af-resultado.jff")
    # af1 = read_af("test-files/conversao_e_io/teste3-af.jff")
    # af1.write_to_file("test-files/resultados-testes/teste3-af-resultado.jff")
    gr = read_gr("test-files/conversao_e_io/teste1-gr.jff")
    print(gr)
