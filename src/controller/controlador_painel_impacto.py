from view.tela_painel_impacto import TelaPainelImpacto
from model.painel_impacto import PainelImpacto
from database.metodos import BaseMetodos


class ControladorPainelImpacto:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPainelImpacto()
        self._db_reservas = BaseMetodos("reservas")
        self._db_ofertas = BaseMetodos("ofertas_relampago")

    def abrir_tela(self, consumidor=None):
        if consumidor is None:
            consumidor = self.__controlador_sistema.consumidor_logado
        if consumidor is None:
            return None

        consumidor_id = self.obter_id_consumidor(consumidor)
        dados = self.calcular_impacto(consumidor_id)
        evento = self.__tela.mostrar_painel(dados)

        mapa_abas = {
            "-NAV_EXPLORAR-": "explorar",
            "-NAV_RESERVAS-": "reservas",
            "-NAV_IMPACTO-": "impacto",
            "-NAV_PERFIL-": "perfil",
        }
        return mapa_abas.get(evento)

    def calcular_impacto(self, consumidor_id) -> dict:
        todas_reservas = self.listar_colecao(self._db_reservas)

        reservas_retiradas = []
        for r in todas_reservas:
            status = str(r.get("status", "")).strip().lower()

            id_cons_reserva = r.get("consumidor_id")
            if id_cons_reserva is None:
                cons_campo = r.get("consumidor")
                id_cons_reserva = (
                    cons_campo.get("id")
                    if isinstance(cons_campo, dict)
                    else cons_campo
                )

            if status == "retirada" and str(id_cons_reserva) == str(consumidor_id):
                reservas_retiradas.append(r)

        todas_ofertas = self.listar_colecao(self._db_ofertas)
        mapa_ofertas = {}
        for o in todas_ofertas:
            of_id = o.get("id")
            if of_id is not None:
                mapa_ofertas[str(of_id)] = o

        economia_total = 0.0
        historico = []

        for reserva in reservas_retiradas:
            oferta_campo = reserva.get("oferta")
            if isinstance(oferta_campo, dict):
                oferta = oferta_campo
            else:
                oferta_id = oferta_campo or reserva.get("oferta_id")
                oferta = mapa_ofertas.get(str(oferta_id))

            if oferta:
                preco_orig = float(oferta.get("original") or 0.0)
                preco_desc = float(oferta.get("desconto") or 0.0)
                economia = max(0.0, preco_orig - preco_desc)
                economia_total += economia

                historico.append({
                    "titulo": oferta.get("titulo", "Oferta Relâmpago"),
                    "estabelecimento": oferta.get("nome_estabelecimento", "Estabelecimento"),
                    "preco_pago": preco_desc,
                    "economia": round(economia, 2),
                })

        total_resgates = len(reservas_retiradas)
        painel = PainelImpacto(
            quantidade_cestas_resgatadas=total_resgates,
            total_comida_salva_kg=round(total_resgates * 0.5, 2),
            total_dinheiro_economizado=round(economia_total, 2),
        )

        nivel, meta, msg_progresso = self.calcular_gamificacao(painel.quantidade_cestas_resgatadas)

        return {
            "total_resgates": painel.quantidade_cestas_resgatadas,
            "comida_salva_kg": painel.total_comida_salva_kg,
            "economia_total": painel.total_dinheiro_economizado,
            "nivel": nivel,
            "meta_proximo_nivel": meta,
            "mensagem_progresso": msg_progresso,
            "historico": historico,
        }

    def calcular_gamificacao(self, total: int):
        if total == 0:
            return "Bronze Save", 1, "Resgate sua 1ª oferta para subir para Prata Save!"
        elif total < 5:
            faltam = 5 - total
            return "Prata Save", 5, f"Faltam {faltam} resgate(s) para Ouro Save."
        elif total < 15:
            faltam = 15 - total
            return "Ouro Save", 15, f"Faltam {faltam} resgate(s) para Diamante Save."
        else:
            return "Diamante Save", total, "Nível máximo atingido! Obrigado por combater o desperdício."

    def obter_id_consumidor(self, consumidor):
        if isinstance(consumidor, dict):
            return consumidor.get("id") or consumidor.get("_id")
        return getattr(consumidor, "id", None)

    def listar_colecao(self, db_instancia) -> list:
        for nome_metodo in ("listar", "listar_todos", "buscar_todos", "get_all"):
            if hasattr(db_instancia, nome_metodo):
                return getattr(db_instancia, nome_metodo)() or []
        if hasattr(db_instancia, "_collection"):
            return list(db_instancia._collection.find())
        return []