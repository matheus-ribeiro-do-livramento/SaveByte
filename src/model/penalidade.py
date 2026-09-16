from datetime import datetime


class Penalidade:
    def __init__(
        self,
        id: int,
        motivo: str,
        data_aplicacao: datetime = None,
        data_expiracao: datetime = None,
    ):
        self._id = id
        self._motivo = motivo
        self._data_aplicacao = data_aplicacao or datetime.now()
        self._data_expiracao = data_expiracao

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def motivo(self):
        return self._motivo

    @motivo.setter
    def motivo(self, motivo):
        self._motivo = motivo

    @property
    def data_aplicacao(self):
        return self._data_aplicacao

    @data_aplicacao.setter
    def data_aplicacao(self, data_aplicacao):
        self._data_aplicacao = data_aplicacao

    @property
    def data_expiracao(self):
        return self._data_expiracao

    @data_expiracao.setter
    def data_expiracao(self, data_expiracao):
        self._data_expiracao = data_expiracao


# Feito por Augusto
