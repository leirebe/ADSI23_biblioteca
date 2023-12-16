class Resenna:
    def __init__(self, idRes, idUsuario, idLibro, comment):
        self.idRes = idRes
        self.idUsuario = idUsuario
        self.idLibro = idLibro
        self.comment = None


    def __str__(self):
        return f"{self.comment}"
