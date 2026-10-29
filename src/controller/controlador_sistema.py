from datetime import datetime, timedelta

from view.tela_sistema import TelaSistema

from controller.controlador_consumidor import ControladorConsumidor
from controller.controlador_reserva import ControladorReservas
from controller.controlador_estabelecimento import ControladorEstabelecimento
from controller.controlador_oferta_relampago import ControladorOfertaRelampago

from model.consumidor import Consumidor
from model.oferta_relampago import OfertaRelampago
from model.reserva import Reserva
from model.enums import StatusReserva
from model.localizacao import Localizacao

class ControladorSistema:

    def __init__(self):
        self._consumidor_logado = None
        self._estabelecimento_logado = None
        self._controlador_consumidor = ControladorConsumidor(self)
        self._controlador_estabelecimento = ControladorEstabelecimento(self)
        self._controlador_oferta = ControladorOfertaRelampago(self)
        self._controlador_reservas = ControladorReservas(self)
        self._consumidores_com_dados_exemplo = set()

        self._tela_sistema = TelaSistema()
        self._carrega_dados_exemplo()

    @property
    def consumidor_logado(self):
        return self._consumidor_logado

    @property
    def estabelecimento_logado(self):
        return self._estabelecimento_logado

    @property
    def controlador_reservas(self):
        return self._controlador_reservas

    def definir_consumidor_logado(self, consumidor):
        self._consumidor_logado = consumidor

    def definir_estabelecimento_logado(self, estabelecimento):
        self._estabelecimento_logado = estabelecimento

    def _carrega_dados_exemplo(self):
        if self._consumidor_logado is None:
            return

        if self._consumidor_logado.id in self._consumidores_com_dados_exemplo:
            return

        agora = datetime.now()
        c = self._consumidor_logado

        limite_r1 = agora + timedelta(hours=5)
        r1 = Reserva(1, c, OfertaRelampago(1, 
                                     "Cesta de paes", 
                                     'Cesta surpresa do dia',
                                     "Padaria Sol", 
                                     30.0, 
                                     10.0, 
                                     5, 
                                     agora - timedelta(hours=3), 
                                     limite_r1),limite_r1)

        limite_r2 = agora + timedelta(minutes=30)
        r2 = Reserva(2, c, OfertaRelampago(2, 
                                    "Marmita do dia", 
                                    'cesta surpresa do dia', 
                                    "Restaurante Bom Prato",
                                    35.0, 
                                    15.0, 
                                    5,
                                    agora - timedelta(hours=3),
                                    limite_r2),limite_r2)

        limite_r3 = agora - timedelta(days=1)
        r3 = Reserva(3, c, OfertaRelampago(3, 
                                     "Cesta de frutas", 
                                     'cesta surpresa do dia', 
                                     "Mercado Verde", 
                                     25.0, 
                                     9.0, 
                                     5,
                                     limite_r3 - timedelta(hours=3), 
                                     limite_r3), limite_r3, data_hora_reserva=agora - timedelta(days=2))
        r3.status = StatusReserva.RETIRADA

        limite_r4 = agora - timedelta(days=2)
        r4 = Reserva(4, c, OfertaRelampago(4, 
                                     "Cesta de salgados", 
                                     'cesta surpresa do dia', 
                                     "Padaria Sol", 
                                     20.0, 
                                     8.0, 
                                     5,
                                     limite_r4 - timedelta(hours=3), 
                                     limite_r4), limite_r4, data_hora_reserva=agora - timedelta(days=3))
        r4.status = StatusReserva.EXPIRADA

        limite_r5 = agora - timedelta(days=3)
        r5 = Reserva(5, c, OfertaRelampago(5, 
                                     "Torta", 
                                     'cesta surpresa do dia', 
                                     "Padaria Sol", 
                                     40.0, 
                                     18.0, 
                                     5,
                                     limite_r5 - timedelta(hours=3), 
                                     limite_r5), limite_r5,data_hora_reserva=agora - timedelta(days=4))
        r5.status = StatusReserva.CANCELADA

        for reserva in [r1, r2, r3, r4, r5]:
            self._controlador_reservas.adicionar_reserva(reserva)

        self._consumidores_com_dados_exemplo.add(c.id)
            

    def inicializa_sistema(self):
        self.abre_tela()

    def consumidor(self):
        self._controlador_consumidor.abre_tela_cadastro_ou_login()

    def estabelecimento(self):
        self._controlador_estabelecimento.abre_tela_cadastro_ou_login()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.consumidor,
            2: self.estabelecimento,
            0: self.encerra_sistema
        }
        while True:
            opcao_escolhida = self._tela_sistema.estabelecimento_ou_consumidor()
            if opcao_escolhida in lista_opcoes:
                lista_opcoes[opcao_escolhida]()
            else:
                print("Opção inválida")

#Feito por Matheus