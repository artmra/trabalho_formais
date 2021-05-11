from io_utils.ine5421.functions import read_gr_file

PATH = '/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/fatoracao/teste2-fatoracao.jff'

gr = read_gr_file(PATH)

gr.eliminar_n_determinismo()
