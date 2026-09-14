class Localizacao:
    def __init__(self, endereco: str, latitude: float, longitude: float):
        self._endereco = endereco
        self._latitude = latitude
        self._longitude = longitude

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, endereco):
        self._endereco = endereco

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude

#Feito por Matheus