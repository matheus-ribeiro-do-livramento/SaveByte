class TelaConsumidor:
    def tela_opcoes(self):
        print("-------- SaveByte ---------")
        print("Escolha sua opção")
        print("1 - Minhas Reservas")
        print("0 - Retornar")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")
                continue


    def cadastro_ou_login(self):
        print("-------- SaveByte ---------")
        print("Escolha sua opção")
        print("1 - Cadastrar consumidor")
        print("2 - Login de consumidor")
        print("0 - Retornar")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")
                continue
    
    def login_consumidor(self):
        print("-------- Login de Consumidor ---------")
        print("Digite seu e-mail:")
        email = input()
        print("Digite sua senha:")
        senha = input()
        return {"email": email, "senha": senha}

    def cadastro_consumidor(self):
        print("-------- Cadastro de Consumidor ---------")
        print("Digite seu nome:")
        nome = input()
        print("Digite a cidade onde você mora:")
        cidade = input()
        print("Digite o bairro onde você mora:")
        bairro = input()
        print("Digite o endereço onde você mora:")
        endereco = input()
        print("Digite seu e-mail:")
        email = input()
        print("Digite sua senha:")
        senha = input()

        return {"nome": nome, "cidade": cidade, "bairro": bairro, "endereco": endereco, "email": email, "senha": senha}

    def mensagem(self, msg):
        print(msg)