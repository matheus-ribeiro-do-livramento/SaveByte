from abc import ABC
from datetime import datetime


class Usuario(ABC):
    def __init__(
        self,
        id: int,
        nome: str,
        email: str,
        senha_hash: str,
        localizacao,  
        data_cadastro: datetime = None
    ):
        self._id: int = id
        self._nome: str = nome
        self._email: str = email
        self._senha_hash: str = senha_hash
        self._localizacao = localizacao
        self._data_cadastro: datetime = data_cadastro or datetime.now()

#Feito por Matheus