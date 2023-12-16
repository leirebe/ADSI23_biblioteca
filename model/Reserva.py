class Reserva:
    def __init__(self, idReserva, idUsuario, idCopiaLibro, devuelto, puntuacion, resenna):
        self.idReserva = idReserva
        self.idUsuario = idUsuario
        self.idCopiaLibro = idCopiaLibro
        self.devuelto = False
        self.puntuacion = 0
        self.resenna = ""

    def __str__(self):
        return f"{self.idReserva}"
