from datetime import datetime, timedelta
from model.enums import StatusReserva
from model.token import Token
from model.oferta_relampago import OfertaRelampago
from model.consumidor import Consumidor


class Reserva:
    def __init__(self, id: int, consumidor: Consumidor, oferta: OfertaRelampago,
                 data_hora_limite_retirada: datetime, data_hora_reserva: datetime = None):
        self._id = id
        self._consumidor = consumidor
        self._oferta = oferta
        self._data_hora_limite_retirada = data_hora_limite_retirada
        self._data_hora_reserva = data_hora_reserva or datetime.now()
        self._status = StatusReserva.PENDENTE
        self._token = self.gerar_token() 

    @property
    def id(self):
        return self._id

    @property
    def consumidor(self):
        return self._consumidor

    @property
    def oferta(self):
        return self._oferta

    @property
    def data_hora_limite_retirada(self):
        return self._data_hora_limite_retirada

    @property
    def data_hora_reserva(self):
        return self._data_hora_reserva

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: StatusReserva):
        self._status = status

    @property
    def token(self):
        return self._token

    def gerar_token(self):
        return Token()

    def esta_pendente(self):
        return self._status == StatusReserva.PENDENTE

    def esta_dentro_do_prazo_de_cancelamento(self):
        limite_para_cancelar = self._data_hora_limite_retirada - timedelta(hours=1)
        return datetime.now() <= limite_para_cancelar

    def cancelar(self):
        self._status = StatusReserva.CANCELADA

# Feito por Augusto

#Função feito por Matheus
