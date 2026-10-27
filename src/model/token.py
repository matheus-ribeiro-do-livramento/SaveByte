import secrets
from datetime import datetime


class Token:
    def __init__(self):
        self._codigo = secrets.token_hex(3)
        self._data_geracao = datetime.now()
        self._usado = False

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

    def validar(self, codigo_informado: str):
        return (not self._usado) and self._codigo == codigo_informado.strip().lower()

# Feito por Augusto