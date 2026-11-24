from view.tela_consumidor import TelaConsumidor
from model.consumidor import Consumidor
from model.localizacao import Localizacao
from datetime import datetime
from database.metodos import BaseMetodos

class ControladorConsumidor:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self._tela_consumidor = TelaConsumidor()
        self._metodos = BaseMetodos("consumidores")
        self._consumidor = [self._documento_para_consumidor(d) for d in self._metodos.listar()]
        self._continua = True

    def _documento_para_consumidor(self, dados):
        localizacao = dados.get("localizacao", {})
        return Consumidor(
            bloqueadoAte=dados.get("bloqueadoAte"),
            preferenciasAlimentares=dados.get("preferenciasAlimentares", []),
            penalidade=dados.get("penalidade", 0),
            dataCadastro=dados.get("dataCadastro"),
            email=dados["email"],
            id=dados["id"],
            localizacao=Localizacao(
                localizacao.get("cidade", ""),
                localizacao.get("bairro", ""),
                localizacao.get("endereco", ""),
            ),
            nome=dados["nome"],
            senha=dados["senha"],
        )

    def _consumidor_para_documento(self, consumidor):
        return {
            "id": consumidor.id,
            "nome": consumidor.nome,
            "email": consumidor.email,
            "senha": consumidor.senha,
            "localizacao": {
                "cidade": consumidor.localizacao.cidade,
                "bairro": consumidor.localizacao.bairro,
                "endereco": consumidor.localizacao.endereco,
            },
            "bloqueadoAte": consumidor.bloqueadoAte,
            "preferenciasAlimentares": consumidor.preferenciasAlimentares,
            "penalidade": consumidor.penalidade,
            "dataCadastro": consumidor.data_cadastro,
        }

    def cadastrar_consumidor(self, dados):
        if dados is None:
            return False
        if self._metodos.buscar_um({"email": dados["email"]}):
            return False

        maior_id = max((con.id for con in self._consumidor), default=0)
        consumidor = Consumidor(
            bloqueadoAte=None,
            preferenciasAlimentares=[],
            penalidade=0,
            dataCadastro=None,
            email=dados["email"],
            id=maior_id + 1,
            localizacao=Localizacao(dados["cidade"], dados["bairro"], dados["endereco"]),
            nome=dados["nome"],
            senha=dados["senha"],
        )
        self._metodos.inserir(self._consumidor_para_documento(consumidor))
        self._consumidor.append(consumidor)
        return True

    def buscar_por_id(self, id_consumidor: str):
        dados = self._bd.buscar_por_id(id_consumidor)
        if not dados:
            return None
        return Consumidor.from_dict(dados)

    def iniciar_cadastro(self):
        
        dados = self._tela_consumidor.cadastro_consumidor()
        if self.cadastrar_consumidor(dados):
            self._tela_consumidor.mensagem("Cadastro efetuado com sucesso!")
            return True
        self._tela_consumidor.mensagem("Erro: dados inválidos.")
        return False

    def realizar_login(self, dados):
        documento = self._metodos.buscar_um({
            "email": dados["email"],
            "senha": dados["senha"],
        })
        if documento:
            return self._documento_para_consumidor(documento)
        return None

    def atualizar_consumidor(self, consumidor, novos_dados):
        documento = self._consumidor_para_documento(consumidor)
        documento.update(novos_dados)
        atualizado = self._metodos.atualizar_por_filtro(
            {"id": consumidor.id},
            novos_dados,
        )
        if atualizado:
            self._consumidor = [
                con for con in self._consumidor if con.id != consumidor.id
            ]
            self._consumidor.append(self._documento_para_consumidor(
                self._metodos.buscar_um({"id": consumidor.id})
            ))
        return atualizado

    def excluir_consumidor(self, consumidor_id):
        excluido = self._metodos.deletar_por_filtro({"id": consumidor_id})
        if excluido:
            self._consumidor = [
                con for con in self._consumidor if con.id != consumidor_id
            ]
        return excluido

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

    def bloquear_consumidor(self, id_consumidor: str, bloqueado_ate: datetime):
        return self._bd.atualizar(
            id_consumidor,
            {
                "status": "BLOQUEADO",
                "bloqueado_ate": bloqueado_ate,
            },
        )

    def desbloquear_consumidor(self, id_consumidor: str):
        return self._bd.atualizar(
            id_consumidor,
            {
                "status": "ATIVO",
                "bloqueado_ate": None,
            },
        )
#Feito por matheus