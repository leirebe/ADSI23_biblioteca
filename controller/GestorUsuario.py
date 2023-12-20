from model import Connection

db = Connection()

class GestorUsuario:

    def __init__(self) -> None:
        pass

    def obtenerHistorialReservas(self, userid: int):
        return db.select(f"SELECT cl.IdCopia FROM Reserva AS r JOIN CopiaLibro AS cl ON r.IdCopiaLibro = cl.IdCopia WHERE r.UsuarioIdU = {userid}")