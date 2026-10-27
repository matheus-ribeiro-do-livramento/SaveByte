from datetime import datetime, timedelta

from view.tela_sistema import TelaSistema

from controller.controlador_reserva import ControladorReservas
from controller.controlador_estabelecimento import controladorEstabelecimento

from model.consumidor import Consumidor
from model.estabelecimento import Estabelecimento
from model.oferta_relampago import OfertaRelampago
from model.reserva import Reserva
from model.enums import StatusReserva
from model.localizacao import Localizacao


class ControladorSistema:

    def __init__(self):
        self._consumidor_logado = Consumidor( bloqueadoAte=None,
    preferenciasAlimentares=[],
    penalidade=0,
    dataCadastro=datetime.now(),
    email="teste@email.com",
    id=1,
    localizacao=Localizacao("Florianópolis", "Centro", "Rua Teste, 100"),
    nome="Consumidor Teste",
    senha="123",)
        self._estabelecimento_logado = None

        self.controlador_estabelecimento = controladorEstabelecimento(self)
        self.__controlador_reservas = ControladorReservas(self)

        self.__tela_sistema = TelaSistema()
        self.__carrega_dados_exemplo()

    @property
    def consumidor_logado(self):
        return self._consumidor_logado

    @property
    def estabelecimento_logado(self):
        return self._estabelecimento_logado

    @property
    def controlador_reservas(self):
        return self._controlador_reservas

    def inicializa_sistema(self):
        self.abre_tela()

    def minhas_reservas(self):
        self._controlador_reservas.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.minhas_reservas, 0: self.encerra_sistema}

        while True:
            opcao_escolhida = self._tela_sistema.tela_opcoes()
            if opcao_escolhida in lista_opcoes:
                lista_opcoes[opcao_escolhida]()
            else:
                print("Opcao invalida")


    def cadastrar_estabelecimento (self):
        self.controlador_estabelecimento.iniciarCadastro()


    def logar_estabelecimento (self):
        user = self.controlador_estabelecimento.iniciarLogin()

        if user:
            self._estabelecimento_logado = user

