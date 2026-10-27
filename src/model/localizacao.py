class Localizacao:
    def __init__(self, cidade: str, bairro: str, endereco: str):
        self._endereco = endereco
        self._cidade = cidade
        self._bairro = bairro

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, endereco):
        self._endereco = endereco

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, cidade):
        self._cidade = cidade

    @property
    def bairro(self):
        return self._bairro

    @bairro.setter
    def bairro(self, bairro):
        self._bairro = bairro 

#Feito por Matheus