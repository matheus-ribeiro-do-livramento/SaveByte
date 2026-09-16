from datetime import datetime


class Token:
    def __init__(
        self,
        codigo: str,
        data_geracao: datetime = None,
        usado: bool = False,
    ):
        self._codigo = codigo
        self._data_geracao = data_geracao or datetime.now()
        self._usado = usado

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @property
    def data_geracao(self):
        return self._data_geracao

    @data_geracao.setter
    def data_geracao(self, data_geracao):
        self._data_geracao = data_geracao

    @property
    def usado(self):
        return self._usado

    @usado.setter
    def usado(self, usado):
        self._usado = usado


# Feito por Augusto
