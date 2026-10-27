class TelaReserva():

    def tela_opcoes(self):
        print("-------- MINHAS RESERVAS ----------")
        print("Escolha a opção")
        print("1 - Listar Minhas Reservas")
        print("2 - Consultar Reserva (detalhes / cancelar)")
        print("0 - Retornar")

        return self.le_inteiro("Escolha a opção: ")

    def le_inteiro(self, mensagem: str):
        while True:
            valor = input(mensagem)
            try:
                return int(valor)
            except ValueError:
                print("Valor inválido, digite um número inteiro.")
