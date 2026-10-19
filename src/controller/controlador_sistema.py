from datetime import datetime, timedelta

from view.tela_sistema import TelaSistema
from controller.controlador_reserva import ControladorReservas
from model.consumidor import Consumidor
from model.oferta_relampago import OfertaRelampago
from model.reserva import Reserva
from model.enums import StatusReserva
from model.localizacao import Localizacao


class ControladorSistema:

    def __init__(self):
        # Provisório: quando o UC06 (login) existir, o consumidor logado virá de lá
        self.__consumidor_logado = Consumidor( bloqueadoAte=None,
    preferenciasAlimentares=[],
    penalidade=0,
    dataCadastro=datetime.now(),
    email="teste@email.com",
    id=1,
    localizacao=Localizacao("Florianópolis", "Centro", "Rua Teste, 100"),
    nome="Consumidor Teste",
    senha="123",)
        self.__controlador_reservas = ControladorReservas(self)
        self.__tela_sistema = TelaSistema()
        self.__carrega_dados_exemplo()

    @property
    def consumidor_logado(self):
        return self.__consumidor_logado

    @property
    def controlador_reservas(self):
        return self.__controlador_reservas

    # Dados de teste (sem banco de dados). Apagar quando o UC04 criar reservas de verdade.
    def __carrega_dados_exemplo(self):
        agora = datetime.now()
        c = self.__consumidor_logado

        def oferta(id, titulo, estab, original, desconto):
            return OfertaRelampago(id, titulo, "Cesta surpresa do dia", estab, original, desconto,
                                   5, agora - timedelta(hours=3), agora + timedelta(hours=6))

        # 1: atual, dá para cancelar (limite daqui a 5h)
        r1 = Reserva(1, c, oferta(1, "Cesta de paes", "Padaria Sol", 30.0, 10.0), agora + timedelta(hours=5))
        # 2: atual, fora do prazo de cancelamento (limite daqui a 30min)
        r2 = Reserva(2, c, oferta(2, "Marmita do dia", "Restaurante Bom Prato", 35.0, 15.0), agora + timedelta(minutes=30))
        # 3, 4, 5: anteriores
        r3 = Reserva(3, c, oferta(3, "Cesta de frutas", "Mercado Verde", 25.0, 9.0), agora - timedelta(days=1))
        r3.status = StatusReserva.RETIRADA
        r4 = Reserva(4, c, oferta(4, "Cesta de salgados", "Padaria Sol", 20.0, 8.0), agora - timedelta(days=2))
        r4.status = StatusReserva.EXPIRADA
        r5 = Reserva(5, c, oferta(5, "Torta", "Padaria Sol", 40.0, 18.0), agora - timedelta(days=3))
        r5.status = StatusReserva.CANCELADA

        for reserva in [r1, r2, r3, r4, r5]:
            self.__controlador_reservas.adicionar_reserva(reserva)

    def inicializa_sistema(self):
        self.abre_tela()

    def minhas_reservas(self):
        self.__controlador_reservas.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {1: self.minhas_reservas, 0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            if opcao_escolhida in lista_opcoes:
                lista_opcoes[opcao_escolhida]()
            else:
                print("Opcao invalida")