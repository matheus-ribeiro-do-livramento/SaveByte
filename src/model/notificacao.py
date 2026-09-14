from datetime import datetime
from enums import TipoNotificacao

class Notificacao:
    def __init__(self, id: int, mensagem: str, tipo: TipoNotificacao, lida: bool = False, data_envio: datetime = None):
        self._id = id
        self._mensagem = mensagem
        self._tipo = tipo
        self._lida = lida
        self._data_envio = data_envio or datetime.now()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def mensagem(self):
        return self._mensagem

    @mensagem.setter
    def mensagem(self, mensagem):
        self._mensagem = mensagem

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

    @property
    def lida(self):
        return self._lida

    @lida.setter
    def lida(self, lida):
        self._lida = lida

    @property
    def data_envio(self):
        return self._data_envio

    @data_envio.setter
    def data_envio(self, data_envio):
        self._data_envio = data_envio

#Feito por Matheus