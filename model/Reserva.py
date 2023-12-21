class Reserva:
    def __init__(self, idReserva, idUsuario, idLibro, fechaHoraInicio, fechaEntrega):
        self.idReserva = idReserva #es necesario
        self.idUsuario = idUsuario
        self.idLibro = idLibro
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaEntrega = fechaEntrega

    def __str__(self):
        return f"{self.idReserva}"
