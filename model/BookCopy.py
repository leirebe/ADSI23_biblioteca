class BookCopy:
    def __init__(self, book, idCopia):
        self.idCopia = idCopia
        self.book = book
        #self.available =

    #@classmethod
    # def generate_copies(cls, book):

    #    random.seed(42)

    #    random_range = int(hashlib.sha256(str(book.idLibro).encode()).hexdigest(), 16) % 5 + 1

    # entre 1 y 5 copias por libro
    #    total_copies = random.randint(1, random_range)

    #    # Generar instancias de BookCopy relacionadas con el libro
    #    copies = [cls(book, f"{book.idLibro}_copy_{i}") for i in range(1, total_copies + 1)]

    #    return copies

    def __str__(self):
        return f"{self.idCopia} ({self.book})"
