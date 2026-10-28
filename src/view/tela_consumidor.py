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
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha:")
        return {"email": email, "senha": senha}

    def cadastro_consumidor(self):
        print("-------- Cadastro de Consumidor ---------")
        nome = self.le_campo('Digite seu nome: ')
        cidade = self.le_campo('Digite a cidade onde você mora: ')
        bairro = self.le_campo('Digite o bairro onde você mora: ')
        endereco = self.le_campo('Digite o endereço onde você mora: ')
        email = self.le_campo('Digite seu e-mail: ')
        senha = self.le_campo('Digite sua senha: ')

        return {"nome": nome, "cidade": cidade, "bairro": bairro, "endereco": endereco, "email": email, "senha": senha}

    def mensagem(self, msg):
        print(msg)

    def le_campo(self, mensagem_input):
        while True:
            valor = input(mensagem_input)
            if valor.strip():
                return valor
            print("Campo obrigatório! Por favor, digite um valor válido.")