import secrets
from datetime import datetime


class Token:
    def __init__(self, codigo: str = None, data_geracao: datetime = None, usado: bool = False):
        self._codigo = codigo or secrets.token_hex(3)
        self._data_geracao = data_geracao or datetime.now()
        self._usado = usado

    @property
    def codigo(self):
        return self._codigo

    @property
    def data_geracao(self):
        return self._data_geracao

    @property
    def usado(self):
        return self._usado

    @usado.setter
    def usado(self, usado: bool):
        self._usado = usado

    def validar(self, codigoInformado: str) -> bool:
        if self.codigo == codigoInformado and not self.usado:
            self.usado = True
            return True
        return False


# Feito por Augusto
