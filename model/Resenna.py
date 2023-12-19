from .Connection import Connection
from .User import User

db = Connection()

class Resenna:
    def __init__(self, idUsuario, libro, comment,puntuacion):
        self.Usuario = idUsuario
        self.Libro = libro
        self.comment = comment
        self.puntuacion = puntuacion

    @property
    def Usuario(self):
        if type(self._Usuario) == int:
            em = db.select("SELECT * from User WHERE id=?", (self._Usuario,))[0]
            self._Usuario = User(em[0], em[1], em[2], em[3])
        return self._Usuario

    @Usuario.setter
    def Usuario(self, value):
        self._Usuario = value

    def __str__(self):
        return f"{self.Usuario}, {self.Libro}, {self.comment}, {self.puntuacion}"
