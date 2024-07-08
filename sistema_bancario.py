from random import randint

lista_de_usuarios = {}
contas = {}

class Cadastro:
    def __init__(self, nome, nascimento, cpf, endereco):
        self._nome = nome
        self._nascimento = nascimento
        self._cpf = cpf
        self._endereco = endereco

    @staticmethod
    def validar_cpf(cpf):  # Validação do CPF 11 dígitos sem caractere especial.
        return cpf.isdigit() and len(cpf) == 11
    
    @staticmethod
    def formatar_cpf(cpf):  # Formatar formato do CPF xxx.xxx.xxx-xx
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

    @staticmethod
    def cadastro_novo_usuario():
        while True:
            cpf = input('Informe seu número de CPF: ')
            if cpf in lista_de_usuarios:
                print('\n=============== CPF já cadastrado, verifique sua conta ===============\n')
                return Menu.exibir_menu()
            elif not Cadastro.validar_cpf(cpf):
                print('='*70)
                print('\nERRO! CPF inválido, certifique-se de que contém 11 dígitos numéricos e sem caracteres especiais.\n')
                print('='*70)
            else:
                break

        nome = input('Informe seu nome: ')
        nascimento = input('Informe sua data de nascimento: ')
        endereco = input('Informe seu endereço: ')
        
        novo_usuario = Cadastro(nome, nascimento, cpf, endereco)
        lista_de_usuarios[cpf] = novo_usuario
        
        print(f'Usuário {nome} cadastrado com sucesso!')

    @staticmethod
    def mostrar_usuarios():
        for cpf, usuario in lista_de_usuarios.items():
            print(f"CPF: {Cadastro.formatar_cpf(cpf)}, Nome: {usuario._nome}, Nascimento: {usuario._nascimento}, Endereço: {usuario._endereco}")


class CriarConta:
    @staticmethod
    def criar_conta_bancaria():
        print('=============== Criação Conta Bancária ===============\n')
        print('Agora vamos criar sua conta bancária')

        cpf = input('Informe seu CPF (somente números): ')
        conta_senha = input('Informe uma senha válida (mínimo 6 caracteres): ')

        if not Cadastro.validar_cpf(cpf):
            print('='*70)
            print('\nERRO! CPF inválido, certifique-se de que contém 11 dígitos numéricos e sem caracteres especiais.\n')
            print('='*70)
            return False
        elif cpf not in lista_de_usuarios:
            print('\n=============== Usuário não cadastrado, cadastre-se primeiro. ===============\n')
            return False
        elif any(conta['cpf'] == cpf for conta in contas.values()):
            print('\n=============== Usuário já possui conta. ===============\n')
            return False

        if len(conta_senha) < 6:
            print('\nERRO! A senha deve ter no mínimo 6 caracteres.\n')
            return False

        # Obter o nome do titular da conta do objeto de usuário na lista_de_usuarios
        nome_titular = lista_de_usuarios[cpf]._nome

        numero_conta = randint(1000, 9999)
        while numero_conta in contas:
            numero_conta = randint(1000, 9999)

        contas[numero_conta] = {
            'cpf': cpf,
            'conta_senha': conta_senha,
            'nome_titular': nome_titular,
            'saldo': 0.0,
            'depositos': [],
            'saques': []
        }
        print('\n============ Conta bancária criada com sucesso! ===============\n')
        print('-'*50)
        print(f'Conta: {numero_conta}\nAgência: 0001')
        print('-'*50)

        return True


class Menu:
    @staticmethod
    def exibir_menu():  # Menu de acesso ao sistema
        while True:
            print('=============== Bem vindo ao Banco Ebner ===============')
            print('\n[1] Novo por aqui? Crie sua conta.')
            print('[2] Já possui conta? Realize seu acesso.')
            print('[3] Exibir todos os usuários.')
            print('[4] Criar Conta Bancária.')
            print('[0] Sair.\n')
            print('========================================================')
            opcao_entrar = input()

            if opcao_entrar == '1':
                print('=============== Cadastro Novo Usuário ===============\n')
                print('Primeiro vamos cadastrar seu usuário.')
                Cadastro.cadastro_novo_usuario()
                
            elif opcao_entrar == '2':
                print('\n=============== Realize seu acesso ===============\n')
                acessar_sistema.acessar()

            elif opcao_entrar == '3':
                Cadastro.mostrar_usuarios()
            
            elif opcao_entrar == '4':
                CriarConta.criar_conta_bancaria()

            elif opcao_entrar == '0':
                print('Saindo do sistema...')
                break

            else:
                print('Opção inválida, por favor tente novamente.')


