from datetime import datetime, timedelta

from view.tela_sistema import TelaSistema
from controller.controlador_reserva import ControladorReservas
from model.consumidor import Consumidor
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
        self._controlador_reservas = ControladorReservas(self)
        self._tela_sistema = TelaSistema()

    @property
    def consumidor_logado(self):
        return self._consumidor_logado

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
                print("Opção inválida")