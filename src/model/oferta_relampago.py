from datetime import datetime, timedelta
from model.enums import StatusOferta


class OfertaRelampago:
    def __init__(self, id: int, titulo: str, descricao: str, nome_estabelecimento: str,
                 original: float, desconto: float, quantidade: int,
                 janela_inicio: datetime, janela_fim: datetime):
        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._nome_estabelecimento = nome_estabelecimento
        self._original = original
        self._desconto = desconto
        self._quantidade = quantidade
        self._inicio = janela_inicio
        self._fim = janela_fim
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
    def original(self):
        return self._original

    @original.setter
    def original(self, original):
        self._original = original

    @property
    def desconto(self):
        return self._desconto

    @desconto.setter
    def desconto(self, desconto):
        self._desconto = desconto

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self._quantidade = quantidade

    @property
    def inicio(self):
        return self._inicio

    @inicio.setter
    def inicio (self, inicio):
        self._inicio = inicio

    @property
    def fim (self):
        return self._fim

    @fim.setter
    def fim(self, fim):
        self._fim = fim

    @property
    def status(self):
        return self._status    

    @status.setter
    def status(self, status):
        self._status = status

    def decrementar_quantidade(self):
        self._quantidade -= 1
        if self._quantidade <= 0:
            self._status = StatusOferta.ESGOTADA

    # NOVO (não estava na UML): devolve a cesta ao estoque quando a reserva é cancelada
    def incrementar_quantidade(self):
        self._quantidade += 1
        if self._status == StatusOferta.ESGOTADA:
            self._status = StatusOferta.DISPONIVEL

    def validarJanelaRetirada (self):
        tempo = self._fim - self._inicio

        if(tempo >= timedelta(hours = 2, minutes = 30 )):
            return True
        else:
            return False
