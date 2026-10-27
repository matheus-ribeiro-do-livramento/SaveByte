from model.enums import TipoEstabelecimento
from model.localizacao import Localizacao


class Estabelecimento:
    def __init__(
        self,
        cnpj: str,
        endereco: str,
        nome_fantasia: str,
        tipo: TipoEstabelecimento,
        senha: str,
        email = str

    ):
        self._cnpj = cnpj
        self._endereco = endereco
        self._nome_fantasia = nome_fantasia
        self._tipo = tipo
        self._senha = senha
        self._email = email

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        self._cnpj = cnpj

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, endereco):
        self._endereco = endereco

    @property
    def nome_fantasia(self):
        return self._nome_fantasia

    @nome_fantasia.setter
    def nome_fantasia(self, nome_fantasia):
        self._nome_fantasia = nome_fantasia

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

    @property
    def senha (self):
        return self._senha

    @senha.getter
    def senha(self, senha):
        self._senha =  senha

    @property
    def email (self):
        return self._email

    @email.getter
    def email (self, email):
        self._email = email


# Feito por Augusto
