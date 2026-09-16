from abc import ABC
from datetime import datetime
from localizacao import Localizacao


class Usuario(ABC):
    def __init__(self, id: int, nome: str, email: str, senha_hash: str,  endereco: str, latitude: float, longitude: float,   data_cadastro: datetime = None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha_hash = senha_hash
        self._localizacao = Localizacao(endereco, latitude, longitude)
        self._data_cadastro = data_cadastro or datetime.now()

#Feito por Matheus