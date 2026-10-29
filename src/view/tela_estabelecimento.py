class TelaEstabelecimento():

    def pegaDadosEstabelecimento(self):
        print('\nDigite o nome fantasia do estabelecimento\n')
        nomeFantasia = input()
        print('\nDigite o e-mail do estabelecimento')
        email = input()
        print('\nDigite o endereço do estabelecimento')
        endereco = input()
        print('\nDigite o CNPJ do estabelecimento (Somente numeros)')
        cnpj = input()
        print('\nDigite o tipo do estabelecimento (EX: padaria, mercado...)')
        tipo = input()
        print('\nCrie uma senha de acesso para o estabelecimento\n')
        senha = input()

        dados = {"nome":nomeFantasia,"email":email,"endereco":endereco,"cnpj":cnpj,"tipo":tipo,"senha":senha}

        return dados

    def pegaDadosLogin(self):
        print('\n-----Login Estabelecimento-----')
        print('Digite o e-mail:')
        email = input()
        print('Digite a senha:')
        senha = input()

        return {"email": email, "senha": senha}

    def mensagem(self, msg):
        print(msg)

    def cadastro_ou_login(self):
        print("\n-------- SaveByte ---------")
        print("Escolha sua opção:")
        print("1 - Cadastrar Estabelecimento")
        print("2 - Login de Estabelecimento")
        print("0 - Retornar")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")

    def menu_gerenciar_ofertas(self):
            print('\n--- Gerenciar Ofertas Relâmpago ---')
            print('1 - Criar nova oferta')
            print('2 - Visualizar minhas ofertas')
            print('3 - Atualizar uma oferta')
            print('4 - Excluir uma oferta')
            print('5 - Validar resgate de uma reserva')
            print('0 - Deslogar e Voltar ao menu principal')
            while True:
                try:
                    return int(input("Escolha a opção: "))
                except ValueError:
                    print("Valor inválido, digite um número inteiro.")

#Feito por Gabriel