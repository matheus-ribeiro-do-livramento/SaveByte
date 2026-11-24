from datetime import datetime, timedelta
from database.metodos import BaseMetodos
from model.enums import StatusReserva


class ControladorPenalidade:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self._bd = BaseMetodos("penalidades")

    def verificar_reservas_expiradas(self, id_consumidor):
        ctrl_res = self._controlador_sistema.controlador_reservas
        ctrl_res.recarregar_reservas()
        reservas = ctrl_res.pega_reservas_do_consumidor(id_consumidor)
        agora = datetime.now()

        for r in reservas:
            if r.status == StatusReserva.PENDENTE and agora > r.data_hora_limite_retirada:
                r.status = StatusReserva.EXPIRADA
                ctrl_res.atualizar_status_reserva(r.id, r.status.value, id_consumidor)
                self.aplicar_penalidade(id_consumidor, r.id)

    def aplicar_penalidade(self, id_consumidor, id_reserva, motivo: str = "Não retirada no prazo"):
        # Evita aplicar penalidade duplicada para a mesma reserva
        ja_penalizada = self._bd.buscar_um({
            "consumidor_id": id_consumidor,
            "reserva_id": id_reserva,
        })
        if ja_penalizada:
            return

        agora = datetime.now()
        penalidade = {
            "consumidor_id": id_consumidor,
            "reserva_id": id_reserva,
            "data_aplicacao": agora,
            "motivo": motivo,
        }
        self._bd.inserir(penalidade)

        data_limite = agora - timedelta(days=7)
        penalidades_recentes = self._bd.listar({
            "consumidor_id": id_consumidor,
            "data_aplicacao": {"$gte": data_limite},
        })

        ctrl_cons = self._controlador_sistema.controlador_consumidor
        ctrl_cons.atualizar_penalidades_contador(id_consumidor, len(penalidades_recentes))

        if len(penalidades_recentes) >= 2:
            bloqueado_ate = agora + timedelta(days=7)
            ctrl_cons.bloquear_consumidor(id_consumidor, bloqueado_ate)

    def verificar_bloqueio_ativo(self, id_consumidor) -> bool:
        self.verificar_reservas_expiradas(id_consumidor)

        ctrl_cons = self._controlador_sistema.controlador_consumidor
        consumidor = ctrl_cons.buscar_por_id(id_consumidor)
        if not consumidor:
            return False

        bloqueado_ate = consumidor.bloqueadoAte
        if bloqueado_ate:
            if datetime.now() >= bloqueado_ate:
                ctrl_cons.desbloquear_consumidor(id_consumidor)
                return False
            return True

        return False

    def listar_penalidades_consumidor(self, id_consumidor) -> list[dict]:
        return self._bd.listar({"consumidor_id": id_consumidor})