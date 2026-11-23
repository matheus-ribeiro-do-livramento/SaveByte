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
        return reserva

    def _reserva_para_documento(self, reserva):
        consumidor = reserva.consumidor
        oferta = reserva.oferta
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
            "estabelecimento_id": oferta.nome_estabelecimento,
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
            "token": {
                "codigo": reserva.token.codigo,
                "data_geracao": reserva.token.data_geracao,
                "usado": reserva.token.usado,
            },
        }

    def adicionar_reserva(self, reserva):
        if not self._metodos.buscar_um({
            "id": reserva.id,
            "consumidor_id": reserva.consumidor.id,
        }):
            self._metodos.inserir(self._reserva_para_documento(reserva))
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

    def pega_reservas_do_consumidor(self):
        consumidor = self._controlador_sistema.consumidor_logado
        return [r for r in self._reservas if r.consumidor.id == consumidor.id]

    def pega_reserva_por_id(self, id: int):
        for reserva in self.pega_reservas_do_consumidor():
            if reserva.id == id:
                return reserva
        return None

    def verificar_reserva(self, id):
        for r in self._reservas:
            if r.oferta.id == id:
                return True
        return False

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
                {"id": reserva.id},
                {"status": reserva.status.value},
            )
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
            reservas = self.pega_reservas_do_consumidor()
            atuais = [self._dados_reserva(r) for r in reservas if r.esta_pendente()]
            anteriores = [self._dados_reserva(r) for r in reservas if not r.esta_pendente()]

            acao, id_reserva = self._tela_reserva.exibir_painel_reservas(atuais, anteriores)

            if acao == "voltar":
                self._continua = False
            elif acao == "detalhes":
                reserva = self.pega_reserva_por_id(id_reserva)
                if reserva:
                    self._tela_reserva.mostra_reserva_detalhes(self._dados_reserva(reserva))
            elif acao == "cancelar":
                reserva = self.pega_reserva_por_id(id_reserva)
                if reserva and self._tela_reserva.pergunta_cancelamento():
                    self.cancelar_reserva(reserva)

    def validar_resgate(self, codigo: str):
        # Feito por Augusto

        tela = TelaResgate()

        estabelecimento = self._controlador_sistema.estabelecimento_logado
        reserva = next(
            (
                reserva
                for reserva in self._reservas
                if estabelecimento is not None
                and reserva.oferta.nome_estabelecimento == estabelecimento.nome_fantasia
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
                {"id": reserva.id},
                {
                    "status": reserva.status.value,
                    "token": {
                        "codigo": reserva.token.codigo,
                        "data_geracao": reserva.token.data_geracao,
                        "usado": reserva.token.usado,
                    },
                },
            )
            tela.mostra_mensagem("Resgate validado com sucesso!")
        else:
            if reserva.status == StatusReserva.EXPIRADA:
                self._metodos.atualizar_varios(
                    {"id": reserva.id},
                    {"status": reserva.status.value},
                )
            tela.mostra_mensagem("Erro: Token inválido ou expirado.")


# feito por matheus
