from trab_formais.io_utils.models.functions import read_af_file

BASE_ADDRESS = 'trab_formais/test-files'
af1 = 'D:/Users/bryan/Desktop/Formais/Trabalho 1/trabalho_formais/trab_formais/test-files/minimizacao/teste3-minimizacao.jff'
# af1 = read_af_file('/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/minimizacao/teste4-minimizacao.jff')
# af2 = read_af_file('/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/minimizacao/teste4-minimizacao.jff')
af2 = 'D:/Users/bryan/Desktop/Formais/Trabalho 1/trabalho_formais/trab_formais/test-files/minimizacao/teste3-minimizacao.jff'
# D:\Users\bryan\Desktop\Formais\Trabalho 1\trabalho_formais\trab_formais\test-files\minimizacao
# "D:\Users\bryan\Desktop\Formais\Trabalho 1\trabalho_formais\trab_formais\test.py"
af1 = read_af_file(af1)
print("resultado antes da minimizacao\n")
print(af1)
af1.minimize_af()


print("\n\nresultado dps da minimizaçaõ:\n")
print(af1)
