from io_utils.ine5421.functions import read_gr_file

PATH1 = ['/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/fatoracao/teste1-fatoracao.jff',
        '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/fatoracao/teste2-fatoracao.jff',
        '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/fatoracao/teste3-fatoracao.jff']

PATH2 = ['/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/eliminar-recursao/teste1-eliminacao-recursao-esquerda.jff',
        '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/eliminar-recursao/teste2-eliminacao-recursao-esquerda.jff',
        '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/eliminar-recursao/teste3-eliminacao-recursao-esquerda.jff']
print("_________________________________________________\nteste fatoracao\n")

i = 0
for p in PATH1:
    gr = read_gr_file(p)
    print(f'gr{i} antes:\n{gr}\n')
    gr.eliminar_n_determinismo()
    print(f'gr{i} depois:\n{gr}\n_________________________________________________')
    i = i + 1

print("teste recursao\n")

i = 0
for p in PATH2:
    gr = read_gr_file(p)
    print(f'gr{i} antes:\n{gr}\n')
    gr.eliminate_left_recursion()
    print(f'gr{i} depois:\n{gr}\n_________________________________________________')
    i = i + 1

print('fim :)')
