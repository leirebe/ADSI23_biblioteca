import sqlite3

from . import BookCopy, Connection, Author, Resenna
import datetime

db = Connection()

class Book:
    def __init__(self, idLibro, title, author, cover, description):
        self.idLibro = idLibro
        self.title = title
        self.author = author
        self.cover = cover
        self.description = description
        self.puntuacion = 0.0
        self.copies = self.getCopies()

    @property
    def author(self):
        if type(self._author) == int:
            em = db.select("SELECT * from Author WHERE id=?", (self._author,))[0]
            self._author = Author(em[0], em[1])
        return self._author

    def insertarResennaUsuario(self, idUsuario, comentario, puntuacion):
        resennas_usuario = self.getResennasUsuario(idUsuario)
        if resennas_usuario:
            self.deleteResennaUsuario(idUsuario) #Si el usuario tiene una reseña la eliminamos
            self.insertarResenna(idUsuario, comentario, puntuacion)

    def getResennasUsuario(self, idUsuario):
        em = db.select("SELECT * FROM Resenna WHERE LibroIdLibro=? AND UsuarioIdU=?", (self.idLibro, idUsuario))
        return [Resenna(r[0], r[1], r[2], r[3]) for r in em]

    def deleteResennaUsuario(self, idUsuario):
        db.execute("DELETE FROM Resenna WHERE LibroIdLibro=? AND UsuarioIdU=?", (self.idLibro, idUsuario))

    def insertarResenna(self, idUsuario, comentario, puntuacion):
        nueva_resenna = Resenna(idUsuario, self.idLibro, comentario, puntuacion)
        db.execute("INSERT INTO Resenna (UsuarioIdU, LibroIdLibro, Comentario, Puntuacion) VALUES (?, ?, ?, ?)",
                   (nueva_resenna.Usuario, nueva_resenna.Libro, nueva_resenna.comment, nueva_resenna.puntuacion))

    @author.setter
    def author(self, value):
        self._author = value

    def getCopies(self):
        em=db.select("SELECT * FROM Reserva WHERE IdCopiaLibro=?",(self.idLibro,))
        copies = [BookCopy(copy[0], self) for copy in em]
        total_copies = len(copies)
        return [copies, total_copies]



    def getResennas(self):
        em=db.select("SELECT * FROM Resenna WHERE libroIdLibro=?",(self.idLibro,))
        return [Resenna(r[0],self,r[2],r[3]) for r in em]

    def insertarResenna(self, idUsuario, comentario, puntuacion):
        nueva_resenna = Resenna(idUsuario, self.idLibro, comentario, puntuacion)
        db.execute("INSERT INTO Resenna (UsuarioIdU, LibroIdLibro, Comentario, Puntuacion) VALUES (?, ?, ?, ?)",
                   (nueva_resenna.Usuario, nueva_resenna.Libro, nueva_resenna.comment, nueva_resenna.puntuacion))

    def __str__(self):
        return f"{self.title} ({self.author})"

    def insertar_resena(usuario_id, libro_id, comentario, puntuacion):
        db.insert("INSERT INTO Resenna (UsuarioIdU, LibroIdLibro, Comentario, puntuacion, FechaHora) VALUES (?, ?, ?, ?, ?)",
            (usuario_id, libro_id, comentario, puntuacion))