class acessar_sistema:
    @staticmethod
    def acessar():  # Função de acesso ao sistema
        print('Agência: 0001')
        conta_acesso = int(input('Conta: '))
        conta_senha_acesso = input('Senha: ')
        
        if conta_acesso in contas:
            if contas[conta_acesso]['conta_senha'] == conta_senha_acesso:
                print('Bem-vindo ao sistema')
                menu_operacoes.menu_operacoes_(conta_acesso)  # Passar o número da conta para o menu de operações
            else:
                print('Senha incorreta, acesso não autorizado!')
        else:
            print('Conta não encontrada, acesso não autorizado!')


class menu_operacoes:
    limite_saque = 3
    numero_saque = 0
    limite_diario = 500

    @staticmethod
    def menu_operacoes_(numero_conta):
        while True:
            print('=============== Menu de Operações ===============')
            print(f"Bem vindo {contas[numero_conta]['nome_titular']}")
            print("Agência: 0001")
            print(f"Conta: {numero_conta}")
            print('\n[d] Depósito')
            print('[s] Saque')
            print('[e] Extrato')
            print('[q] Sair')
            print('=================================================')
            opcao = input().strip().lower()
        
            if opcao == 'd':
                menu_operacoes.deposito(numero_conta)
            elif opcao == 's':
                menu_operacoes.saque(numero_conta)
            elif opcao == 'e':
                menu_operacoes.extrato(numero_conta)
            elif opcao == 'q':
                print('Obrigado por utilizar nossos serviços. Volte sempre!')
                break
            else:
                print('Opção inválida. Por favor, selecione uma opção válida.')

    @staticmethod
    def deposito(numero_conta):
        valor = float(input('Informe o valor para depósito: '))
        contas[numero_conta]['saldo'] += valor
        contas[numero_conta]['depositos'].append(valor)
        print(f'Depósito de R${valor:.2f} realizado com sucesso! Saldo atual: R${contas[numero_conta]["saldo"]:.2f}')

    @staticmethod
    def saque(numero_conta):
        valor = float(input('Informe o valor para saque: '))
        if valor > contas[numero_conta]['saldo']:
            print('Saldo insuficiente.')
        elif valor > menu_operacoes.limite_diario:
            print(f'Limite de saque diário excedido. Máximo permitido: R$ {menu_operacoes.limite_diario:.2f}.')
        elif menu_operacoes.numero_saque >= menu_operacoes.limite_saque:
            print('Você atingiu o limite diário de saques. Por favor, volte amanhã.')
        else:
            contas[numero_conta]['saldo'] -= valor
            contas[numero_conta]['saques'].append(valor)
            menu_operacoes.numero_saque += 1
            print(f'Saque de R${valor:.2f} realizado com sucesso! Saldo atual: R${contas[numero_conta]["saldo"]:.2f}')

    @staticmethod
    def extrato(numero_conta):
        saldo = contas[numero_conta]['saldo']
        print(f'Agência: 0001')
        print(f'Conta: {numero_conta}')
        print('\nDepósitos realizados:')
        for i, valor in enumerate(contas[numero_conta]['depositos'], 1):
            print(f'Depósito {i}: R$ {valor:.2f}')
        print('\nSaques realizados:')
        for i, valor in enumerate(contas[numero_conta]['saques'], 1):
            print(f'Saque {i}: R$ {valor:.2f}')
        print(f'\nSaldo atual da sua conta: R$ {saldo:.2f}\n')


# Exibindo o menu
Menu.exibir_menu()
