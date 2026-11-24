from datetime import datetime, timedelta
import unicodedata
from view.tela_resgate import TelaResgate
from view.tela_reserva import TelaReserva
from model.reserva import Reserva
from model.oferta_relampago import OfertaRelampago
from model.consumidor import Consumidor
from model.localizacao import Localizacao
from model.enums import StatusReserva, StatusOferta
from model.token import Token
from database.metodos import BaseMetodos


class ControladorReservas():

    def __init__(self, controlador_sistema):
        self._metodos = BaseMetodos("reservas")
        self._reservas = [self._documento_para_reserva(d) for d in self._metodos.listar()]
        self._tela_reserva = TelaReserva()
        self._controlador_sistema = controlador_sistema
        self._continua = True

    def _documento_para_reserva(self, dados):
        consumidor_dados = dados.get("consumidor", {})
        localizacao = consumidor_dados.get("localizacao", {})
        consumidor = Consumidor(
            bloqueadoAte=consumidor_dados.get("bloqueadoAte"),
            preferenciasAlimentares=consumidor_dados.get("preferenciasAlimentares", []),
            penalidade=consumidor_dados.get("penalidade", 0),
            dataCadastro=consumidor_dados.get("dataCadastro"),
            email=consumidor_dados.get("email", ""),
            id=consumidor_dados.get("id"),
            localizacao=Localizacao(
                localizacao.get("cidade", ""),
                localizacao.get("bairro", ""),
                localizacao.get("endereco", ""),
            ),
            nome=consumidor_dados.get("nome", ""),
            senha=consumidor_dados.get("senha", ""),
        )
        oferta_dados = dados["oferta"]
        oferta = OfertaRelampago(
            oferta_dados["id"],
            oferta_dados["titulo"],
            oferta_dados["descricao"],
            oferta_dados["nome_estabelecimento"],
            oferta_dados["original"],
            oferta_dados["desconto"],
            oferta_dados["quantidade"],
            oferta_dados["inicio"],
            oferta_dados["fim"],
        )
        oferta.status = StatusOferta(oferta_dados.get("status", StatusOferta.DISPONIVEL.value))
        token_dados = dados["token"]
        token = Token(
            token_dados["codigo"],
            token_dados.get("data_geracao"),
            token_dados.get("usado", False),
        )
        reserva = Reserva(
            dados["id"],
            consumidor,
            oferta,
            dados["data_hora_limite_retirada"],
            dados["data_hora_reserva"],
            StatusReserva(dados["status"]),
            token,
        )
        reserva._estabelecimento_id = dados.get("estabelecimento_id")
        reserva._estoque_reservado = bool(dados.get("estoque_reservado", False))
        return reserva

    def recarregar_reservas(self):
        self._reservas = [self._documento_para_reserva(d) for d in self._metodos.listar()]

    def _normalizar_nome(self, nome):
        texto = unicodedata.normalize("NFKD", (nome or "").strip())
        sem_acento = "".join(c for c in texto if not unicodedata.combining(c))
        return sem_acento.casefold()

    def _reserva_para_documento(self, reserva, estabelecimento=None):
        consumidor = reserva.consumidor
        oferta = reserva.oferta
        estabelecimento_id = estabelecimento.cnpj if estabelecimento else oferta.nome_estabelecimento
        return {
            "id": reserva.id,
            "consumidor_id": consumidor.id,
            "consumidor": {
                "id": consumidor.id,
                "nome": consumidor.nome,
                "email": consumidor.email,
                "senha": consumidor.senha,
                "dataCadastro": consumidor.data_cadastro,
                "localizacao": {
                    "cidade": consumidor.localizacao.cidade,
                    "bairro": consumidor.localizacao.bairro,
                    "endereco": consumidor.localizacao.endereco,
                },
                "preferenciasAlimentares": consumidor.preferenciasAlimentares,
                "penalidade": consumidor.penalidade,
                "bloqueadoAte": consumidor.bloqueadoAte,
            },
            "estabelecimento_id": estabelecimento_id,
            "oferta": {
                "id": oferta.id,
                "titulo": oferta.titulo,
                "descricao": oferta.descricao,
                "nome_estabelecimento": oferta.nome_estabelecimento,
                "original": oferta.original,
                "desconto": oferta.desconto,
                "quantidade": oferta.quantidade,
                "inicio": oferta.inicio,
                "fim": oferta.fim,
                "status": oferta.status.value,
            },
            "data_hora_limite_retirada": reserva.data_hora_limite_retirada,
            "data_hora_reserva": reserva.data_hora_reserva,
            "status": reserva.status.value,
            "estoque_reservado": bool(getattr(reserva, "_estoque_reservado", False)),
            "token": {
                "codigo": reserva.token.codigo,
                "data_geracao": reserva.token.data_geracao,
                "usado": reserva.token.usado,
            },
        }

    def criar_reserva_de_oferta(self, oferta, estabelecimento=None):
        consumidor = self._controlador_sistema.consumidor_logado
        if consumidor is None:
            return None

        # RF16: impedir que consumidores bloqueados realizem novas reservas
        if consumidor.bloqueadoAte and datetime.now() < consumidor.bloqueadoAte:
            self._tela_reserva.mostra_mensagem(
                f"Sua conta está bloqueada até {consumidor.bloqueadoAte.strftime('%d/%m/%Y %H:%M')} e não pode realizar reservas."
            )
            return None

        self.recarregar_reservas()
        ctrl_of = self._controlador_sistema.controlador_oferta
        ctrl_of.recarregar_ofertas()
        oferta_atual = ctrl_of.buscar_oferta(oferta.id, oferta.nome_estabelecimento)
        if oferta_atual is None:
            self._tela_reserva.mostra_mensagem("Oferta não encontrada.")
            return None

        # RN02: mesma cidade e bairro
        compat, _, est_resolvido = ctrl_of._oferta_no_bairro_do_consumidor(oferta_atual, consumidor)
        estabelecimento = estabelecimento or est_resolvido
        if not compat:
            self._tela_reserva.mostra_mensagem(
                "Você só pode reservar ofertas de estabelecimentos no mesmo bairro e cidade do seu cadastro."
            )
            return None

        if oferta_atual.status != StatusOferta.DISPONIVEL or oferta_atual.quantidade <= 0:
            self._tela_reserva.mostra_mensagem("Esta oferta está esgotada ou indisponível no momento.")
            return None

        # RN03: apenas 1 reserva por estabelecimento por dia para o mesmo consumidor
        hoje = datetime.now().date()
        alvo_estab = self._normalizar_nome(oferta_atual.nome_estabelecimento)
        estab_cnpj = str(estabelecimento.cnpj).strip() if estabelecimento else None
        for r in self._reservas:
            if r.consumidor.id != consumidor.id or r.status == StatusReserva.CANCELADA:
                continue
            if not isinstance(r.data_hora_reserva, datetime) or r.data_hora_reserva.date() != hoje:
                continue
            mesmo_nome = self._normalizar_nome(r.oferta.nome_estabelecimento) == alvo_estab
            estab_doc_id = getattr(r, "_estabelecimento_id", None)
            mesmo_cnpj = estab_cnpj and estab_doc_id and str(estab_doc_id).strip() == estab_cnpj
            if mesmo_nome or mesmo_cnpj:
                self._tela_reserva.mostra_mensagem(
                    f"Você já realizou uma reserva em '{oferta_atual.nome_estabelecimento}' hoje (limite de 1 por dia por estabelecimento)."
                )
                return None

        agora = datetime.now()
        if isinstance(oferta_atual.fim, datetime) and oferta_atual.fim.year > 1900:
            limite_retirada = oferta_atual.fim
        elif isinstance(oferta_atual.fim, datetime):
            limite_retirada = agora.replace(
                hour=oferta_atual.fim.hour,
                minute=oferta_atual.fim.minute,
                second=0,
                microsecond=0,
            )
            if limite_retirada <= agora:
                limite_retirada = limite_retirada + timedelta(days=1)
        else:
            limite_retirada = agora + timedelta(hours=3)

        novo_id = max((r.id for r in self._reservas if isinstance(r.id, int)), default=0) + 1
        nova_reserva = Reserva(
            novo_id,
            consumidor,
            oferta_atual,
            limite_retirada,
            data_hora_reserva=agora,
        )
        nova_reserva._estabelecimento_id = estabelecimento.cnpj if estabelecimento else oferta_atual.nome_estabelecimento
        nova_reserva._estoque_reservado = True

        ctrl_of.reservar_estoque_oferta(oferta_atual, estabelecimento)
        self._metodos.inserir(self._reserva_para_documento(nova_reserva, estabelecimento))
        self._reservas.append(nova_reserva)

        self._tela_reserva.mostra_mensagem(
            f"Reserva #{nova_reserva.id} confirmada!\n"
            f"Oferta: {oferta_atual.titulo}\n"
            f"Estabelecimento: {oferta_atual.nome_estabelecimento}\n"
            f"Código de retirada (token): {nova_reserva.token.codigo}"
        )
        return nova_reserva

    def todas_reservas(self):
        return list(self._reservas)

    def vincular_estabelecimento_nas_reservas(self, estabelecimento):
        alvo = self._normalizar_nome(estabelecimento.nome_fantasia)
        for reserva in self._reservas:
            if self._normalizar_nome(reserva.oferta.nome_estabelecimento) == alvo:
                reserva.oferta.nome_estabelecimento = estabelecimento.nome_fantasia
                self._metodos.atualizar_por_filtro(
                    {"id": reserva.id, "consumidor_id": reserva.consumidor.id},
                    {
                        "estabelecimento_id": estabelecimento.cnpj,
                        "oferta.nome_estabelecimento": estabelecimento.nome_fantasia,
                    },
                )

    def adicionar_reserva(self, reserva):
        estabelecimento = self._controlador_sistema.controlador_estabelecimento.buscar_por_nome_fantasia(
            reserva.oferta.nome_estabelecimento
        )
        if estabelecimento is not None:
            reserva.oferta.nome_estabelecimento = estabelecimento.nome_fantasia
        self._controlador_sistema.controlador_oferta.registrar_oferta_se_nao_existir(
            reserva.oferta, estabelecimento
        )
        if not self._metodos.buscar_um({
            "id": reserva.id,
            "consumidor_id": reserva.consumidor.id,
        }):
            self._metodos.inserir(self._reserva_para_documento(reserva, estabelecimento))
        if not any(
            r.id == reserva.id and r.consumidor.id == reserva.consumidor.id
            for r in self._reservas
        ):
            self._reservas.append(reserva)

    def possui_reservas_do_consumidor(self, consumidor_id):
        return self._metodos.buscar_um({"consumidor_id": consumidor_id}) is not None

    def atualizar_reserva(self, reserva_id, consumidor_id, novos_dados):
        atualizado = self._metodos.atualizar_por_filtro(
            {"id": reserva_id, "consumidor_id": consumidor_id},
            novos_dados,
        )
        if atualizado:
            for reserva in self._reservas:
                if reserva.id == reserva_id and reserva.consumidor.id == consumidor_id:
                    if "status" in novos_dados:
                        reserva.status = StatusReserva(novos_dados["status"])
                    break
        return atualizado

    def excluir_reserva(self, reserva_id, consumidor_id):
        excluido = self._metodos.deletar_por_filtro({
            "id": reserva_id,
            "consumidor_id": consumidor_id,
        })
        if excluido:
            self._reservas = [
                reserva for reserva in self._reservas
                if not (
                    reserva.id == reserva_id
                    and reserva.consumidor.id == consumidor_id
                )
            ]
        return excluido

    def pega_reservas_do_consumidor(self, id_consumidor=None):
        if id_consumidor is None:
            consumidor = self._controlador_sistema.consumidor_logado
            if consumidor is None:
                return []
            id_consumidor = consumidor.id
        return [r for r in self._reservas if r.consumidor.id == id_consumidor]

    def pega_reserva_por_id(self, id: int):
        for reserva in self.pega_reservas_do_consumidor():
            if reserva.id == id:
                return reserva
        return None

    def pega_reservas_da_oferta(self, id_oferta, nome_estabelecimento=None, estabelecimento_id=None):
        alvo_nome = self._normalizar_nome(nome_estabelecimento) if nome_estabelecimento is not None else None
        alvo_id = str(estabelecimento_id).strip() if estabelecimento_id is not None else None
        id_alvo = str(id_oferta).strip()
        resultado = []
        for r in self._reservas:
            if str(r.oferta.id).strip() != id_alvo:
                continue
            if alvo_nome is None and alvo_id is None:
                resultado.append(r)
                continue
            mesmo_nome = (
                alvo_nome is not None
                and self._normalizar_nome(r.oferta.nome_estabelecimento) == alvo_nome
            )
            estab_doc_id = getattr(r, "_estabelecimento_id", None)
            mesmo_estab_id = (
                alvo_id is not None
                and estab_doc_id is not None
                and str(estab_doc_id).strip() == alvo_id
            )
            if mesmo_nome or mesmo_estab_id:
                resultado.append(r)
        return resultado

    def verificar_reserva(self, id, nome_estabelecimento=None, estabelecimento_id=None):
        self.recarregar_reservas()
        return len(self.pega_reservas_da_oferta(id, nome_estabelecimento, estabelecimento_id)) > 0

    def _dados_reserva(self, reserva):
        oferta = reserva.oferta
        return {"id": reserva.id,
                "status": reserva.status.value,
                "token": reserva.token.codigo,
                "titulo": oferta.titulo,
                "descricao": oferta.descricao,
                "estabelecimento": oferta.nome_estabelecimento,
                "preco": oferta.desconto,
                "preco_original": oferta.original,
                "data_reserva": reserva.data_hora_reserva,
                "limite_retirada": reserva.data_hora_limite_retirada}

    def lista_reservas(self):
        reservas = self.pega_reservas_do_consumidor()
        atuais = [r for r in reservas if r.esta_pendente()]
        anteriores = [r for r in reservas if not r.esta_pendente()]

        self._tela_reserva.mostra_titulo("RESERVAS ATUAIS")
        if len(atuais) == 0:
            self._tela_reserva.mostra_mensagem("Voce nao possui reservas atuais.\n")
        for reserva in atuais:
            self._tela_reserva.mostra_reserva(self._dados_reserva(reserva))

        self._tela_reserva.mostra_titulo("RESERVAS ANTERIORES")
        if len(anteriores) == 0:
            self._tela_reserva.mostra_mensagem("Voce nao possui reservas anteriores.\n")
        for reserva in anteriores:
            self._tela_reserva.mostra_reserva(self._dados_reserva(reserva))

    def consultar_reserva(self):
        self.lista_reservas()
        id_reserva = self._tela_reserva.seleciona_reserva()
        reserva = self.pega_reserva_por_id(id_reserva)

        if reserva is None:
            self._tela_reserva.mostra_mensagem("ATENCAO: Reserva nao existente")
            return

        self._tela_reserva.mostra_reserva_detalhes(self._dados_reserva(reserva))

        if reserva.esta_pendente() and self._tela_reserva.pergunta_cancelamento():
            self.cancelar_reserva(reserva)

    def cancelar_reserva(self, reserva):
        if not reserva.esta_pendente():
            self._tela_reserva.mostra_mensagem("Nao e possivel cancelar: a reserva nao esta com o status pendente.")
        elif not reserva.esta_dentro_do_prazo_de_cancelamento():
            self._tela_reserva.mostra_mensagem("O prazo para o cancelamento da reserva acabou (minimo de 1 hora de antecedencia).")
        else:
            reserva.cancelar()
            self._metodos.atualizar_varios(
                {"id": reserva.id, "consumidor_id": reserva.consumidor.id},
                {"status": reserva.status.value},
            )
            if getattr(reserva, "_estoque_reservado", False):
                self._controlador_sistema.controlador_oferta.devolver_estoque_oferta(reserva.oferta)
            self._tela_reserva.mostra_mensagem("Reserva cancelada com sucesso!")

    def retornar(self):
        self._continua = False

    def iniciar_validacao_resgate(self):
        # Feito por Augusto
        
        tela = TelaResgate()
        codigo = tela.solicitar_token()
        self.validar_resgate(codigo)

    def abre_tela(self):
        self._continua = True
        while self._continua:
            self.recarregar_reservas()
            reservas = self.pega_reservas_do_consumidor()
            atuais = [self._dados_reserva(r) for r in reservas if r.esta_pendente()]
            anteriores = [self._dados_reserva(r) for r in reservas if not r.esta_pendente()]

            acao, id_reserva = self._tela_reserva.exibir_painel_reservas(atuais, anteriores)

            if acao == "voltar":
                self._continua = False
                return "menu"
            elif acao == "explorar":
                self._continua = False
                return "explorar"
            elif acao == "perfil":
                self._continua = False
                return "perfil"
            elif acao == "atualizar":
                continue
            elif acao == "em_breve":
                self._tela_reserva.mostra_mensagem("Funcionalidade em desenvolvimento.")
            elif acao == "detalhes":
                reserva = self.pega_reserva_por_id(id_reserva)
                if reserva:
                    self._tela_reserva.mostra_reserva_detalhes(self._dados_reserva(reserva))
            elif acao == "cancelar":
                reserva = self.pega_reserva_por_id(id_reserva)
                if reserva and self._tela_reserva.pergunta_cancelamento():
                    self.cancelar_reserva(reserva)
        return "menu"

    def validar_resgate(self, codigo: str):
        # Feito por Augusto

        self.recarregar_reservas()
        tela = TelaResgate()

        estabelecimento = self._controlador_sistema.estabelecimento_logado
        alvo = self._normalizar_nome(estabelecimento.nome_fantasia) if estabelecimento is not None else ""
        reserva = next(
            (
                reserva
                for reserva in self._reservas
                if estabelecimento is not None
                and self._normalizar_nome(reserva.oferta.nome_estabelecimento) == alvo
                and reserva.token.codigo == codigo
            ),
            None,
        )

        if reserva is None:
            tela.mostra_mensagem(
                "Atenção: Reserva não localizada ou não pertence a este estabelecimento."
            )
            return

        if reserva.confirmarRetirada(codigo):
            self._metodos.atualizar_varios(
                {"id": reserva.id, "consumidor_id": reserva.consumidor.id},
                {
                    "estabelecimento_id": estabelecimento.cnpj,
                    "status": reserva.status.value,
                    "token": {
                        "codigo": reserva.token.codigo,
                        "data_geracao": reserva.token.data_geracao,
                        "usado": reserva.token.usado,
                    },
                },
            )
            self._controlador_sistema.controlador_oferta.registrar_resgate_oferta(
                reserva.oferta,
                estabelecimento,
                decrementar_estoque=not getattr(reserva, "_estoque_reservado", False),
            )
            tela.mostra_mensagem("Resgate validado com sucesso!")
        else:
            if reserva.status == StatusReserva.EXPIRADA:
                self._metodos.atualizar_varios(
                    {"id": reserva.id, "consumidor_id": reserva.consumidor.id},
                    {"status": reserva.status.value},
                )
            tela.mostra_mensagem("Erro: Token inválido ou expirado.")

    def atualizar_status_reserva(self, id_reserva: str, novo_status: str):
        return self._metodos.atualizar(id_reserva, {"status": novo_status})
    #Feito por Gabriel
# feito por matheus
