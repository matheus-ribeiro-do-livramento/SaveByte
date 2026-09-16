from datetime import datetime

from usuario import Usuario


class Consumidor(usuario):
    def __init__(self, bloqueaAte: datetime, 
                 preferenciasAlimentares: list, 
                 penalidade: int):
        super().__init__(dataCadastro, email, id, localizacao, nome, senha)
        self._bloquadoAte: datetime
        self.preferenciasAlimentares: list

    @property
    def bloqueadoAte(self):
        return self._bloquadoAte

    @bloqueadoAte.setter
    def bloqueadoAte(self, bloqueadoAte: datetime):
        self._bloquadoAte = datetime

# Feito por Gabriel
