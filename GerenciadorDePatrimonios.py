import getpass
import sys
import os
from operator import itemgetter
from datetime import datetime, date


CARACTERES = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'


def menu(opcao):
    # Gerencia as opções

    if opcao == 1:
        regPatrimonio()
    elif opcao == 2:
        regProfessor()
    elif opcao == 3:
        verificaSenha()
    elif opcao == 4:
        menuHistAcesso()
    else:
        sys.exit()


def verificaSenha():
    # Verifica se a senha está correta, caso esteja chama função menuacesso caso não mostra senha incorreta

    try:
        arquivo = open('professores.txt', 'r')
        arquivo.close()
    except:
        print('Nenhum professor cadastrado!')
        input('\nPressione enter para voltar ao Menu\n>> ')
        main()

    os.system('cls')
    senha = getpass.getpass('Insira senha: ').strip()  # getpass
    senha_cripto = ''
    for caractere in senha:
        if caractere in CARACTERES:
            index = CARACTERES.find(caractere) + 5
            if index >= 62:
                index -= 62
            senha_cripto += CARACTERES[index]
    arquivo = open('professores.txt', 'r')
    lista = arquivo.readlines()

    if senha_cripto+'\n' in lista:
        pos = lista.index(senha_cripto+'\n')
        nomeProf = lista[pos-1]
        matricula = lista[pos+1]
        arquivo.close()

        menuAcesso(senha, nomeProf, matricula)

    arquivo.close()

    print('Senha incorreta')
    input('\nPressione enter para voltar ao Menu\n>> ')
    main()


def verificaPatrimonioDispo(n_patrimonio):
    # Verifica se o patrimonio que se quer retirar ou devolver está disponível

    try:
        arquivo = open('PatrimoniosDisponiveis.txt', 'r')
        arquivo.close()
    except:
        print('\nNenhum patrimônio cadastrado')
        input('Pressione enter para voltar ao menu\n>>')
        main()

    arquivo = open('PatrimoniosDisponiveis.txt', 'r')
    lista = arquivo.readlines()
    if n_patrimonio+'\n' in lista:
        pos = lista.index(n_patrimonio+'\n') - 1
        descricao = lista[pos]
        arquivo.close()
        return [True, descricao]

    arquivo.close()

    return [False, '']


def verificaProfessor(matricula):
    # Verifica se a matrícula ja foi cadastrada em outro professor

    arquivo = open('professores.txt', 'r')
    for linha in arquivo:
        if linha[:-1] == matricula:
            return True

    return False


def regPatrimonio():
    # Faz o registro de patrimônios

    print('-' * 30 + 'REG PATRIMÔNIO' + '-' * 30)

    try:
        arquivo = open('patrimonio.txt', 'r')
        num_patrimonio = int(arquivo.readlines()[-1]) + 1
        arquivo.close()
    except:
        num_patrimonio = 1

    arquivo = open('patrimonio.txt', 'a')
    
    descricao = input('Descrição do patrimônio: ').strip()
    arquivo.write(descricao + '\n')
    arquivo.write(str(num_patrimonio) + '\n')
    
    arquivo.close()

    # Chama função que registra o patrimonio adicionado aos Patrimonio Disponíveis
    regPatrimonioDispo(num_patrimonio)

    print('\n' + 'Patrimônio registrado com sucesso!' + '\n')

    print('Registrar novo Patrimônio [1]\nVoltar para o Menu [2]')
    opcao = lerOpcao(input('>> '))
    if opcao == '1':
        return regPatrimonio()

    return main()


def regProfessor():
    # Faz o registro de professores

    print('-' * 30 + 'REG PROFESSOR' + '-' * 30)

    nome = input('Nome do professor: ').strip()
    # getpass.getpass() para não mostrar a senha
    senha = getpass.getpass('Senha do professor (apenas letras e números): ').strip()
    senha_cripto = criptografarSenha(senha) # Criptografa senha (CIFRA DE CÉSAR)
    matricula = input('Matrícula do professor: ').strip()

    arquivo = open('professores.txt', 'a')

    isProfCadastrado = verificaProfessor(matricula)  # Verifica se a matricula digitada ja foi cadastrada
    if isProfCadastrado:
        print('\nProfessor ja cadastrado\n')
        return regProfessor()

    arquivo.write(nome + '\n')
    arquivo.write(senha_cripto + '\n')
    arquivo.write(matricula + '\n')

    arquivo.close()

    print('\n' + 'Professor registrado com sucesso!' + '\n')

    print('Registrar novo Professor [1]\nVoltar para o Menu [2]')
    opcao = lerOpcao(input('>> '))
    if opcao == '1':
        return regProfessor()

    return main()


