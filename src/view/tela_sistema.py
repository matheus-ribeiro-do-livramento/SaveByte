class TelaSistema:
    def tela_opcoes(self):
        print("-------- SaveByte ---------")
        print("Escolha sua opcao")
        print("1 - Minhas Reservas")
        print("0 - Finalizar sistema")
        while True:
            try:
                return int(input("Escolha a opcao: "))
            except ValueError:
                print("Valor invalido, digite um numero inteiro.")