from datetime import datetime

from src.model.enums import StatusOferta


class OfertaRelampago:
    def __init__(
        self,
        id: int,
        descricao: str,
        preco_com_desconto: float,
        preco_original: float,
        quantidade_disponivel: int,
        titulo: str,
        janela_inicio: datetime = None,
        janela_fim: datetime = None,
        status: StatusOferta = StatusOferta.DISPONIVEL,
    ):
        self._id = id
        self._descricao = descricao
        self._preco_com_desconto = preco_com_desconto
        self._preco_original = preco_original
        self._quantidade_disponivel = quantidade_disponivel
        self._titulo = titulo
        self._janela_inicio = janela_inicio
        self._janela_fim = janela_fim
        self._status = status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @property
    def preco_com_desconto(self):
        return self._preco_com_desconto

    @preco_com_desconto.setter
    def preco_com_desconto(self, preco_com_desconto):
        self._preco_com_desconto = preco_com_desconto

    @property
    def preco_original(self):
        return self._preco_original

    @preco_original.setter
    def preco_original(self, preco_original):
        self._preco_original = preco_original

    @property
    def quantidade_disponivel(self):
        return self._quantidade_disponivel

    @quantidade_disponivel.setter
    def quantidade_disponivel(self, quantidade_disponivel):
        self._quantidade_disponivel = quantidade_disponivel

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

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
