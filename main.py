import getpass
import sys
import os
import time
from datetime import datetime


def menu(opcao):
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
    try:
        arquivo = open('professores.txt', 'r')
        arquivo.close()
    except:
        print('Nenhum professor cadastrado!')
        input('\nPressione enter para voltar ao Menu\n>> ')
        main()

    os.system('cls')
    senha = input('Insira senha: ')  # getpass

    arquivo = open('professores.txt', 'r')
    for linha in arquivo:
        if linha[:-1] == senha:
            matricula = arquivo.readline()
            arquivo.close()
            menuAcesso(senha, matricula)

    arquivo.close()

    print('Senha incorreta')
    time.sleep(2)
    main()


def regPatrimonio():
    print('-' * 10 + 'REG PATRIMÔNIO' + '-' * 10)

    try:
        arquivo = open('patrimonio.txt', 'r')
        num_patrimonio = int(arquivo.readlines()[-1]) + 1
        arquivo.close()
    except:
        num_patrimonio = 1

    arquivo = open('patrimonio.txt', 'a')
    
    descricao = input('Descrição do patrimônio: ')
    arquivo.write(descricao + '\n')
    arquivo.write(str(num_patrimonio) + '\n')
    
    arquivo.close()

    print('\n' + 'Patrimônio registrado com sucesso!' + '\n')

    print('Registrar novamente [1]\nVoltar para o Menu [2]')
    opcao = lerOpcao(input('>> '))
    if opcao == '1':
        return regPatrimonio()

    return main()


def regProfessor():
    print('-' * 10 + 'REG PROFESSOR' + '-' * 10)

    arquivo = open('professores.txt', 'a')

    nome = input('Nome do professor: ')
    senha = input('Senha do professor: ')   # getpass.getpass() para não mostrar a senha
    senha_cripto = criptografarSenha(senha)
    matricula = input('Matrícula do professor: ')
    arquivo.write(nome + '\n')
    arquivo.write(senha_cripto + '\n')
    arquivo.write(matricula + '\n')

    arquivo.close()

    print('\n' + 'Professor registrado com sucesso!' + '\n')

    print('Registrar novamente [1]\nVoltar para o Menu [2]')
    opcao = lerOpcao(input('>> '))
    if opcao == '1':
        return regProfessor()

    return main()


def regAcesso(matricula, numero_patrimonio, tipo):
    arquivo = open('acesso.txt', 'a')
    arquivo.write(matricula)
    arquivo.write(numero_patrimonio + '\n')
    arquivo.write(tipo + '\n')

    data = datetime.now()
    dia = str(data.day)
    mes = str(data.month)
    ano = str(data.year)
    hora = str(data.hour)
    min = str(data.minute)
    sec = str(data.second)

    arquivo.write(dia + '/' + mes + '/' + ano + '\n')
    arquivo.write(hora + '/' + min + '/' + sec + '\n')

    arquivo.close()


def menuAcesso(senha, matricula):
    def retirarPatrimonio(matricula):
        os.system('cls')
        print('-' * 10 + 'RETIRAR PATRIMÔNIO' + '-' * 10)
        numero_patrimonio = input('Insira o número do patrimônio para retirar: ')
        # Função que verifica o numero de patrimonio na lista de patrimônions cadastrados
        tipo = 'retirada'
        regAcesso(matricula, numero_patrimonio, tipo)

        print('\n' + 'Patrimônio retirado com sucesso!' + '\n')

        print('Retirar outro [1]\nVoltar para o Menu de Acesso [2]')
        opcao = lerOpcao(input('>> '))
        if opcao == '1':
            return retirarPatrimonio(matricula)

        return menuAcesso(senha, matricula)

    def devolucaoPatrimonio(matricula):
        os.system('cls')
        print('-' * 10 + 'DEVOLUÇÃO PATRIMÔNIO' + '-' * 10)
        numero_patrimonio = input('Insira o número do patrimônio para devolução: ')
        tipo = 'devolução'
        regAcesso(matricula, numero_patrimonio, tipo)

        print('\n' + 'Patrimônio retornado com sucesso!' + '\n')

        print('Retornar outro patrimônio [1]\nVoltar para o Menu de Acesso [2]')
        opcao = lerOpcao(input('>> '))
        if opcao == '1':
            return devolucaoPatrimonio(matricula)

        return menuAcesso(senha, matricula)

    os.system('cls')

    print('-' * 12 + 'REG ACESSO' + '-' * 12)
    print('''Retirar patrimônio [1]
Devolução patrimônio [2]
Voltar para o Menu [3]''')
    opcao = input('>> ')
    while opcao not in ['1', '2', '3']:
        print('Opção inválida!')
        opcao = input('>> ')

    if opcao == '1':
        retirarPatrimonio(matricula)
    elif opcao == '2':
        devolucaoPatrimonio(matricula)
    else:
        main()


def criptografarSenha(senha):
    senha_cripto = senha

    return senha_cripto


def menuHistAcesso():
    def listaPatrimonioDispo():
        pass

    def listaPatrimonioDevolucao():
        pass

    def historicoRetirada():
        pass

    def patrimonioMaisUti():
        pass

    pass


def lerOpcao(opcao):
    while opcao not in ['1', '2']:
        print('Opção inválida!')
        opcao = input('>> ')

    return opcao


def main():
    opcao = '0'
    while opcao != '4':
        os.system('cls')

        print('-'*20 + 'MENU' + '-'*20)
        print('''Registro de Patrimônios [1]
Registro de Professores [2]
Registro de acesso aos Patrimônios [3]
Histórico de Acesso [4]
Sair [5]
>>''', end=' ')
        opcao = input()
        while opcao not in ['1', '2', '3', '4', '5']:
            print('Opção inválida!')
            opcao = input('>> ')

        os.system('cls')

        menu(int(opcao))


main()
