from .Connection import Connection
from .User import User

db = Connection()

class Resenna:
    def __init__(self, IdResenna, idUsuario, libro, comment,puntuacion):
        self.ResennaId = IdResenna
        self.Usuario = idUsuario
        self.Libro = libro
        self.comment = comment
        self.puntuacion = puntuacion

    @property
    def Usuario(self):
        if type(self._Usuario) == int:
            em = db.select("SELECT Nombre from User WHERE id=?", (self._Usuario,))
            if em:
                return em[0][0]
            else:
                return None

    @Usuario.setter
    def Usuario(self, value):
        self._Usuario = value

    def __str__(self):
        return f"{self.ResennaId}{self.Usuario}, {self.Libro}, {self.comment}, {self.puntuacion}"



