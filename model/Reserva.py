import datetime

from controller.GestorUsuario import db


class Reserva:
    def __init__(self, idReserva, idUsuario, idLibro, fechaHoraInicio, fechaEntrega):
        self.idReserva = idReserva #es necesario
        self.idUsuario = idUsuario
        self.idLibro = idLibro
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaEntrega = fechaEntrega

    def __str__(self):
        return f"{self.idReserva}"

    def devolver_libro(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.update("UPDATE Reserva SET FechaEntrega = ? WHERE IdReserva = ? AND UsuarioIdU = ?",
                  (now, self.idReserva,self.idUsuario))
