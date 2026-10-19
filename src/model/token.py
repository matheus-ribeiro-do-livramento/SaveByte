import secrets
from datetime import datetime


class Token:
    def __init__(self):
        # RN01 / RNF07: 6 caracteres hexadecimais gerados com a biblioteca secrets
        self.__codigo = secrets.token_hex(3)
        self.__data_geracao = datetime.now()
        self.__usado = False

    @property
    def codigo(self):
        return self.__codigo

    @property
    def data_geracao(self):
        return self.__data_geracao

    @property
    def usado(self):
        return self.__usado

    @usado.setter
    def usado(self, usado: bool):
        self.__usado = usado

    def validar(self, codigo_informado: str):
        return (not self.__usado) and self.__codigo == codigo_informado.strip().lower()