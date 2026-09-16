from datetime import datetime

from src.model.enums import StatusReserva
from src.model.token import Token


class Reserva:
    def __init__(
        self,
        id: int,
        data_hora_retirada: datetime,
        data_hora_reserva: datetime = None,
        status: StatusReserva = StatusReserva.PENDENTE,
        token: Token = None,
    ):
        self._id = id
        self._data_hora_retirada = data_hora_retirada
        self._data_hora_reserva = data_hora_reserva or datetime.now()
        self._status = status
        self._token = token

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def data_hora_retirada(self):
        return self._data_hora_retirada

    @data_hora_retirada.setter
    def data_hora_retirada(self, data_hora_retirada):
        self._data_hora_retirada = data_hora_retirada

    @property
    def data_hora_reserva(self):
        return self._data_hora_reserva

    @data_hora_reserva.setter
    def data_hora_reserva(self, data_hora_reserva):
        self._data_hora_reserva = data_hora_reserva

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token


# Feito por Augusto
