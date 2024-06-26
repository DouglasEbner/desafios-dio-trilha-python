# Criação de modelo de sistema Bancário
from random import randint

# Dicionários de usuários e contas
usuarios = {}
contas = {}

def validar_cpf(cpf): # Validação do CPF 11 digitos sem caractere especial. (método string)
    return cpf.isdigit() and len(cpf) == 11

def formatar_cpf(cpf): # Formatar formato do CPF xxx.xxx.xxx-xx
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def adicionar_usuario(): # Função de cadastro de novo usuário.
    cpf = input('Informe seu número de CPF (somente números): \n')
    if cpf in usuarios:
        print('=============== CPF já cadastrado, verifique sua conta =============== ')
        return False
    elif not validar_cpf(cpf):
        print('='*70)
        print('\nERRO! CPF inválido, certifique-se de que contém 11 dígitos numéricos e sem caracteres especiais.\n')
        print('='*70)
        return False
    nome = input('Informe seu nome completo: \n')
    nascimento = input('Informe sua data de nascimento: \n')
    endereco = input('Informe seu endereço (Logradouro - Nº - cidade - estado): \n')

    if not validar_cpf(cpf):
        print('='*70)
        print('\nERRO! CPF inválido, certifique-se de que contém 11 dígitos numéricos e sem caracteres especiais.\n')
        print('='*70)
        return False

    usuarios[cpf] = {
        'nome': nome,
        'nascimento': nascimento,
        'cpf': formatar_cpf(cpf),
        'endereco': endereco
    }
    print('\n=============== Usuário cadastrado com sucesso! ===============\n')
    return True

def criar_conta_bancaria():
    print('=============== Criação Conta Bancária ===============\n')
    print('Agora vamos criar sua conta bancária')
    cpf = input('Informe seu CPF (somente números): \n')
    conta_senha = input('Informe uma senha válida (mínimo 6 caracteres): \n')

    if not validar_cpf(cpf):
        print('='*70)
        print('\nERRO! CPF inválido, certifique-se de que contém 11 dígitos numéricos e sem caracteres especiais.\n')
        print('='*70)
        return False
    elif cpf not in usuarios:
        print('\n=============== Usuário não cadastrado, cadastre-se primeiro. ===============\n')
        return False
    elif any(conta['cpf'] == cpf for conta in contas.values()):
        print('\n=============== Usuário já possui conta. ===============\n')
        return False

    if len(conta_senha) < 6:
        print('\n ERRO! A senha deve ter no mínimo 6 caracteres.\n')
        return False

    numero_conta = randint(1000, 9999)
    while numero_conta in contas:
        numero_conta = randint(1000, 9999)

    contas[numero_conta] = {
        'cpf': cpf,
        'conta_senha': conta_senha,
        'saldo': 0.0
    }
    print('\n============ Conta bancária criada com sucesso! ===============\n')
    print('-'*50)
    print(f'Conta: {numero_conta}\nAgência: 0001')
    print('-'*50)

    return True

def menu_um(): # Menu de acesso ao sistema
    while True:
        print('=============== Bem vindo ao Banco Ebner ===============')
        print('\n[1] Novo por aqui? Crie sua conta.')
        print('[2] Já possui conta? Realize seu acesso.\n')
        print('========================================================')
        opcao_entrar = input()

        if opcao_entrar == '1':
            print('=============== Cadastro Novo Usuário ===============\n')
            print('Primeiro vamos cadastrar seu usuário.')
            if adicionar_usuario():
                criar_conta_bancaria()
            
        elif opcao_entrar == '2':
            print('\n=============== Realize seu acesso ===============\n')
            acessar()
        else:
            print('Opção inválida, por favor tente novamente.')

def acessar(): #Função de acesso ao sistema
    print('Agência: 0001')
    conta_acesso = int(input('Conta: '))
    conta_senha_acesso = input('Senha: ')
    
    if conta_acesso in contas:
        if contas[conta_acesso]['conta_senha'] == conta_senha_acesso:
            print('Bem vindo ao sistema')
            menu_operacoes(conta_acesso)  # Passar o número da conta para o menu de operações
        else:
            print('Senha incorreta, acesso não autorizado!')
    else:
        print('Conta não encontrada, acesso não autorizado!')

# Variáveis globais para controle das operações bancárias
saques = []
depositos = []
saldo_global = 0
limite_diario = 500
limite_saques = 3
numero_saques = 0
numero_depositos = 0

# Função para realizar um depósito
def deposito(numero_conta):
    global saldo_global, numero_depositos
    print('\n=============== Depósito ===============')
    valor_deposito = float(input('Informe o valor desejado para depósito: R$ '))
    if valor_deposito <= 0:
        print('Você informou um valor inválido. O depósito não foi realizado.')
        return False
    else:
        saldo_global += valor_deposito
        contas[numero_conta]['saldo'] += valor_deposito
        numero_depositos += 1
        depositos.append(valor_deposito)
        print(f'Depósito de R$ {valor_deposito:.2f} realizado com sucesso.\n')
        return True

# Função para realizar um saque
def saque(numero_conta):
    global saldo_global, numero_saques
    print('\n=============== Saque ===============')
    if numero_saques >= limite_saques:
        print('Você atingiu o limite diário de saques. Por favor, volte amanhã.')
        return False
    else:
        valor_saque = float(input(f'Informe o valor desejado para saque (limite diário de R$ {limite_diario:.2f}): R$ '))
        if valor_saque > saldo_global:
            print('Você não possui saldo suficiente para realizar este saque.')
        elif valor_saque > limite_diario:
            print(f'Limite de saque diário excedido. Máximo permitido: R$ {limite_diario:.2f}.')
        elif valor_saque <= 0:
            print('Você informou um valor inválido. O saque não foi realizado.')
        else:
            saldo_global -= valor_saque
            contas[numero_conta]['saldo'] -= valor_saque
            numero_saques += 1
            saques.append(valor_saque)
            print(f'Saque de R$ {valor_saque:.2f} realizado com sucesso.\n')
        return True

# Função para exibir o extrato da conta
def extrato(numero_conta):
    global saldo_global
    print('\n=============== Extrato ===============')
    print(f'Agência: 0001')
    print(f'Conta: {numero_conta}')
    print('Depósitos realizados:')
    for i, valor in enumerate(depositos, 1):
        print(f'Depósito {i}: R$ {valor:.2f}')
    print('\nSaques realizados:')
    for i, valor in enumerate(saques, 1):
        print(f'Saque {i}: R$ {valor:.2f}')
    print(f'\nSaldo atual da sua conta: R$ {contas[numero_conta]["saldo"]:.2f}\n')
    return True

# Loop principal do menu de operações
def menu_operacoes(numero_conta):
    while True:
        opcao = input(menu.format(numero_conta=numero_conta, usuario=usuarios[contas[numero_conta]['cpf']])).strip().lower()
        
        if opcao == 'd':
            deposito(numero_conta)
        elif opcao == 's':
            saque(numero_conta)
        elif opcao == 'e':
            extrato(numero_conta)
        elif opcao == 'q':
            print('Obrigado por utilizar nossos serviços. Volte sempre!')
            break
        else:
            print('Opção inválida. Por favor, selecione uma opção válida.')

# Menu de operações bancárias
menu = """
=============== Banco Ebner ===============

Bem vindo {usuario[nome]}
Agência: 0001
Conta: {numero_conta}

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Iniciar o menu de operações
menu_um()
