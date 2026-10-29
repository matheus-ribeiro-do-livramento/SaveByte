from view.tela_resgate import TelaResgate
from view.tela_reserva import TelaReserva


class ControladorReservas():

    def __init__(self, controlador_sistema):
        self._reservas = []
        self._tela_reserva = TelaReserva()
        self._controlador_sistema = controlador_sistema
        self._continua = True

    def adicionar_reserva(self, reserva):
        self._reservas.append(reserva)

    def pega_reservas_do_consumidor(self):
        consumidor = self._controlador_sistema.consumidor_logado
        return [r for r in self._reservas if r.consumidor.id == consumidor.id]

    def pega_reserva_por_id(self, id: int):
        for reserva in self.pega_reservas_do_consumidor():
            if reserva.id == id:
                return reserva
        return None

    def verificar_reserva(self, id):
        for r in self._reservas:
            if r.id == id:
                return True
            else:
                return False

    def _dados_reserva(self, reserva):
        oferta = reserva.oferta
        return {"id": reserva.id,
                "status": reserva.status.value,
                "token": reserva.token.codigo,
                "titulo": oferta.titulo,
                "descricao": oferta.descricao,
                "estabelecimento": oferta.nome_estabelecimento,
                "preco": oferta.desconto,
                "preco_original": oferta.original,
                "data_reserva": reserva.data_hora_reserva,
                "limite_retirada": reserva.data_hora_limite_retirada}

    def lista_reservas(self):
        reservas = self.pega_reservas_do_consumidor()
        atuais = [r for r in reservas if r.esta_pendente()]
        anteriores = [r for r in reservas if not r.esta_pendente()]

        self._tela_reserva.mostra_titulo("RESERVAS ATUAIS")
        if len(atuais) == 0:
            self._tela_reserva.mostra_mensagem("Voce nao possui reservas atuais.\n")
        for reserva in atuais:
            self._tela_reserva.mostra_reserva(self._dados_reserva(reserva))

        self._tela_reserva.mostra_titulo("RESERVAS ANTERIORES")
        if len(anteriores) == 0:
            self._tela_reserva.mostra_mensagem("Voce nao possui reservas anteriores.\n")
        for reserva in anteriores:
            self._tela_reserva.mostra_reserva(self._dados_reserva(reserva))

    def consultar_reserva(self):
        self.lista_reservas()
        id_reserva = self._tela_reserva.seleciona_reserva()
        reserva = self.pega_reserva_por_id(id_reserva)

        if reserva is None:
            self._tela_reserva.mostra_mensagem("ATENCAO: Reserva nao existente")
            return

        self._tela_reserva.mostra_reserva_detalhes(self._dados_reserva(reserva))

        if reserva.esta_pendente() and self._tela_reserva.pergunta_cancelamento():
            self.cancelar_reserva(reserva)

    def cancelar_reserva(self, reserva):
        if not reserva.esta_pendente():
            self._tela_reserva.mostra_mensagem("Nao e possivel cancelar: a reserva nao esta com o status pendente.")
        elif not reserva.esta_dentro_do_prazo_de_cancelamento():
            self._tela_reserva.mostra_mensagem("O prazo para o cancelamento da reserva acabou (minimo de 1 hora de antecedencia).")
        else:
            reserva.cancelar()
            self._tela_reserva.mostra_mensagem("Reserva cancelada com sucesso!")

    def retornar(self):
        self._continua = False

    def abre_tela(self):
        lista_opcoes = {1: self.lista_reservas, 2: self.consultar_reserva, 0: self.retornar}

        self._continua = True
        while self._continua:
            opcao = self._tela_reserva.tela_opcoes()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()
            else:
                self._tela_reserva.mostra_mensagem("Opcao invalida")

    def validar_resgate(self, codigo: str, id_reserva: int):
        # Feito por Augusto
        tela = TelaResgate()

        reserva = self.pega_reserva_por_id(id_reserva)

        if reserva is None:
            tela.mostra_mensagem("Atenção: Reserva não localizada no sistema.")
            return

        if reserva.confirmarRetirada(codigo):
            tela.mostra_mensagem("Resgate validado com sucesso!")
        else:
            tela.mostra_mensagem("Erro: Token inválido ou expirado.")


# feito por matheus
