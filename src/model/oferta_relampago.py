from datetime import datetime
from model.enums import StatusOferta


class OfertaRelampago:
    # nome_estabelecimento é provisório: quando o Estabelecimento for integrado,
    # troque por uma referência ao objeto Estabelecimento (como está na UML).
    def __init__(self, id: int, titulo: str, descricao: str, nome_estabelecimento: str,
                 preco_original: float, preco_com_desconto: float, quantidade_disponivel: int,
                 janela_inicio: datetime, janela_fim: datetime):
        self.__id = id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__nome_estabelecimento = nome_estabelecimento
        self.__preco_original = preco_original
        self.__preco_com_desconto = preco_com_desconto
        self.__quantidade_disponivel = quantidade_disponivel
        self.__janela_inicio = janela_inicio
        self.__janela_fim = janela_fim
        self.__status = StatusOferta.DISPONIVEL

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def descricao(self):
        return self.__descricao

    @property
    def nome_estabelecimento(self):
        return self.__nome_estabelecimento

    @property
    def preco_original(self):
        return self.__preco_original

    @property
    def preco_com_desconto(self):
        return self.__preco_com_desconto

    @property
    def quantidade_disponivel(self):
        return self.__quantidade_disponivel

    @property
    def status(self):
        return self.__status

    def decrementar_quantidade(self):
        self.__quantidade_disponivel -= 1
        if self.__quantidade_disponivel <= 0:
            self.__status = StatusOferta.ESGOTADA

    # NOVO (não estava na UML): devolve a cesta ao estoque quando a reserva é cancelada
    def incrementar_quantidade(self):
        self.__quantidade_disponivel += 1
        if self.__status == StatusOferta.ESGOTADA:
            self.__status = StatusOferta.DISPONIVEL