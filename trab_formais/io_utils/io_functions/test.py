from io_utils.io_functions.functions import read_af_file

# BASE_PATH_1 = '/home/evaristo/Faculdade/lingFormais/trabalho_formais/trab_formais/test-files/test-files/determinizacao/teste'
# BASE_PATH_1 = 'D:/Users/bryan/Desktop/Formais/TRABALHO/trabalho_formais/trab_formais/test-files/test-files/minimizacao/teste3-minimizacao.jff'
BASE_PATH_1 = 'D:/Users/bryan/Desktop/Formais/TRABALHO/trabalho_formais/trab_formais/test-files/test-files/minimizacao/teste4-minimizacao.jff'
# BASE_PATH_2 = '-determinizacao.jff'

# af1 = read_af_file(BASE_PATH_1+'1'+BASE_PATH_2)
af1 = read_af_file(BASE_PATH_1)
# af2 = read_af_file(BASE_PATH_1+'2'+BASE_PATH_2)
# af1.determinize()
# print(f'af original:\n\n{af1.string_in_file_format()}')
af1.minimize_af()
# print(f'\n\naf minimizado:\n\n{af1.string_in_file_format()}')
# print('\nfim')