def regAcesso(nomeProf, matricula, numero_patrimonio, tipo):
    # Escreve no arquivo acesso.txt com todas as informações da movimentação que foi efetuada

    arquivo = open('acesso.txt', 'a')
    arquivo.write(nomeProf)
    arquivo.write(matricula)
    arquivo.write(numero_patrimonio + '\n')
    arquivo.write(tipo + '\n')

    data = datetime.now()
    dia = str(data.day)
    if len(dia) < 2:
        dia = '0' + dia
    mes = str(data.month)
    if len(mes) < 2:
        mes = '0' + mes
    ano = str(data.year)
    hora = str(data.hour)
    if len(hora) < 2:
        hora = '0' + hora
    min = str(data.minute)
    if len(min) < 2:
        min = '0' + min
    sec = str(data.second)
    if len(sec) < 2:
        sec = '0' + sec

    arquivo.write(dia + '/' + mes + '/' + ano + '\n')
    arquivo.write(hora + ':' + min + ':' + sec + '\n')

    arquivo.close()


def menuAcesso(senha, nomeProf, matricula):
    # Menu de acesso com opções de retirar um patrimônio ou de devolução

    def retirarPatrimonio():
        os.system('cls')
        print('-' * 30 + 'RETIRAR PATRIMÔNIO' + '-' * 30)
        numero_patrimonio = input('Insira o número do patrimônio para retirar: ').strip()

        # Função que verifica o numero de patrimonio existe na lista de patrimônions disponíveis (verificaPatriDispo)
        valores_de_retorno = verificaPatrimonioDispo(numero_patrimonio)

        # Valor True ou False para verificar se o patrimonio pode ser retirado ou nao
        verificaDisponibilidade = valores_de_retorno[0]

        # Descrição do patrimônio que vai ser retirado
        descricao = valores_de_retorno[1]

        if verificaDisponibilidade:
            tipo = 'retirada'

            # Função que escreve em acesso.txt
            regAcesso(nomeProf, matricula, numero_patrimonio, tipo)

            # Função que registra os patrimônios retirados
            regPatrimonioRetirados(descricao, numero_patrimonio, nomeProf, matricula)

            # Função que remove o patrimônio que agora foi retirado da lista PatrimonioDisponiveis
            atualizaPatrimonioDispo(numero_patrimonio)

        else:
            print('\nPatrimônio não consta na lista de Disponíveis')
            input('Pressione enter para voltar ao Menu\n>> ')
            main()

        print('\n' + 'Patrimônio retirado com sucesso!' + '\n')

        print('Retirar outro [1]\nVoltar para o Menu de Acesso [2]')
        opcao = lerOpcao(input('>> '))
        if opcao == '1':
            return retirarPatrimonio()

        return menuAcesso(senha, nomeProf, matricula)

    def devolucaoPatrimonio():
        os.system('cls')
        print('-' * 30 + 'DEVOLUÇÃO PATRIMÔNIO' + '-' * 30)
        numero_patrimonio = input('Insira o número do patrimônio para devolução: ').strip()

        # Função que verifica o numero de patrimonio existe na lista de patrimônions disponíveis (verificaPatriDispo)
        valores_de_retorno = verificaPatrimonioDispo(numero_patrimonio)

        # Valor True ou False para verificar se o patrimonio pode ser retirado ou nao
        verificaDisponibilidade = valores_de_retorno[0]

        if not verificaDisponibilidade:
            tipo = 'devolução'

            # Função que escreve em acesso.txt
            regAcesso(nomeProf, matricula, numero_patrimonio, tipo)

            # Função que registra os patrimônios disponíveis
            regPatrimonioDispo(numero_patrimonio)

            # Função que remove o patrimônio que agora está disponivel da lista PatrimonioRetirados
            atualizaPatrimoniosRetirados(numero_patrimonio)

        else:
            print('\nEsse Patrimônio não foi retirado')
            input('Pressione enter para voltar ao Menu\n>> ')
            main()

        print('\n' + 'Patrimônio retornado com sucesso!' + '\n')

        print('Retornar outro patrimônio [1]\nVoltar para o Menu de Acesso [2]')
        opcao = lerOpcao(input('>> '))
        if opcao == '1':
            return devolucaoPatrimonio()

        return menuAcesso(senha, nomeProf, matricula)

    # Executa quando do menu de acesso é chamado
    os.system('cls')

    print('-' * 39 + 'REG ACESSO' + '-' * 30)
    print('''Retirar patrimônio [1]
Devolução patrimônio [2]
Voltar para o Menu [3]''')
    opcao = input('>> ')
    while opcao not in ['1', '2', '3']:
        print('Opção inválida!')
        opcao = input('>> ')

    if opcao == '1':
        retirarPatrimonio()
    elif opcao == '2':
        devolucaoPatrimonio()
    else:
        main()


