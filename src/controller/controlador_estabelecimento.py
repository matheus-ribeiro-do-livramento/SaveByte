from view.tela_estabelecimento import TelaEstabelecimento
from model.estabelecimento import Estabelecimento
from model.localizacao import Localizacao
from model.enums import TipoEstabelecimento
from database.metodos import BaseMetodos

class ControladorEstabelecimento ():

    def __init__(self, controlador_sistema):
        self._metodos = BaseMetodos("estabelecimentos")
        self.__estabelecimentos = [self._documento_para_estabelecimento(d) for d in self._metodos.listar()]
        self.__controlador_sistema = controlador_sistema
        self.__tela_estabelecimento = TelaEstabelecimento()
        self._continua = True

    def _documento_para_estabelecimento(self, dados):
        tipo = TipoEstabelecimento(dados.get("tipo", "padaria"))
        loc = dados.get("localizacao") or {}
        endereco = loc.get("endereco") or dados.get("endereco", "")
        cidade = loc.get("cidade") or dados.get("cidade", "")
        bairro = loc.get("bairro") or dados.get("bairro", "")
        return Estabelecimento(
            dados["cnpj"],
            endereco,
            dados["nome_fantasia"],
            tipo,
            dados["senha"],
            dados["email"],
            cidade=cidade,
            bairro=bairro,
        )

    def _estabelecimento_para_documento(self, estabelecimento):
        tipo = estabelecimento.tipo.value if isinstance(estabelecimento.tipo, TipoEstabelecimento) else str(estabelecimento.tipo)
        return {
            "cnpj": estabelecimento.cnpj,
            "endereco": estabelecimento.endereco,
            "localizacao": {
                "cidade": estabelecimento.cidade,
                "bairro": estabelecimento.bairro,
                "endereco": estabelecimento.endereco,
            },
            "nome_fantasia": estabelecimento.nome_fantasia,
            "tipo": tipo,
            "senha": estabelecimento.senha,
            "email": estabelecimento.email,
        }

    def iniciarCadastro(self):
        dados = self.__tela_estabelecimento.pegaDadosEstabelecimento()
        if dados is None:
            return

        certo = self.cadastrarEstabelecimento(dados)

        if (certo):
            return self.__tela_estabelecimento.mensagem('Cadastro efetuado com sucesso')
        else:
            return self.__tela_estabelecimento.mensagem('Erro: CNPJ ou E-mail já em uso')
            
    

    def cadastrarEstabelecimento (self, dados):
        if dados is None:
            return False
        if self._metodos.buscar_um({
            "$or": [
                {"email": dados["email"]},
                {"cnpj": dados["cnpj"]},
            ]
        }):
            return False
        tipo = TipoEstabelecimento(dados["tipo"])
        estabelecimento = Estabelecimento(dados["cnpj"],
                                          dados["endereco"], 
                                          dados["nome"], 
                                          tipo,
                                          dados["senha"], 
                                          dados["email"],
                                          cidade=dados.get("cidade", ""),
                                          bairro=dados.get("bairro", ""))
        
        self._metodos.inserir(self._estabelecimento_para_documento(estabelecimento))
        self.__estabelecimentos.append(estabelecimento)
        self.__controlador_sistema.vincular_estabelecimento(estabelecimento)
        return True

    def recarregar_estabelecimentos(self):
        self.__estabelecimentos = [self._documento_para_estabelecimento(d) for d in self._metodos.listar()]

    def listar_estabelecimentos(self):
        return list(self.__estabelecimentos)

    def buscar_por_nome_fantasia(self, nome_fantasia: str):
        alvo = (nome_fantasia or "").strip().casefold()
        for est in self.__estabelecimentos:
            if (est.nome_fantasia or "").strip().casefold() == alvo:
                return est
        return None

    def buscar_por_cnpj(self, cnpj: str):
        alvo = str(cnpj or "").strip()
        for est in self.__estabelecimentos:
            if str(est.cnpj).strip() == alvo:
                return est
        return None

    def iniciarLogin(self):
        dados = self.__tela_estabelecimento.pegaDadosLogin()

        estabelecimento_logado = self.realizarLogin(dados)

        if estabelecimento_logado:
            self.__tela_estabelecimento.mensagem(f'\n Login efetuado com sucesso! \n Bem vindo, {estabelecimento_logado.nome_fantasia}')
            return estabelecimento_logado
        else:
            self.__tela_estabelecimento.mensagem('Erro: e-mail ou senha invalidos')

            return None

    def retornar(self):
        self._continua = False

    def realizarLogin (self, dados):
        documento = self._metodos.buscar_um({
            "email": dados["email"],
            "senha": dados["senha"],
        })
        if documento:
            return self._documento_para_estabelecimento(documento)
        return None

    def atualizar_estabelecimento(self, estabelecimento, novos_dados):
        atualizado = self._metodos.atualizar_por_filtro(
            {"cnpj": estabelecimento.cnpj},
            novos_dados,
        )
        if atualizado:
            documento = self._metodos.buscar_um({"cnpj": estabelecimento.cnpj})
            novo = self._documento_para_estabelecimento(documento)
            self.__estabelecimentos = [
                est for est in self.__estabelecimentos
                if est.cnpj != estabelecimento.cnpj
            ]
            self.__estabelecimentos.append(novo)
            self.__controlador_sistema.vincular_estabelecimento(novo)
        return atualizado

    def excluir_estabelecimento(self, cnpj):
        excluido = self._metodos.deletar_por_filtro({"cnpj": cnpj})
        if excluido:
            self.__estabelecimentos = [
                est for est in self.__estabelecimentos if est.cnpj != cnpj
            ]
        return excluido

    def abre_tela_cadastro_ou_login(self):
        lista_opcoes = {1: self.iniciarCadastro, 
                        2: self.logar_estabelecimento, 
                        0: self.retornar}
        
        self._continua = True
        while self._continua:
            opcao = self.__tela_estabelecimento.cadastro_ou_login()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()
            else:
                print("Opção inválida")

    def logar_estabelecimento(self):
        user = self.iniciarLogin()
        if user:
            if not user.bairro.strip() or not user.cidade.strip():
                loc = self.__tela_estabelecimento.completar_localizacao(
                    user.nome_fantasia,
                    user.endereco,
                    user.bairro,
                    user.cidade,
                )
                if loc:
                    user.endereco = loc["endereco"]
                    user.bairro = loc["bairro"]
                    user.cidade = loc["cidade"]
                    self.atualizar_estabelecimento(
                        user,
                        {
                            "endereco": user.endereco,
                            "localizacao": {
                                "cidade": user.cidade,
                                "bairro": user.bairro,
                                "endereco": user.endereco,
                            },
                        },
                    )
            self.__controlador_sistema.definir_estabelecimento_logado(user)
            self.__controlador_sistema.vincular_estabelecimento(user)
            self.abrir_gerenciador_ofertas()

    def abrir_gerenciador_ofertas(self):
            
            opcoes_oferta = {
                1: self.__controlador_sistema._controlador_oferta.criarOferta,
                2: self.__controlador_sistema._controlador_oferta.listarOferta,
                3: self.__controlador_sistema._controlador_oferta.atualizarOferta,
                4: self.__controlador_sistema._controlador_oferta.excluirOferta,
                5: self.__controlador_sistema.controlador_reservas.iniciar_validacao_resgate,
            }
    
            while True:
                opcao = self.__tela_estabelecimento.menu_gerenciar_ofertas()
                if opcao == 0:
                    self.__controlador_sistema.definir_estabelecimento_logado(None)
                    print("\nLogout do estabelecimento efetuado.")
                    break
                elif opcao in opcoes_oferta:
                    opcoes_oferta[opcao]()
                else:
                    print("Opção inválida.")

# Feito por Gabriel
        