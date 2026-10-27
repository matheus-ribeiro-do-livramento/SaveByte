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

