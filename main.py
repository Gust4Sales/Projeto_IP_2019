import getpass
import os

def menu(opcao):
    if opcao == 1:
        regPatrimonio()
    elif opcao == 2:
        regProfessor()
    elif opcao == 3:
        acessoPatrimonio()
    if opcao == 4:
        return


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


def criptografarSenha(senha):
    senha_cripto = senha

    return senha_cripto


def acessoPatrimonio():
    def listaPatrimonioDispo():
        pass

    def recebimentoPatrimonio():
        pass

    def devolucaoPatrimonio():
        pass

    def listaPatrimonioDevolucao():
        pass

    def historicoRetirada():
        pass

    def patrimonioMaisUti():
        pass

    pass


opcao = '0'
while opcao != '4':
    os.system('cls')

    print('-'*20 + 'MENU' + '-'*20)
    print('''Registro de Patrimônios [1]
Registro de Professores [2]
Registro de acesso aos Patrimônios [3]
Sair [4]
>>''', end=' ')
    opcao = input()
    while opcao not in ['1', '2', '3', '4']:
        print('Opção inválida!')
        opcao = input('>> ')
    os.system('cls')

    menu(int(opcao))

