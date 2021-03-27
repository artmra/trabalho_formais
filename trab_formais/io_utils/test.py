from trab_formais.io_utils.io_utils.functions import read_af_file

BASE_PATH_1 = '/home/evaristo/Faculdade/lingFormais/trabalho_formais/trab_formais/test-files/test-files/determinizacao/teste'
BASE_PATH_2 = '-determinizacao.jff'

af1 = read_af_file(BASE_PATH_1+'1'+BASE_PATH_2)
# af2 = read_af_file(BASE_PATH_1+'2'+BASE_PATH_2)
# af1.determinize()
print(f'af original:\n\n{af1.string_in_file_format()}')
af1.determinize()
print(f'\n\naf determinizado:\n\n{af1.string_in_file_format()}')
print('\nfim')

