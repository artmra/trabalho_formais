## Trabalho da disciplina INE5421

Repositório do trabalho de formais.

## Instalando requerimentos
Dentro do repositório do projeto execute o seguinte(é necessário ter o python3 e pip3 instalados):
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Para desativar o ambiente virtual:
```
deactivate
```

## Rodar localmente
Verifique se a pasta ```media``` está localizada dentro de ```trab_formais/```; caso não, crie uma; em seguida ative o 
virtual env
```
source venv/bin/activate
```
Em seguida vá para o destino do arquivo manage.py e rode o seguinte comando:
```
python manage.py runserver
```
Caso seja necessário fazer migrações basta usar:
```
python manage.py migrate
```
O endereço do site se encontra em: [localhost:8000](http://localhost:8000/)

## Formato de Arquivos
Arquivos testes em: \
/trab_formais/ine5421/test-files
### Automato Finito Exemplo:
```
5
0
1,2
a,b
0,a,1-2-3
0,b,2
1,a,1
1,b,3
2,a,4
2,b,2
3,a,1
3,b,3
4,a,4
4,b,2
```
**Primeira Linha** : Número de Estados \
**Segunda Linha** : Estado Inicial \
**Terceira Linha** : Estado(s) de Aceitação \
**Demais Linhas** : Transições (Estado Origem, Letra Pertencente ao Alfabeto, Estado(s) Destino separados por hífen)

### Grámatica Regular Exemplo:
```
S
S,A
a,b,&
S -> aA | a | &
A -> bA | a
```
**Primeira Linha** : Estado Inicial \
**Segunda Linha** : Não terminais separados por vírgulas \
**Terceira Linha** : Terminais separados por vírgulas \
**Demais Linhas** : Regras (Cabeça da produção separador por '->' e corpo da produção separador por '|') \
Epsilon é representado como '&'
