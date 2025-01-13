import copy

class ChavePrototipo:
    def __init__(self, id = "", nome = '', qr_code = '', posse = 0):
        self._idChave = id
        self._nomeSala = nome
        self._qrCode = qr_code
        self._posse = posse

    def clonar(self, n):
        copia = copy.copy(self)
        return copia

