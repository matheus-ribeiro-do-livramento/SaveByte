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

    def mostra_titulo(self, titulo: str):
        print("\n======== " + titulo + " ========")

    def mostra_reserva(self, dados_reserva):
        print("CODIGO DA RESERVA: ", dados_reserva["id"])
        print("OFERTA: ", dados_reserva["titulo"])
        print("STATUS: ", dados_reserva["status"])
        print("TOKEN: ", dados_reserva["token"])
        print("\n")

    def mostra_reserva_detalhes(self, dados_reserva):
        print("\n-------- DETALHES DA RESERVA ----------")
        print("CODIGO DA RESERVA: ", dados_reserva["id"])
        print("STATUS: ", dados_reserva["status"])
        print("TOKEN: ", dados_reserva["token"])
        print("OFERTA: ", dados_reserva["titulo"])
        print("DESCRICAO: ", dados_reserva["descricao"])
        print("ESTABELECIMENTO: ", dados_reserva["estabelecimento"])
        print("PRECO: R$ {:.2f} (de R$ {:.2f})".format(dados_reserva["preco"], dados_reserva["preco_original"]))
        print("RESERVADO EM: ", dados_reserva["data_reserva"].strftime("%d/%m/%Y %H:%M"))
        print("RETIRAR ATE: ", dados_reserva["limite_retirada"].strftime("%d/%m/%Y %H:%M"))
        print("\n")

    def seleciona_reserva(self):
        return self.le_inteiro("Codigo da reserva que deseja selecionar: ")

    def pergunta_cancelamento(self):
        resposta = input("Deseja solicitar o cancelamento desta reserva? (s/n): ")
        return resposta.strip().lower() == "s"

    def mostra_mensagem(self, msg):
        print(msg)