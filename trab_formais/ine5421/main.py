from functions import read_af, read_gr

if __name__ == '__main__':
    af1 = read_af("test-files/conversao_e_io/teste1-af.jff")
    af1.write_to_file("test-files/resultados-testes/teste1-af-resultado.jff")
    af2 = read_af("test-files/conversao_e_io/teste2-af.jff")
    af2.write_to_file("test-files/resultados-testes/teste2-af-resultado.jff")
    af3 = read_af("test-files/conversao_e_io/teste3-af.jff")
    af3.write_to_file("test-files/resultados-testes/teste3-af-resultado.jff")
    gr1 = read_gr("test-files/conversao_e_io/teste1-gr.jff")
    gr1.write_to_file("test-files/resultados-testes/teste1-gr-resultado.jff")
    gr2 = read_gr("test-files/fatoracao/teste1-fatoracao.jff")
    gr2.write_to_file("test-files/resultados-testes/teste1-fatoracao-resultado.jff")
    gr3 = read_gr("test-files/fatoracao/teste2-fatoracao.jff")
    gr3.write_to_file("test-files/resultados-testes/teste2-fatoracao-resultado.jff")
