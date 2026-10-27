from datetime import datetime

from model.usuario import Usuario


class Consumidor(Usuario):
    def __init__(self, bloqueadoAte: datetime, 
                 preferenciasAlimentares: list, 
                 penalidade: int, dataCadastro, email, id, localizacao, nome, senha):
        super().__init__(id, nome, email, senha,
                         localizacao.cidade, localizacao.bairro, localizacao.endereco,
                         dataCadastro)
        self._bloquadoAte = bloqueadoAte
        self._preferenciasAlimentares = preferenciasAlimentares
        self._penalidade = penalidade

    @property
    def bloqueadoAte(self):
        return self._bloquadoAte

    @bloqueadoAte.setter
    def bloqueadoAte(self, bloqueadoAte: datetime):
        self._bloquadoAte = bloqueadoAte

    @property
    def preferenciasAlimentares(self):
        return self._preferenciasAlimentares

    @preferenciasAlimentares.setter
    def preferenciasAlimentares(self, preferenciaAlimentares: list):
        self._preferenciasAlimentares = preferenciaAlimentares

    @property
    def penalidade(self):
        return self._penalidade

    @penalidade.setter
    def penalidade(self, penalidade):
        self._penalidade = penalidade

# Feito por Gabriel