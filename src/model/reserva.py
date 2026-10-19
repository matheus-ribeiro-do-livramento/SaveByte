from datetime import datetime, timedelta
from model.enums import StatusReserva
from model.token import Token
from model.oferta_relampago import OfertaRelampago
from model.consumidor import Consumidor


class Reserva:
    def __init__(self, id: int, consumidor: Consumidor, oferta: OfertaRelampago,
                 data_hora_limite_retirada: datetime, data_hora_reserva: datetime = None):
        self.__id = id
        self.__consumidor = consumidor
        self.__oferta = oferta
        self.__data_hora_limite_retirada = data_hora_limite_retirada
        self.__data_hora_reserva = data_hora_reserva or datetime.now()
        self.__status = StatusReserva.PENDENTE
        self.__token = self.gerar_token()  # RF09: token gerado na criação da reserva

    @property
    def id(self):
        return self.__id

    @property
    def consumidor(self):
        return self.__consumidor

    @property
    def oferta(self):
        return self.__oferta

    @property
    def data_hora_limite_retirada(self):
        return self.__data_hora_limite_retirada

    @property
    def data_hora_reserva(self):
        return self.__data_hora_reserva

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: StatusReserva):
        self.__status = status

    @property
    def token(self):
        return self.__token

    def gerar_token(self):
        return Token()

    def esta_pendente(self):
        return self.__status == StatusReserva.PENDENTE

    # RN07: cancelar com no mínimo 1 hora de antecedência do horário final de retirada
    def esta_dentro_do_prazo_de_cancelamento(self):
        limite_para_cancelar = self.__data_hora_limite_retirada - timedelta(hours=1)
        return datetime.now() <= limite_para_cancelar

    def cancelar(self):
        self.__status = StatusReserva.CANCELADA
        self.__oferta.incrementar_quantidade()