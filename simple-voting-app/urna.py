from funcao_urna import BancoDados, Cadidatos, Votos

input('Bem-vindo ao programa de urna.\n(PRESSIONE QUALQUER TECLA)\n')
input('A ordem de funcionamento será:\n1º Etapa: Cadastro dos candidatos\n2º Etapa: Inicio das votações\n3º Etapa: Contagem de votos.\n(PRESSIONE QUALQUER TECLA)\n')
input('Iniciando a 1º Etapa - Cadastro de candidato\n(PRESSIONE QUALQUER TECLA)\n')

BancoDados().criar_banco_dados()

"""Adição de candidatos"""
add_candidado = True
num_candidato = 1
Cadidatos().criar_nulo()
while add_candidado:
    print(f'Escreva os nome do {num_candidato}º candidato\n')
    nome_candidato = input('Digite o nome do candidato: ').split(':')[0]
    cpf = str(input('Digite o número do CPF do candidato: ').split(':')[0])
    numero_candidato = int(input('Digite o número do candidato: ').split(':')[0])

    payload = {
        'nome': nome_candidato,
        'cpf': cpf,
        'numero_candidato': numero_candidato
    }
    Cadidatos().add_candidados(payload)

    print(f'\nAdicionando o candidato: {nome_candidato.title()}\nCPF: {cpf}\nNúmero do candidato: {numero_candidato}')
    print('Deseja adicionar mais candidatos?')
    continuar = input('->').lower()
    add_candidado = False if 'n' in continuar else True
    num_candidato += 1

print('Etapa 1ª Etapa finalizada com SUCESSO!')
input('\nIniciando a 2º Etapa - Inicio das votações\n(PRESSIONE QUALQUER TECLA)\n')

"""Votação"""
candidatos_adicionados = Cadidatos().vizualizar_dados()
continuacao_votacao = True

while continuacao_votacao:
    print(f'\t\tEscolha um dos candidatos: {candidatos_adicionados}\n')
    numero_candidato = int(input('Digite o número do candidato: ').split(':')[0])
    adicao_voto = Votos().add_votos(numero_candidato)

    print('Deseja continuar a votação?')
    continuar = input('->').lower()
    continuacao_votacao = False if 'n' in continuar else True

print('Etapa 2ª Etapa finalizada com SUCESSO!')
input('\nIniciando a 3º Etapa - Contagem de votos\n(PRESSIONE QUALQUER TECLA)\n')

"""Contagem de Votos"""
resultado = Votos().contagem()
print(f'Resultado da Contagem de votos\nResultado:{resultado}')

print('Deseja a extratificação dos votos?')
extratificar = input('->').lower()
extratificacao = False if 'n' in extratificar else True

if extratificacao:
    arquivo_extratificacao = Votos().extratificacao_votos()
    print(f'Arquivo de Extratificação:\n{arquivo_extratificacao}')

print('\nFim do programa de Eleição.')