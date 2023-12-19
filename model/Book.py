from .BookCopy import BookCopy
from .Connection import Connection
from .Author import Author

db = Connection()


class Book:
    def __init__(self, idLibro, title, author, cover, description):
        self.idLibro = idLibro
        self.title = title
        self.author = author
        self.cover = cover
        self.description = description
        self.disponible = True
        self.puntuacion = 0.0
        self.listaResennas = []
        self.copies = BookCopy.generate_copies(book=self)

    @property
    def author(self):
        if type(self._author) == int:
            em = db.select("SELECT * from Author WHERE id=?", (self._author,))[0]
            self._author = Author(em[0], em[1])
        return self._author

    def agregarResennas(Resenna, self):  # NO sabemos si es necesaria esta función
        self.listaResennas.append(Resenna)

    @author.setter
    def author(self, value):
        self._author = value

    def availableCopies(self):
        print("Total de copias:", len(self.copies))
        copiasDisp = [copy.idCopia for copy in self.copies if copy.available]
        print("Copias disponibles:", copiasDisp)
        return len(copiasDisp), copiasDisp

    def __str__(self):
        return f"{self.title} ({self.author})"
