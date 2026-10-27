class TelaSistema:
    def tela_opcoes(self):
        print("-------- SaveByte ---------")
        print("Escolha sua opção")
        print("1 - Minhas Reservas")
        print("0 - Finalizar sistema")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")