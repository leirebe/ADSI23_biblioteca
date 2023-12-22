import datetime

from model import Connection, Book, User, Reserva, BookCopy
from model.tools import hash_password

db = Connection()


class LibraryController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LibraryController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def search_books(self, title="", author="", limit=6, page=0):
        count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
        res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit * page))
        books = [
            Book(b[0], b[1], b[2], b[3], b[4])
            for b in res
        ]
        return books, count

    def getBook(self, id_):
        res = db.select("""
				SELECT b.* 
				FROM Book b
				WHERE b.id = ?
			""", (id_,))
        if len(res) == 1:
            b = res[0]
            return Book(b[0], b[1], b[2], b[3], b[4])
        else:
            return None

    def get_available_copies(self, book_id):
        # Obtener la lista de copias disponibles para el libro dado
        available_copies = db.select(
            "SELECT idCopia FROM CopiaLibro WHERE LibroidLibro = ?",
            (book_id,)
        )
        # Verificar si cada copia está disponible (no reservada)
        return [copia_id[0] for copia_id in available_copies if self.is_copy_available(copia_id[0])]

    def is_copy_available(self, copy_id):
        # Verificar si una copia específica está disponible (no reservada)
        reservation = db.select(
            "SELECT FechaEntrega FROM Reserva WHERE IdCopiaLibro = ? AND FechaEntrega IS NULl",
            (copy_id,)
        )

        return len(reservation) == 0

    def reserve_copy(self, user_id, book_id, reserve_time):
        available_copies = self.get_available_copies(book_id)
        if available_copies:
            reservation = self.create_reservation(user_id, available_copies[0], reserve_time)
            return f"Reserva realizada con éxito. Número de reserva: {reservation.idReserva}"
        else:
            return "No hay copias disponibles para reservar."

    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE Email = ? AND Password = ?", (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][3])
        else:
            return None

    def get_user_cookies(self, token, time):
        user = db.select(
            "SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?",
            (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][3])
        else:
            return None

    def get_user_id(self, id):
        user = db.select("SELECT * from User WHERE id = ? ", (id,))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2], user[0][3])
        else:
            return None

    def create_user(self, nombre, email, password):
        # Verificar si el usuario ya existe con el mismo correo electrónico
        existing_user = db.select("SELECT * FROM User WHERE email = ?", (email,))
        if existing_user:
            return None  # El usuario ya existe

        # Crear un nuevo usuario con nombre, correo electrónico y contraseña
        user_id = db.insert("INSERT INTO User(nombre, email, password) VALUES (?, ?, ?)",
                            (nombre, email, hash_password(password)))
        if user_id:
            return User(user_id, nombre, email, hash_password(password))  # Devolver el nuevo usuario
        else:
            return None  # Error al crear el usuario

    def create_reservation(self, user_id, copy_id, reserve_time):
        db.insert(
            "INSERT INTO Reserva(usuarioIdU, copiaLibroIdCopia, FechaHoraInicio, FechaEntrega) VALUES (?, ?, ?, NULL)",
            (user_id, copy_id, reserve_time)
        )
        reserva = db.select("SELECT * FROM RESERVA WHERE UsuarioIdU= ? AND IdCopiaLibro=? AND FechaHoraInicio=? AND FechaEntrega is NULL", (user_id, copy_id, reserve_time))[0]

        return Reserva(reserva[0], reserva[1], reserva[2], reserva[3], reserva[4])

    def get_reserva(self, libroId, userId):
        reserve = db.select("SELECT * FROM Reserva WHERE idLibro = ? AND usuarioIdU = ? AND FechaEntrega IS NULL", (libroId, userId))
        if reserve:
            return Reserva(reserve[0][0], reserve[0][1], reserve[0][2], reserve[0][3], reserve[0][4])
        else:
            return None

    def insert_review(self, user_id, book_id, comentario, puntuacion):
        existing_review = db.select("SELECT * FROM Resenna WHERE UsuarioIdU = ? AND LibroIdLibro = ?",
                                    (user_id, book_id))
        if existing_review: #Actualizar la existente
            db.update("UPDATE Resenna SET Comentario = ?, puntuacion = ? WHERE UsuarioIdU = ? AND LibroIdLibro = ?",
                      (comentario, puntuacion, user_id, book_id))
        else: #Insertar una nueva
            db.insert("INSERT INTO Resenna (UsuarioIdU, LibroIdLibro, Comentario, puntuacion) VALUES (?, ?, ?, ?)",
                      (user_id, book_id, comentario, puntuacion))

    def generarListaRecomendaciones(self, user):
        # precondicion: usuario con historial de reservas
        # 1) acceder a su historial de reservas (id de libros)
        listaReservas = user.get_libros_reservados()
        listaIds = tuple([libro.idLibro for libro in listaReservas])
        # 2) acceder a catalogo: obtener 20 libros que no se encuentren en el historial
        placeholders = ', '.join(['?' for _ in listaIds])
        listaLibros = db.select(f"SELECT * FROM Book WHERE id NOT IN ({placeholders}) LIMIT 20", (listaIds))
        listaRecomendaciones = [Book(b[0], b[1], b[2], b[3], b[4]) for b in listaLibros]
        # devolver: lista de recomendaciones (libros no leidos)
        return listaRecomendaciones
        # renderizar libros en: GET /
