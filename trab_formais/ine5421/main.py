# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from functions import read_af, read_gr


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    af1 = read_af("test-files/conversao_e_io/teste1-af.jff")
    af1.write_to_file("test-files/resultados-testes/teste1-af-resultado.jff")
    af1 = read_af("test-files/conversao_e_io/teste2-af.jff")
    af1.write_to_file("test-files/resultados-testes/teste2-af-resultado.jff")
    af1 = read_af("test-files/conversao_e_io/teste3-af.jff")
    af1.write_to_file("test-files/resultados-testes/teste3-af-resultado.jff")
    # readGR("test-files/teste1conversaoParaAF.jff")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
