import random


class BookCopy:
    def __init__(self, idCopia, book):
        self.idCopia = idCopia
        self.book = book
        self.available = True

    def generate_copies(cls, book):
        # Fijar la semilla para reproducir la misma secuencia cada vez
        random.seed(42)

        # entre 1 y 5 copias por libro
        total_copies = random.randint(1, 5)

        # Generar instancias de BookCopy relacionadas con el libro
        copies = [cls(book, f"{book.idLibro}_copy_{i}") for i in range(1, total_copies + 1)]

        return copies

    def reserve(self):
        if self.available:
            self.available = False

    def __str__(self):
        return f"{self.idCopia} ({self.book})"
