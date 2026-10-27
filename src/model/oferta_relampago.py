from datetime import datetime
from model.enums import StatusOferta


class OfertaRelampago:
    def __init__(self, id: int, titulo: str, descricao: str, nome_estabelecimento: str,
                 preco_original: float, preco_com_desconto: float, quantidade_disponivel: int,
                 janela_inicio: datetime, janela_fim: datetime):
        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._nome_estabelecimento = nome_estabelecimento
        self._preco_original = preco_original
        self._preco_com_desconto = preco_com_desconto
        self._quantidade_disponivel = quantidade_disponivel
        self._janela_inicio = janela_inicio
        self._janela_fim = janela_fim
        self._status = StatusOferta.DISPONIVEL

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @property
    def nome_estabelecimento(self):
        return self._nome_estabelecimento

    @nome_estabelecimento.setter
    def nome_estabelecimento(self, nome_estabelecimento):
        self._nome_estabelecimento = nome_estabelecimento

    @property
    def preco_original(self):
        return self._preco_original

    @preco_original.setter
    def preco_original(self, preco_original):
        self._preco_original = preco_original

    @property
    def preco_com_desconto(self):
        return self._preco_com_desconto

    @preco_com_desconto.setter
    def preco_com_desconto(self, preco_com_desconto):
        self._preco_com_desconto = preco_com_desconto

    @property
    def quantidade_disponivel(self):
        return self._quantidade_disponivel

    @quantidade_disponivel.setter
    def quantidade_disponivel(self, quantidade_disponivel):
        self._quantidade_disponivel = quantidade_disponivel

    @property
    def janela_inicio(self):
        return self._janela_inicio

    @janela_inicio.setter
    def janela_inicio(self, janela_inicio):
        self._janela_inicio = janela_inicio

    @property
    def janela_fim(self):
        return self._janela_fim

    @janela_fim.setter
    def janela_fim(self, janela_fim):
        self._janela_fim = janela_fim

    @property
    def status(self):
        return self._status    

    @status.setter
    def status(self, status):
        self._status = status

# Feito por Augusto
