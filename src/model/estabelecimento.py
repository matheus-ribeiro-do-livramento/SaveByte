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
        email: str,
        cidade: str = "",
        bairro: str = "",
        localizacao: Localizacao = None,
    ):
        self._cnpj = cnpj
        self._localizacao = localizacao or Localizacao(cidade, bairro, endereco)
        self._endereco = self._localizacao.endereco
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
        return self._localizacao.endereco

    @endereco.setter
    def endereco(self, endereco):
        self._endereco = endereco
        self._localizacao.endereco = endereco

    @property
    def localizacao(self):
        return self._localizacao

    @localizacao.setter
    def localizacao(self, localizacao: Localizacao):
        self._localizacao = localizacao
        self._endereco = localizacao.endereco

    @property
    def cidade(self):
        return self._localizacao.cidade

    @cidade.setter
    def cidade(self, cidade: str):
        self._localizacao.cidade = cidade

    @property
    def bairro(self):
        return self._localizacao.bairro

    @bairro.setter
    def bairro(self, bairro: str):
        self._localizacao.bairro = bairro

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

    @senha.setter
    def senha(self, senha):
        self._senha =  senha

    @property
    def email (self):
        return self._email

    @email.setter
    def email (self, email):
        self._email = email


# Feito por Augusto
