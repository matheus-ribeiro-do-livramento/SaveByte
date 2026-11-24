from datetime import datetime
from view.tela_ofertaRelampago import TelaOfertaRelampago
from model.oferta_relampago import OfertaRelampago
from model.enums import StatusOferta, StatusReserva
from database.metodos import BaseMetodos

class ControladorOfertaRelampago():

    def __init__(self, controlador_sistema):
        self._metodos = BaseMetodos("ofertas_relampago")
        self._ofertas = [self._documento_para_oferta(d) for d in self._metodos.listar()]
        self._telaOferta = TelaOfertaRelampago()
        self._controlador_sistema = controlador_sistema

    def _documento_para_oferta(self, dados):
        oferta = OfertaRelampago(
            dados["id"],
            dados["titulo"],
            dados["descricao"],
            dados["nome_estabelecimento"],
            dados["original"],
            dados["desconto"],
            dados["quantidade"],
            dados["inicio"],
            dados["fim"],
        )
        oferta.status = StatusOferta(dados.get("status", StatusOferta.DISPONIVEL.value))
        return oferta

    def _oferta_para_documento(self, oferta, estabelecimento=None):
        return {
            "id": oferta.id,
            "titulo": oferta.titulo,
            "descricao": oferta.descricao,
            "nome_estabelecimento": oferta.nome_estabelecimento,
            "estabelecimento_id": estabelecimento.cnpj if estabelecimento else oferta.nome_estabelecimento,
            "original": oferta.original,
            "desconto": oferta.desconto,
            "quantidade": oferta.quantidade,
            "inicio": oferta.inicio,
            "fim": oferta.fim,
            "status": oferta.status.value if isinstance(oferta.status, StatusOferta) else str(oferta.status),
        }

    def _normalizar_nome(self, nome):
        return (nome or "").strip().casefold()

    def _oferta_expirada_por_tempo(self, oferta):
        return (
            isinstance(oferta.fim, datetime)
            and oferta.fim.year > 1900
            and datetime.now() > oferta.fim
        )

    def _atualizar_status_expiradas(self):
        for of in self._ofertas:
            if of.status == StatusOferta.DISPONIVEL and self._oferta_expirada_por_tempo(of):
                of.status = StatusOferta.EXPIRADA
                self._metodos.atualizar_varios(
                    {"id": of.id, "nome_estabelecimento": of.nome_estabelecimento},
                    {"status": of.status.value},
                )

    def recarregar_ofertas(self):
        self._ofertas = [self._documento_para_oferta(d) for d in self._metodos.listar()]
        self._atualizar_status_expiradas()

    def _motivo_bloqueio_modificacao(self, oferta, estabelecimento=None, acao="modificar"):
        self._controlador_sistema.controlador_reservas.recarregar_reservas()
        self._atualizar_status_expiradas()

        estab_id = estabelecimento.cnpj if estabelecimento else None
        reservas = self._controlador_sistema.controlador_reservas.pega_reservas_da_oferta(
            oferta.id, oferta.nome_estabelecimento, estabelecimento_id=estab_id
        )

        if any(r.status == StatusReserva.PENDENTE for r in reservas):
            return f"Não é possível {acao} esta oferta: ela já possui reserva PENDENTE."
        if any(r.status == StatusReserva.RETIRADA for r in reservas):
            return f"Não é possível {acao} esta oferta: ela já possui reserva RETIRADA."
        if any(r.status == StatusReserva.EXPIRADA for r in reservas):
            return f"Não é possível {acao} esta oferta: ela já possui reserva EXPIRADA."
        if any(r.status == StatusReserva.CANCELADA for r in reservas):
            return f"Não é possível {acao} esta oferta: ela já possui reserva CANCELADA."
        if reservas:
            return f"Não é possível {acao} esta oferta: ela já possui reserva registrada."
        if self._oferta_expirada_por_tempo(oferta) or oferta.status == StatusOferta.EXPIRADA:
            return f"Não é possível {acao} esta oferta: a oferta já está EXPIRADA."
        if oferta.status != StatusOferta.DISPONIVEL:
            return f"Não é possível {acao} esta oferta: status atual é {oferta.status.value.upper()}."
        return None

    def buscar_oferta(self, id_oferta, nome_estabelecimento):
        alvo = self._normalizar_nome(nome_estabelecimento)
        id_alvo = str(id_oferta).strip()
        for of in self._ofertas:
            if str(of.id).strip() == id_alvo and self._normalizar_nome(of.nome_estabelecimento) == alvo:
                return of
        return None

    def registrar_oferta_se_nao_existir(self, oferta_origem, estabelecimento=None):
        existente = self.buscar_oferta(oferta_origem.id, oferta_origem.nome_estabelecimento)
        if existente is not None:
            return existente

        if estabelecimento is None:
            estabelecimento = self._controlador_sistema.controlador_estabelecimento.buscar_por_nome_fantasia(
                oferta_origem.nome_estabelecimento
            )

        nome_estab = estabelecimento.nome_fantasia if estabelecimento else oferta_origem.nome_estabelecimento
        nova_oferta = OfertaRelampago(
            oferta_origem.id,
            oferta_origem.titulo,
            oferta_origem.descricao,
            nome_estab,
            oferta_origem.original,
            oferta_origem.desconto,
            oferta_origem.quantidade,
            oferta_origem.inicio,
            oferta_origem.fim,
        )
        nova_oferta.status = (
            oferta_origem.status
            if isinstance(oferta_origem.status, StatusOferta)
            else StatusOferta(str(oferta_origem.status))
        )

        self._metodos.inserir(self._oferta_para_documento(nova_oferta, estabelecimento))
        self._ofertas.append(nova_oferta)
        return nova_oferta

    def sincronizar_ofertas_de_reservas(self, reservas):
        for reserva in reservas:
            self.registrar_oferta_se_nao_existir(reserva.oferta)

    def vincular_estabelecimento_nas_ofertas(self, estabelecimento):
        alvo = self._normalizar_nome(estabelecimento.nome_fantasia)
        for of in self._ofertas:
            if self._normalizar_nome(of.nome_estabelecimento) == alvo:
                nome_antigo = of.nome_estabelecimento
                of.nome_estabelecimento = estabelecimento.nome_fantasia
                self._metodos.atualizar_varios(
                    {"id": of.id, "nome_estabelecimento": nome_antigo},
                    {
                        "estabelecimento_id": estabelecimento.cnpj,
                        "nome_estabelecimento": estabelecimento.nome_fantasia,
                    },
                )

    def registrar_resgate_oferta(self, oferta_reserva, estabelecimento=None):
        oferta = self.registrar_oferta_se_nao_existir(oferta_reserva, estabelecimento)
        if oferta.quantidade > 0:
            oferta.decrementar_quantidade()
        if estabelecimento is None:
            estabelecimento = self._controlador_sistema.controlador_estabelecimento.buscar_por_nome_fantasia(
                oferta.nome_estabelecimento
            )
        self._metodos.atualizar_varios(
            {"id": oferta.id, "nome_estabelecimento": oferta.nome_estabelecimento},
            self._oferta_para_documento(oferta, estabelecimento),
        )
        return oferta

    def criarOferta (self):
        dados = self._telaOferta.pegaDadosOferta()
        if dados is None:
            return
        user = self._controlador_sistema.estabelecimento_logado

        oferta = OfertaRelampago(dados["id"],
                                 dados["titulo"],
                                 dados["descricao"],
                                 user.nome_fantasia,
                                 dados["original"],
                                 dados["desconto"],
                                 dados["quantidade"],
                                 dados["inicio"],
                                 dados["fim"])
        tempo_valido = oferta.validarJanelaRetirada()

        if tempo_valido:
            if self.buscar_oferta(dados["id"], user.nome_fantasia):
                self._telaOferta.mensagem("Erro: já existe uma oferta com esse ID.")
                return
            self._metodos.inserir(self._oferta_para_documento(oferta, user))
            self._ofertas.append(oferta)
            self._telaOferta.mensagem('Oferta criada com sucesso!')
        else:
            self._telaOferta.mensagem('Erro: Minimo de 2h 30min de janela de retirada')

    def listarOferta (self):
        self.recarregar_ofertas()
        self._controlador_sistema.controlador_reservas.recarregar_reservas()

        user = self._controlador_sistema.estabelecimento_logado
        alvo = self._normalizar_nome(user.nome_fantasia)

        ofertas = [of for of in self._ofertas if self._normalizar_nome(of.nome_estabelecimento) == alvo]
        reservas_por_oferta = {
            of.id: self._controlador_sistema.controlador_reservas.pega_reservas_da_oferta(
                of.id, of.nome_estabelecimento, estabelecimento_id=user.cnpj
            )
            for of in ofertas
        }

        possuiOfertas = self._telaOferta.exibirOfertas(ofertas, reservas_por_oferta)
        return possuiOfertas, ofertas

    def excluirOferta (self):

        possuiOfertas, ofertas = self.listarOferta()

        if not possuiOfertas:
            self._telaOferta.mensagem('O estabelecimento não possui ofertas relâmpago')
            return
        idSelecionado = self._telaOferta.pegaIdOferta()

        ofertaAExcluir = None

        for of in ofertas:
            if str(of.id).strip() == str(idSelecionado).strip():
                ofertaAExcluir = of
                break

        if not ofertaAExcluir:
            self._telaOferta.mensagem('Erro: Oferta não encontrada')
            return

        user = self._controlador_sistema.estabelecimento_logado
        motivo_bloqueio = self._motivo_bloqueio_modificacao(ofertaAExcluir, user, acao="excluir")
        if motivo_bloqueio:
            self._telaOferta.mensagem(motivo_bloqueio)
            return

        confirmaçãoExclusão = self._telaOferta.confimarExclusão(ofertaAExcluir)

        if confirmaçãoExclusão == 'S':
            self._metodos.deletar_por_filtro({
                "id": ofertaAExcluir.id,
                "nome_estabelecimento": ofertaAExcluir.nome_estabelecimento,
            })
            self._ofertas.remove(ofertaAExcluir)
            self._telaOferta.mensagem(F'\nOferta {idSelecionado} excluida com sucesso!')
            return
        else:
            self._telaOferta.mensagem('\nOperação cancelada')
            return

    def atualizarOferta (self):
        possuiOfertas, ofertas = self.listarOferta()

        if not possuiOfertas:
            self._telaOferta.mensagem('\nNão existe ofertas cadastradas')
            return

        idOferta = self._telaOferta.pegaIdOferta()
        oferta = None

        for of in ofertas:
            if str(of.id).strip() == str(idOferta).strip():
                oferta = of
                break

        if oferta is None:
            self._telaOferta.mensagem('\nOferta não encontrada')
            return

        user = self._controlador_sistema.estabelecimento_logado
        motivo_bloqueio = self._motivo_bloqueio_modificacao(oferta, user, acao="atualizar")
        if motivo_bloqueio:
            self._telaOferta.mensagem(motivo_bloqueio)
            return

        ofertaAtualizada = self._telaOferta.exibirCamposOferta(oferta)
        if ofertaAtualizada is None:
            return

        inicio_org = oferta.inicio
        fim_org = oferta.fim

        oferta.inicio = ofertaAtualizada["inicio"]
        oferta.fim = ofertaAtualizada["fim"]

        tempoValido = oferta.validarJanelaRetirada()
        if tempoValido:
            oferta.titulo = ofertaAtualizada["titulo"]
            oferta.descricao = ofertaAtualizada["descricao"]
            oferta.original = ofertaAtualizada["original"]
            oferta.desconto = ofertaAtualizada["desconto"]
            oferta.quantidade = ofertaAtualizada["quantidade"]
            user = self._controlador_sistema.estabelecimento_logado
            self._metodos.atualizar_varios(
                {"id": oferta.id, "nome_estabelecimento": oferta.nome_estabelecimento},
                self._oferta_para_documento(oferta, user),
            )
            self._telaOferta.mensagem('Oferta atualizada com sucesso!')
            return
        else:
            oferta.inicio = inicio_org
            oferta.fim = fim_org
            self._telaOferta.mensagem('Erro: Tempo mínimo de retirada de 02:30')
            return

# Feito por Gabriel