from view.tela_reserva import TelaReserva


class ControladorReservas():

    def __init__(self, controlador_sistema):
        self.__reservas = []
        self.__tela_reserva = TelaReserva()
        self.__controlador_sistema = controlador_sistema
        self.__continua = True

    # Usado também pelo UC04 (reservar oferta) quando for implementado
    def adicionar_reserva(self, reserva):
        self.__reservas.append(reserva)

    # Só enxerga as reservas do consumidor logado
    def pega_reservas_do_consumidor(self):
        consumidor = self.__controlador_sistema.consumidor_logado
        return [r for r in self.__reservas if r.consumidor.id == consumidor.id]

    def pega_reserva_por_id(self, id: int):
        for reserva in self.pega_reservas_do_consumidor():
            if reserva.id == id:
                return reserva
        return None

    # Converte a Reserva em um dicionário para a tela (a tela não conhece o modelo)
    def __dados_reserva(self, reserva):
        oferta = reserva.oferta
        return {"id": reserva.id,
                "status": reserva.status.value,
                "token": reserva.token.codigo,
                "titulo": oferta.titulo,
                "descricao": oferta.descricao,
                "estabelecimento": oferta.nome_estabelecimento,
                "preco": oferta.preco_com_desconto,
                "preco_original": oferta.preco_original,
                "data_reserva": reserva.data_hora_reserva,
                "limite_retirada": reserva.data_hora_limite_retirada}

    # Reservas atuais = pendentes; anteriores = retiradas, expiradas ou canceladas
    def lista_reservas(self):
        reservas = self.pega_reservas_do_consumidor()
        atuais = [r for r in reservas if r.esta_pendente()]
        anteriores = [r for r in reservas if not r.esta_pendente()]

        self.__tela_reserva.mostra_titulo("RESERVAS ATUAIS")
        if len(atuais) == 0:
            self.__tela_reserva.mostra_mensagem("Voce nao possui reservas atuais.\n")
        for reserva in atuais:
            self.__tela_reserva.mostra_reserva(self.__dados_reserva(reserva))

        self.__tela_reserva.mostra_titulo("RESERVAS ANTERIORES")
        if len(anteriores) == 0:
            self.__tela_reserva.mostra_mensagem("Voce nao possui reservas anteriores.\n")
        for reserva in anteriores:
            self.__tela_reserva.mostra_reserva(self.__dados_reserva(reserva))

    def consultar_reserva(self):
        self.lista_reservas()
        id_reserva = self.__tela_reserva.seleciona_reserva()
        reserva = self.pega_reserva_por_id(id_reserva)

        if reserva is None:
            self.__tela_reserva.mostra_mensagem("ATENCAO: Reserva nao existente")
            return

        self.__tela_reserva.mostra_reserva_detalhes(self.__dados_reserva(reserva))

        # Só reservas atuais podem ter cancelamento solicitado
        if reserva.esta_pendente() and self.__tela_reserva.pergunta_cancelamento():
            self.cancelar_reserva(reserva)

    # Segue o diagrama de atividades: verifica status -> verifica prazo -> cancela
    def cancelar_reserva(self, reserva):
        if not reserva.esta_pendente():
            self.__tela_reserva.mostra_mensagem("Nao e possivel cancelar: a reserva nao esta com o status pendente.")
        elif not reserva.esta_dentro_do_prazo_de_cancelamento():
            self.__tela_reserva.mostra_mensagem("O prazo para o cancelamento da reserva acabou (minimo de 1 hora de antecedencia).")
        else:
            reserva.cancelar()
            self.__tela_reserva.mostra_mensagem("Reserva cancelada com sucesso!")

    def retornar(self):
        self.__continua = False

    def abre_tela(self):
        lista_opcoes = {1: self.lista_reservas, 2: self.consultar_reserva, 0: self.retornar}

        self.__continua = True
        while self.__continua:
            opcao = self.__tela_reserva.tela_opcoes()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()
            else:
                self.__tela_reserva.mostra_mensagem("Opcao invalida")