from view.tela_reserva import TelaReserva


class ControladorReservas():

    def __init__(self, controlador_sistema):
        self._reservas = []
        self._tela_reserva = TelaReserva()
        self._controlador_sistema = controlador_sistema
        self._continua = True

    def retornar(self):
        self._continua = False

    def abre_tela(self):
        lista_opcoes = {1: self.lista_reservas, 2: self.consultar_reserva, 0: self.retornar}

        self.__continua = True
        while self.__continua:
            opcao = self.__tela_reserva.tela_opcoes()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()
            else:
                self.__tela_reserva.mostra_mensagem("Opcao invalida")
