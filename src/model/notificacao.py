from datetime import datetime
from enums import TipoNotificacao

class Notificacao:
    def __init__(
        self,
        id: int,
        mensagem: str,
        tipo: TipoNotificacao,
        lida: bool = False,
        data_envio: datetime = None
    ):
        self._id: int = id
        self._mensagem: str = mensagem
        self._tipo: TipoNotificacao = tipo
        self._lida: bool = lida
        self._data_envio: datetime = data_envio or datetime.now()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = valor

    @property
    def mensagem(self):
        return self._mensagem

    @mensagem.setter
    def mensagem(self, valor: str):
        self._mensagem = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor: TipoNotificacao):
        self._tipo = valor

    @property
    def lida(self):
        return self._lida

    @lida.setter
    def lida(self, valor: bool):
        self._lida = valor

    @property
    def data_envio(self):
        return self._data_envio

    @data_envio.setter
    def data_envio(self, valor: datetime):
        self._data_envio = valor

#Feito por Matheus