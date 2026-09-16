class PainelImpacto:
    def __init__(
        self,
        quantidade_cestas_resgatadas: int = 0,
        total_comida_salva_kg: float = 0.0,
        total_dinheiro_economizado: float = 0.0,
    ):
        self._quantidade_cestas_resgatadas = quantidade_cestas_resgatadas
        self._total_comida_salva_kg = total_comida_salva_kg
        self._total_dinheiro_economizado = total_dinheiro_economizado

    @property
    def quantidade_cestas_resgatadas(self):
        return self._quantidade_cestas_resgatadas

    @quantidade_cestas_resgatadas.setter
    def quantidade_cestas_resgatadas(self, quantidade_cestas_resgatadas):
        self._quantidade_cestas_resgatadas = quantidade_cestas_resgatadas

    @property
    def total_comida_salva_kg(self):
        return self._total_comida_salva_kg

    @total_comida_salva_kg.setter
    def total_comida_salva_kg(self, total_comida_salva_kg):
        self._total_comida_salva_kg = total_comida_salva_kg

    @property
    def total_dinheiro_economizado(self):
        return self._total_dinheiro_economizado

    @total_dinheiro_economizado.setter
    def total_dinheiro_economizado(self, total_dinheiro_economizado):
        self._total_dinheiro_economizado = total_dinheiro_economizado


# Feito por Augusto
