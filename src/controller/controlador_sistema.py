from datetime import datetime, timedelta

from view.tela_sistema import TelaSistema

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
        self._consumidor_logado = Consumidor(
            bloqueadoAte=None,
            preferenciasAlimentares=[],
            penalidade=0,
            dataCadastro=datetime.now(),
            email="teste@email.com",
            id=1,
            localizacao=Localizacao("Florianópolis", "Centro", "Rua Teste, 100"),
            nome="Consumidor Teste",
            senha="123"
        )
        self._estabelecimento_logado = None

        self._controlador_estabelecimento = ControladorEstabelecimento(self)
        self._controlador_oferta = ControladorOfertaRelampago(self)
        self._controlador_reservas = ControladorReservas(self)

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

    def _carrega_dados_exemplo(self):
        agora = datetime.now()
        c = self._consumidor_logado

        def oferta(id, titulo, estab, original, desconto):
            return OfertaRelampago(id, titulo, "Cesta surpresa do dia", estab, original, desconto,
                                   5, agora - timedelta(hours=3), agora + timedelta(hours=6))

        r1 = Reserva(1, c, oferta(1, "Cesta de paes", "Padaria Sol", 30.0, 10.0), agora + timedelta(hours=5))
        r2 = Reserva(2, c, oferta(2, "Marmita do dia", "Restaurante Bom Prato", 35.0, 15.0), agora + timedelta(minutes=30))
        r3 = Reserva(3, c, oferta(3, "Cesta de frutas", "Mercado Verde", 25.0, 9.0), agora - timedelta(days=1))
        r3.status = StatusReserva.RETIRADA
        r4 = Reserva(4, c, oferta(4, "Cesta de salgados", "Padaria Sol", 20.0, 8.0), agora - timedelta(days=2))
        r4.status = StatusReserva.EXPIRADA
        r5 = Reserva(5, c, oferta(5, "Torta", "Padaria Sol", 40.0, 18.0), agora - timedelta(days=3))
        r5.status = StatusReserva.CANCELADA

        for reserva in [r1, r2, r3, r4, r5]:
            self._controlador_reservas.adicionar_reserva(reserva)

    def inicializa_sistema(self):
        self.abre_tela()

    def minhas_reservas(self):
        self._controlador_reservas.abre_tela()

    def cadastrar_estabelecimento(self):
        self._controlador_estabelecimento.iniciarCadastro()

    def logar_estabelecimento(self):
        user = self._controlador_estabelecimento.iniciarLogin()
        if user:
            self._estabelecimento_logado = user
            self.abrir_gerenciador_ofertas() 

    def abrir_gerenciador_ofertas(self):
        if not self._estabelecimento_logado:
            print("\nErro: Você precisa fazer login como estabelecimento primeiro.")
            return

        opcoes_oferta = {
            1: self._controlador_oferta.criarOferta,
            2: self._controlador_oferta.listarOferta,
            3: self._controlador_oferta.atualizarOferta,
            4: self._controlador_oferta.excluirOferta
        }

        while True:
            opcao = self._tela_sistema.menu_gerenciar_ofertas()
            if opcao == 0:
                self._estabelecimento_logado = None 
                print("\nLogout do estabelecimento efetuado.")
                break
            elif opcao in opcoes_oferta:
                opcoes_oferta[opcao]()
            else:
                print("Opção inválida.")

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.minhas_reservas,
            2: self.cadastrar_estabelecimento,
            3: self.logar_estabelecimento,
            4: self.abrir_gerenciador_ofertas,
            0: self.encerra_sistema
        }

        while True:
            opcao_escolhida = self._tela_sistema.tela_opcoes()
            if opcao_escolhida in lista_opcoes:
                lista_opcoes[opcao_escolhida]()
            else:
                print("Opção inválida")