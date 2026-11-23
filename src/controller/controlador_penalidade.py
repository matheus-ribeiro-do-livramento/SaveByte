from src.database.metodos import BaseMetodos
from src.model import enums
from datetime import datetime, timedelta

class ControladorPenalidade():
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self._bd = BaseMetodos("penalidades")


    def verificar_reservas_expiradas(self, id_consumidor):
        reservas = self._controlador_sistema.controlador_reservas.pega_reservas_do_consumidor(id_consumidor)
        agora = datetime.now()

        for r in reservas:
            if r.status == enums.StatusReserva("PENDENTE") and agora > r.data_hora_limite_retirada:
                r.status = enums.StatusReserva("EXPIRADA")
                self._controlador_sistema.controlador_reservas.atualizar_statsu_reserva(r.id, r.status.value)
                self.aplicar_penalidade(id_consumidor, r.id)

    def aplicar_penalidade(self, id_consumidor, id_reserva, motivo: str = "Não retirada no prazo"):
        agora = datetime.now()

        penalidade = {
            "consumidor_id": id_consumidor,
            "reserva_id": id_reserva,
            "data_aplicação": agora,
            "motivo": motivo           
        }
        self._bd.inserir(penalidade)

        data_limite = agora - timedelta(days = 7)
        penalidade_recente = self._bd.listar({
            "comsumidor_id": id_consumidor, 
            "data_aplicação": {"$gte": data_limite}})
        
        if len(penalidade_recente) >= 2:
            bloqueado_ate = agora + timedelta(days=7)
            self._controlador_sistema.controlador_consumidor.bloquear_consumidor(id_consumidor, bloqueado_ate)

    def verificar_bloqueio_ativo(self, id_consumidor: str):
        self.verificar_reservas_expiradas(id_consumidor)

        consumidor = self._controlador_sistema.controlador_consumidor.buscar_por_id(id_consumidor)
        if not consumidor:
            return False

        bloqueado_ate = getattr(consumidor, "bloqueado_ate", None)
        esta_bloqueado = consumidor.status == enums.StatusConta("BLOQUEADO")

        if esta_bloqueado:
            if bloqueado_ate and datetime.now() >= bloqueado_ate:
                self._controlador_sistema.controlador_consumidor.desbloquear_consumidor(id_consumidor)
                return False
            return True

        return False

    def listar_penalidades_consumidor(self, id_consumidor: str) -> list[dict]:
        return self._bd.listar({"consumidor_id": id_consumidor})