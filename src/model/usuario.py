from abc import ABC
from datetime import datetime
from model.localizacao import Localizacao


class Usuario(ABC):
    def __init__(self, id: int, nome: str, email: str, senha_hash: str, cidade: str, bairro: str, endereco: str, data_cadastro: datetime = None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha_hash = senha_hash
        self._localizacao = Localizacao(cidade, bairro, endereco)
        self._data_cadastro = data_cadastro or datetime.now()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id


#Feito por Matheus