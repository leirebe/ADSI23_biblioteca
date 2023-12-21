import datetime

from controller.GestorUsuario import db


class Reserva:
    def __init__(self, idReserva, idUsuario, idLibro, fechaHoraInicio, fechaEntrega, devuelto, puntuacion, resenna):
        self.idReserva = idReserva #es necesario
        self.idUsuario = idUsuario
        self.idLibro = idLibro
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaEntrega = fechaEntrega
        self.devuelto = False
        self.puntuacion = 0
        self.resenna = ""

    @staticmethod
    def generate_unique_id():
        # contador para generar id's únicos de la clase Reserva
        if not hasattr(Reserva, '_id_counter'):
            Reserva._id_counter = 1
        else:
            Reserva._id_counter += 1
        return Reserva._id_counter
    def __str__(self):
        return f"{self.idReserva}"

    def devolver_libro(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.update("UPDATE Reserva SET FechaEntrega = ? WHERE IdReserva = ? AND UsuarioIdU = ?",
                  (now, self.idReserva,self.idUsuario))
