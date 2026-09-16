from src.model.enums import TipoEstabelecimento
from src.model.localizacao import Localizacao


class Estabelecimento:
    def __init__(
        self,
        cnpj: str,
        endereco: str,
        nome_fantasia: str,
        tipo: TipoEstabelecimento,
    ):
        self._cnpj = cnpj
        self._endereco = endereco
        self._nome_fantasia = nome_fantasia
        self._tipo = tipo

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


# Feito por Augusto