def criptografarSenha(senha):
    # Criptografia da senha. (CIFRA DE CÉSAR)

    for char in senha:
        if char not in CARACTERES:
            print('\nCaractere inválido.')
            input('Pressione enter para voltar ao menu\n>>')
            main()

    if len(senha) < 4:
        print('\nSenha necessita pelo menos 4 caracteres')
        input('Pressione enter para voltar ao menu\n>>')
        main()

    senha_cripto = ''

    for caractere in senha:
        if caractere in CARACTERES:
            index = CARACTERES.find(caractere) + 5
            if index >= 62:
                index -= 62
            senha_cripto += CARACTERES[index]

    return senha_cripto


def regPatrimonioRetirados(descricao, numero_patrimonio, nomeProf, matricula):
    # Registra os patrimônios que foram retirados no arquivo PatrimoniosRetirados.txt

    arquivo = open('PatrimoniosRetirados.txt', 'a')
    arquivo.write(descricao)
    arquivo.write(numero_patrimonio + '\n')
    arquivo.write(nomeProf)
    arquivo.write(matricula)

    arquivo.close()

    atualizaPatrimonioMaisUti(descricao, numero_patrimonio)


def atualizaPatrimoniosRetirados(numero_patrimonio):
    # Remove da lista PatrimoniosRetirados.txt o patrimônio que foi devolvido

    arquivo = open('PatrimoniosRetirados.txt', 'r')
    lista = arquivo.readlines()
    arquivo.close()

    arquivo = open('PatrimoniosRetirados.txt', 'w')
    pos = lista.index(numero_patrimonio + '\n')
    lista.pop(pos)
    lista.pop(pos)
    lista.pop(pos)
    lista.pop(pos - 1)
    arquivo.writelines(lista)
    arquivo.close()


def regPatrimonioDispo(numero_patrimonio):
    # Registra os patrimônios disponíveis sempre que um patrimônio é devolvido ou um novo é registrado

    arq = open('patrimonio.txt', 'r')

    lista = arq.readlines()
    pos = lista.index(str(numero_patrimonio) + '\n')
    descricao = lista[pos-1]

    arq.close()

    arquivo = open('PatrimoniosDisponiveis.txt', 'a')
    arquivo.write(descricao)
    arquivo.write(str(numero_patrimonio) + '\n')
    arquivo.close()


def atualizaPatrimonioDispo(numero_patrimonio):
    # Remove da lista PatrimoniosDisponiveis.txt o patrimônio que foi retirado

    arquivo = open('PatrimoniosDisponiveis.txt', 'r')
    lista = arquivo.readlines()
    arquivo.close()

    arquivo = open('PatrimoniosDisponiveis.txt', 'w')
    pos = lista.index(numero_patrimonio + '\n') - 1
    lista.pop(pos)
    lista.pop(pos)
    arquivo.writelines(lista)
    arquivo.close()


def atualizaPatrimonioMaisUti(descricao, n_patrimonio):
    #  Atualiza a lista de Patrimonios Mais Utilizados

    data = datetime.now()
    dia = str(data.day)
    if len(dia) < 2:
        dia = '0' + dia
    mes = str(data.month)
    if len(mes) < 2:
        mes = '0' + mes
    ano = str(data.year)

    arquivo = open('PatrimoniosMaisUti.txt', 'a')

    arquivo.write(dia + '/' + mes + '/' + ano + '\n')
    arquivo.write(descricao)
    arquivo.write(str(n_patrimonio) + '\n')

    arquivo.close()


