from ine5421.functions import read_af_file
import time

BASE_ADDRESS = 'trab_formais/test-files'

af1 = read_af_file('/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/minimizacao/teste4-minimizacao.jff')
af2 = read_af_file('/home/evaristo/Faculdade/ling_formais/trabalho_formais/trab_formais/test-files/minimizacao/teste4-minimizacao.jff')
print("resultado antes da minimizacao")
print(af1)
in1 = time.time()
af1.minimize_af_1()
fi1 = time.time()
in2 = time.time()
af2.minimize_af_2()
fi2 = time.time()

print("\n\nresultado usando metodo 1\n")
print(af1)
print("\n\nresultado usando metodo 2\n")
print(af2)
