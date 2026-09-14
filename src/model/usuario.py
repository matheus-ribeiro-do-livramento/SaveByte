from abc import ABC
from datetime import datetime


class Usuario(ABC):
    def __init__(self, id: int, nome: str, email: str, senha_hash: str, localizacao: Localizacao,   data_cadastro: datetime = None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha_hash = senha_hash
        self._localizacao = localizacao
        self._data_cadastro = data_cadastro or datetime.now()

#Feito por Matheus