def retornaDicPatriMaisUti(dias):
    # Cria uma lista com dicionários que contêm as informações dos patrimônios em ordem de utilizações

    try:
        arquivo = open('PatrimoniosMaisUti.txt', 'r')
        arquivo.close()
    except:
        print('\nNenhum patrimônio utilizado até o momento\n')
        input('Pressione enter para voltar ao Menu\n>>')
        menuHistAcesso()

    data_atual = date.today()
    arquivo = open('PatrimoniosMaisUti.txt', 'r')

    lista = arquivo.readlines()

    arquivo.seek(0, 0)
    c = 0
    #  Percorre a lista de PatrimoniosMaisUtilizados e retira os que foram utilizados fora da data limite
    for linha in arquivo.readlines():
        if c % 3 == 0:
            dia = int(linha[:2])
            mes = int(linha[3:5])
            ano = int(linha[6:10])
            delta = (date(year=ano, month=mes, day=dia) - data_atual).days
            if abs(delta) > dias:
                lista.pop(c)
                lista.pop(c)
                lista.pop(c)
                c -= 3

        c += 1

    arquivo.close()

    # Cria lista de posições dos numeros de patrimônios na lista
    posicoes = [2]
    for cont in range(int(len(lista) / 3) - 1):
        posicoes.append(posicoes[cont] + 3)

    listaMaisUti = []
    # Cria lista com as informações e atualiza um contador
    for posicao in posicoes:
        cont = 0
        for item in lista:
            if lista[posicao] == item:
                cont += 1
            if lista[posicao] not in listaMaisUti:
                listaMaisUti.append(lista[posicao - 1])
                listaMaisUti.append(lista[posicao])
                listaMaisUti.append(cont)
            else:
                pos = listaMaisUti.index(lista[posicao])
                listaMaisUti[pos + 1] = cont

    lista = []
    for c in range(int(len(listaMaisUti) / 3)):
        cont = 0
        lista.append({'descricao': listaMaisUti[cont][:-1], 'num_patrimonio': listaMaisUti[cont + 1][:-1],
                      'contador': listaMaisUti[cont + 2]})
        if len(listaMaisUti) != 0:
            listaMaisUti.pop(cont)
            listaMaisUti.pop(cont)
            listaMaisUti.pop(cont)

    lista = sorted(lista, key=itemgetter('contador'), reverse=True)

    return lista


