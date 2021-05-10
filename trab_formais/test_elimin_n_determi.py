from io_utils.ine5421.functions import read_gr_file

PATH = '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/fatoracao/teste1-fatoracao.jff'

gr = read_gr_file(PATH)
print(gr)

gr.eliminar_n_determinismo_direto()
gr.eliminate_left_recursion()

print(f'\n\n{gr}')
