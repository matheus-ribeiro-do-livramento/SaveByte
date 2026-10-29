class TelaSistema:
    def tela_opcoes(self):
        print("\n-------- SaveByte ---------")
        print("Escolha sua opção:")
        print("1 - Minhas Reservas (Consumidor)")
        print("2 - Cadastrar Estabelecimento")
        print("3 - Login de Estabelecimento")
        print("4 - Painel do Estabelecimento Logado")
        print("0 - Finalizar sistema")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")

    

    def estabelecimento_ou_consumidor(self):
        print("\n-------- SaveByte ---------")
        print("Escolha sua opção:")
        print("1 - Acessar como Consumidor")
        print("2 - Acessar como Estabelecimento")
        print("0 - Finalizar sistema")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")

#Feito por matheus