from io_utils.ine5421.functions import read_gr_file

PATH = '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/eliminar-recursao/teste3-eliminacao-recursao-esquerda.jff'

gr = read_gr_file(PATH)
print(gr)

gr.eliminate_left_recursion()

print(f'\n\n{gr}')