def menuHistAcesso():
    # Mostra as listagens

    def listaPatrimonioDispo():
        # Listagem dos patrimônios disponíveis

        os.system('cls')
        print('-'*30 + 'PATRIMÔNIOS DISPONÍVEIS' + '-'*30, end='\n\n')
        try:
            arquivo = open('PatrimoniosDisponiveis.txt', 'r')
            arquivo.close()
        except:
            print('Nenhum Patrimônio disponível!')
            input('Pressione enter para voltar\n>>')
            menuHistAcesso()

        arquivo = open('PatrimoniosDisponiveis.txt', 'r')

        lista = arquivo.readlines()
        arquivo.seek(0, 0)

        for x in range(int(len(lista) / 2)):
            print('Descrição>{:.^40}NºPatrimônio>{:.>20}'.format(arquivo.readline()[:-1], arquivo.readline()))

        arquivo.close()

        input('\n\nPressione enter para voltar ao menu\n>>')
        menuHistAcesso()

    def listaPatrimonioRetirados():
        # Listagem dos patrimônios que foram retirados

        os.system('cls')
        print('-'*30 + 'PATRIMÔNIOS RETIRADOS' + '-'*30, end='\n\n')

        try:
            arquivo = open('PatrimoniosRetirados.txt', 'r')
            arquivo.close()
        except:
            print('Nenhum patrimônio retirado!')
            input('Pressione enter para voltar\n>>')
            menuHistAcesso()

        arquivo = open('PatrimoniosRetirados.txt', 'r')

        lista = arquivo.readlines()
        arquivo.seek(0, 0)

        for x in range(int(len(lista) / 4)):
            print('Descrição>{:.^40}NºPatrimônio>{:.>20}'.format(arquivo.readline()[:-1], arquivo.readline()))
            print('Professor>{:.^40}NºMatrícula>{:.>21}'.format(arquivo.readline()[:-1], arquivo.readline()))
            print('                                        ||')
        arquivo.close()

        input('\n\nPressione enter para voltar ao menu\n>>')
        menuHistAcesso()


    def patrimonioMaisUti():
        # Faz a listagem dos patrimonios mais utilizados em ordem

        os.system('cls')
        print('-' * 30 + 'PATRIMÔNIOS MAIS UTILIZADOS' + '-' * 30, end='\n\n')

        dias = input('Insira a quantidade de dias: ').strip()
        while not dias.isnumeric():
            print('Valor inválido')
            dias = input('Insira a quantidade de dias: ').strip()

        dias = int(dias)

        # Chama função que retorna uma lista com dicionários contendo as informações prontas para serem disponibilizadas
        lista = retornaDicPatriMaisUti(dias)

        os.system('cls')
        print('-' * 30 + 'PATRIMÔNIOS MAIS UTILIZADOS' + '-' * 30, end='\n\n')

        for x in range(len(lista)):
            dicionario = lista[x]
            print('Descrição>{:.^40}NºPatrimônio>{:.>20}'.format(dicionario['descricao'], dicionario['num_patrimonio']))
            print('                      Utilizado {} vezes nos últimos {} dias'.format(dicionario['contador'], dias))
            print('                                        ||')

        input('\nPressione enter para voltar ao Menu\n>>')
        main()

    def listaMovimentacao():
        # Listagem de toda movimentação realizada

        os.system('cls')
        print('-' * 30 + 'LISTAGEM DA MOVIMENTAÇÃO' + '-' * 30)
        print('\n\n')
        try:
            arquivo = open('acesso.txt', 'r')
            arquivo.close()
        except:
            print('Nenhuma movimentação realizada!')
            input('Pressione enter para voltar\n>>')
            menuHistAcesso()

        arquivo = open('acesso.txt', 'r')

        lista = arquivo.readlines()
        arquivo.seek(0, 0)

        x = 0
        for _ in range(int(len(lista) / 6)):
            print('Professor>{:.^30}NºMatrícula>{:.>30}'.format(lista[x][:-1], lista[x+1][:-1]))
            print('NºPatrimônio>{:.^27}Movimentação>{:.>30}'.format(lista[x+2][:-1], lista[x+3][:-1]))
            print('Data>{:.^38}Hora>{:.>34}'.format(lista[x + 4][:-1], lista[x + 5][:-1]))
            print()
            x += 6

        arquivo.close()

        input('\n\nPressione enter para voltar ao menu\n>>')
        menuHistAcesso()

    # Executa quando o menu do historico de acesso é chamado

    os.system('cls')
    print('-' * 30 + 'MENU HISTÓRICO' + '-' * 30)
    print('''Listagem dos Patrimônios aguardando devolução [1]
Listagem dos Patrimõnios disponíveis para retirada [2]
Listagem dos Patrimônios mais utilizados [3]
Listagem da Movimentação [4]
Voltar para o Menu [5]
>>''', end=' ')

    opcao = input()
    while opcao not in ['1', '2', '3', '4', '5']:
        print('Opção inválida!')
        opcao = input('>> ')

    if opcao == '1':
        listaPatrimonioRetirados()
    elif opcao == '2':
        listaPatrimonioDispo()
    elif opcao == '3':
        patrimonioMaisUti()
    elif opcao == '4':
        listaMovimentacao()

    main()


def lerOpcao(opcao):
    # Função utilizada nos registros quando se quer validar um entrada de usuário entre cadastrar novamente ou voltar
    # ao menu anterior

    while opcao not in ['1', '2']:
        print('Opção inválida!')
        opcao = input('>> ')

    return opcao


def main():
    # Painel de Opções

    os.system('cls')

    print('-'*30 + 'MENU' + '-'*30)
    print('''Registro de Patrimônios [1]
Registro de Professores [2]
Acesso aos Patrimônios [3]
Histórico de Acesso [4]
Sair [5]
>>''', end=' ')
    opcao = input().strip()
    while opcao not in ['1', '2', '3', '4', '5']:
        print('Opção inválida!')
        opcao = input('>> ').strip()

    os.system('cls')

    menu(int(opcao))


main()
