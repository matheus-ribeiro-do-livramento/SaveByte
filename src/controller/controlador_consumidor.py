from view.tela_consumidor import TelaConsumidor
from model.consumidor import Consumidor
from model.localizacao import Localizacao

class ControladorConsumidor:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self._tela_consumidor = TelaConsumidor()
        self._consumidor = []
        self._continua = True

    def cadastrar_consumidor(self, dados):
        for con in self._consumidor:
            if con.email == dados["email"]:
                return False

        consumidor = Consumidor(
            bloqueadoAte=None,
            preferenciasAlimentares=[],
            penalidade=0,
            dataCadastro=None,
            email=dados["email"],
            id=len(self._consumidor) + 1,
            localizacao=Localizacao(dados["cidade"], dados["bairro"], dados["endereco"]),
            nome=dados["nome"],
            senha=dados["senha"],
        )
        self._consumidor.append(consumidor)
        return True

    def iniciar_cadastro(self):
        dados = self._tela_consumidor.cadastro_consumidor()
        if self.cadastrar_consumidor(dados):
            self._tela_consumidor.mensagem("Cadastro efetuado com sucesso!")
            return True
        self._tela_consumidor.mensagem("Erro: e-mail já cadastrado.")
        return False

    def realizar_login(self, dados):
        for consumidor in self._consumidor:
            if consumidor.email == dados["email"] and consumidor.senha == dados["senha"]:
                return consumidor
        return None

    def retornar(self):
        self._continua = False

    def iniciar_login(self):
        dados = self._tela_consumidor.login_consumidor()
        consumidor = self.realizar_login(dados)
        if consumidor is None:
            self._tela_consumidor.mensagem("Erro: e-mail ou senha inválidos.")
            return None
        self._controlador_sistema.definir_consumidor_logado(consumidor)
        self._controlador_sistema._carrega_dados_exemplo()
        self._tela_consumidor.mensagem(f"Login efetuado com sucesso! Bem-vindo, {consumidor.nome}.")
        self.interface_consumidor()
    

    def abre_tela_cadastro_ou_login(self):
        lista_opcoes = {1: self.iniciar_cadastro, 2: self.iniciar_login, 0: self.retornar}
        self._continua = True
        while self._continua:
            opcao = self._tela_consumidor.cadastro_ou_login()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()   

    def minhas_reservas(self):
        self._controlador_sistema.controlador_reservas.abre_tela()

    def interface_consumidor(self):
        lista_opcoes = {1: self.minhas_reservas, 0: self.retornar}
        self._continua = True
        while self._continua:
            opcao = self._tela_consumidor.tela_opcoes()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()
            else:
                self._tela_consumidor.mensagem("Opção inválida.")