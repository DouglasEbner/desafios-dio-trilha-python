
# Abertura do Menu opções para o cliente.
menu = """

=============== Banco Ebner ===============

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Variaveis de uso para a logica das operações.
saques = {}
depositos = {}
saldo = 0
limite = 500
numero_saques = 0
limite_saques = 3
numero_depositos = 0

# Loop para fuções do Menu
while True:

    opcao = input(menu).upper()
# Primeir opção Depósito
    if opcao == 'D':
        print('\n=============== Depósito ===============')
        valor_deposito = float(input('Informe o valor desejado: R$ '))
        if valor_deposito <= 0:
            print('Você informou um valor inválido, por favor informe um valor válido.')
        else:
            saldo += valor_deposito
            numero_depositos += 1
            depositos[f"Depósito {numero_depositos}"] = valor_deposito
            print(f'Você depositou R$ {valor_deposito:.2f}.\n')
# segunda Opção Saque
    elif opcao == 'S':
        print('\n=============== Saque ===============')
        if numero_saques >= limite_saques:
            print('Você não possui mais saques disponíveis para hoje, por favor volte amanhã.')
        else:
            valor_saque = float(input('Informe o quanto deseja sacar (limite de R$ 500,00 por saque): R$ '))
            if valor_saque > saldo:
                print('Você não possui saldo suficiente.')
            elif valor_saque > limite:
                print('Limite de saque diário de R$ 500,00. Por favor, informe um valor válido.')
            elif valor_saque <= 0:
                print('Você informou um valor inválido, por favor informe um valor válido.')
            else:
                saldo -= valor_saque
                numero_saques += 1
                saques[f"Saque {numero_saques}"] = valor_saque
                print(f'Saque de R$ {valor_saque:.2f} realizado com sucesso.')
                print(f'Você ainda possui {limite_saques - numero_saques} saques disponíveis para realizar hoje.\n')

# terceira Opção Extrato
    elif opcao == 'E':
        print('\n=============== Extrato ===============')
        print('Depósitos:')
        for extrato_depositos, valor in depositos.items():
            print(f'{extrato_depositos}: R$ {valor:.2f}')

        print('\nSaques:')
        for extrato_saques, valor in saques.items():
            print(f'{extrato_saques}: R$ -{valor:.2f}')

        print(f'\nSaldo da sua conta: R$ {saldo:.2f}')
        print(f'Você possui {limite_saques - numero_saques} saques disponíveis para hoje.\n')

# Quarta opção Sair
    elif opcao == 'Q':
        print('Obrigado por ser nosso cliente, volte sempre!')
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.\n')
