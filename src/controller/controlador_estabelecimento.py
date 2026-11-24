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
        # RN10: não permite atualizar CNPJ nem e-mail após o cadastro
        dados_permitidos = {
            k: v for k, v in (novos_dados or {}).items()
            if k not in ("cnpj", "email")
        }
        if not dados_permitidos:
            return False

        nome_antigo = estabelecimento.nome_fantasia
        loc_antiga = (
            (estabelecimento.cidade or "").strip(),
            (estabelecimento.bairro or "").strip(),
            (estabelecimento.endereco or "").strip(),
        )

        atualizado = self._metodos.atualizar_por_filtro(
            {"cnpj": estabelecimento.cnpj},
            dados_permitidos,
        )
        if atualizado:
            documento = self._metodos.buscar_um({"cnpj": estabelecimento.cnpj})
            novo = self._documento_para_estabelecimento(documento)
            self.__estabelecimentos = [
                est for est in self.__estabelecimentos
                if est.cnpj != estabelecimento.cnpj
            ]
            self.__estabelecimentos.append(novo)

            logado = self.__controlador_sistema.estabelecimento_logado
            if logado is not None and str(logado.cnpj).strip() == str(novo.cnpj).strip():
                self.__controlador_sistema.definir_estabelecimento_logado(novo)

            loc_nova = (
                (novo.cidade or "").strip(),
                (novo.bairro or "").strip(),
                (novo.endereco or "").strip(),
            )
            endereco_mudou = loc_nova != loc_antiga
            nome_mudou = novo.nome_fantasia != nome_antigo

            if endereco_mudou or nome_mudou:
                self.__controlador_sistema.controlador_oferta.atualizar_ofertas_do_estabelecimento(
                    novo,
                    nome_antigo=nome_antigo,
                    atualizar_localizacao=endereco_mudou,
                )
                self.__controlador_sistema.controlador_reservas.vincular_estabelecimento_nas_reservas(
                    novo,
                    nome_antigo=nome_antigo,
                )
            else:
                self.__controlador_sistema.vincular_estabelecimento(novo)
        return atualizado

    def editar_cadastro_estabelecimento(self, estabelecimento, dados):
        if estabelecimento is None or not dados:
            return False, "Erro: dados inválidos."

        # RN10: CNPJ e e-mail não podem ser alterados após o cadastro
        if "cnpj" in dados and str(dados["cnpj"]).strip() != str(estabelecimento.cnpj).strip():
            return False, "Erro: não é permitido alterar o CNPJ após o cadastro."
        if "email" in dados and str(dados["email"]).strip() != str(estabelecimento.email).strip():
            return False, "Erro: não é permitido alterar o e-mail após o cadastro."

        nome_fantasia = (dados.get("nome_fantasia") or dados.get("nome") or "").strip()
        endereco = (dados.get("endereco") or "").strip()
        bairro = (dados.get("bairro") or "").strip()
        cidade = (dados.get("cidade") or "").strip()
        tipo_valor = (dados.get("tipo") or "").strip()

        if not all([nome_fantasia, endereco, bairro, cidade, tipo_valor]):
            return False, "Preencha todos os campos obrigatórios."

        try:
            tipo = TipoEstabelecimento(tipo_valor)
        except ValueError:
            return False, "Erro: tipo de estabelecimento inválido."

        senha_atual = (dados.get("senha_atual") or "").strip()
        nova_senha = (dados.get("nova_senha") or "").strip()
        confirmar_senha = (dados.get("confirmar_senha") or "").strip()
        quer_alterar_senha = bool(senha_atual or nova_senha or confirmar_senha)

        if quer_alterar_senha:
            if not senha_atual or not nova_senha or not confirmar_senha:
                return False, "Para alterar a senha, preencha a senha atual, a nova senha e a confirmação."

            # RN12: atualização de senha exige inserção prévia da senha atual
            documento = self._metodos.buscar_um({"cnpj": estabelecimento.cnpj})
            senha_armazenada = documento["senha"] if documento else estabelecimento.senha
            if senha_atual != senha_armazenada:
                return False, "Erro: a senha atual informada está incorreta."

            if nova_senha != confirmar_senha:
                return False, "Erro: a nova senha e a confirmação não conferem."

            if nova_senha == senha_atual:
                return False, "Erro: a nova senha deve ser diferente da senha atual."

        endereco_mudou = (
            (estabelecimento.cidade or "").strip() != cidade
            or (estabelecimento.bairro or "").strip() != bairro
            or (estabelecimento.endereco or "").strip() != endereco
        )

        novos_dados = {
            "nome_fantasia": nome_fantasia,
            "tipo": tipo.value,
            "endereco": endereco,
            "localizacao": {
                "cidade": cidade,
                "bairro": bairro,
                "endereco": endereco,
            },
        }
        if quer_alterar_senha:
            novos_dados["senha"] = nova_senha

        atualizado = self.atualizar_estabelecimento(estabelecimento, novos_dados)
        if not atualizado:
            return False, "Não foi possível atualizar o perfil."

        if endereco_mudou and quer_alterar_senha:
            return True, "Perfil e senha atualizados com sucesso! A localização das suas ofertas ativas também foi atualizada."
        if endereco_mudou:
            return True, "Perfil atualizado com sucesso! A localização das suas ofertas ativas também foi atualizada."
        if quer_alterar_senha:
            return True, "Perfil e senha atualizados com sucesso!"
        return True, "Perfil atualizado com sucesso!"

    def perfil_estabelecimento(self):
        estabelecimento = self.__controlador_sistema.estabelecimento_logado
        if estabelecimento is None:
            return "ofertas"

        resultado = self.__tela_estabelecimento.perfil_estabelecimento(estabelecimento)
        if not isinstance(resultado, dict):
            return resultado

        _, msg = self.editar_cadastro_estabelecimento(estabelecimento, resultado["dados"])
        self.__tela_estabelecimento.mensagem(msg)
        return "perfil"

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

    def _navegar_abas(self, aba_atual):
        while aba_atual in ("retirada", "perfil"):
            if aba_atual == "retirada":
                aba_atual = self.__controlador_sistema.controlador_reservas.iniciar_validacao_resgate()
            elif aba_atual == "perfil":
                aba_atual = self.perfil_estabelecimento()

    def abrir_gerenciador_ofertas(self):
        opcoes_oferta = {
            1: self.__controlador_sistema._controlador_oferta.criarOferta,
            2: self.__controlador_sistema._controlador_oferta.listarOferta,
            3: self.__controlador_sistema._controlador_oferta.atualizarOferta,
            4: self.__controlador_sistema._controlador_oferta.excluirOferta,
            5: lambda: self._navegar_abas("retirada"),
            6: lambda: self._navegar_abas("perfil"),
        }

        while True:
            opcao = self.__tela_estabelecimento.menu_gerenciar_ofertas()
            if opcao == 0:
                self.__controlador_sistema.definir_estabelecimento_logado(None)
                print("\nLogout do estabelecimento efetuado.")
                break
            elif opcao == 7:
                continue
            elif opcao in opcoes_oferta:
                opcoes_oferta[opcao]()
            else:
                print("Opção inválida.")

# Feito por Gabriel
        