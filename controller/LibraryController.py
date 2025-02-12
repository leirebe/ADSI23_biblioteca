import datetime
from datetime import datetime

from model import Connection, Book, User, Reserva, BookCopy
from model.tools import hash_password
from model.Forum import Tema, Mensaje

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

    def create_user(self, username, email, password):
        # Verificar si el usuario ya existe con el mismo correo electrónico
        existing_user = db.select("SELECT * FROM User WHERE Email = ?", (email,))
        if existing_user:
            return None

        user_id = db.insert("INSERT INTO User(Nombre, Email, Password, Rol) VALUES (?, ?, ?, 0)",
                            (username, email, hash_password(password)))
        if user_id:
            return User(user_id, username, 0, email)
        else:
            return None

    def create_reservation(self, user_id, copy_id, reserve_time):
        db.insert(
            "INSERT INTO Reserva(usuarioIdU, IdCopiaLibro, FechaHoraInicio, FechaEntrega) VALUES (?, ?, ?, NULL)",
            (user_id, copy_id, reserve_time)
        )
        reserva = db.select("SELECT * FROM RESERVA WHERE UsuarioIdU= ? AND IdCopiaLibro=? AND FechaHoraInicio=? AND FechaEntrega is NULL", (user_id, copy_id, reserve_time))[0]

        return Reserva(reserva[0], reserva[1], reserva[2], reserva[3], reserva[4])

    def get_reserva(self, libroId, userId):
        reserve = db.select("SELECT * FROM Reserva WHERE IdCopiaLibro = ? AND usuarioIdU = ?",
                            (libroId, userId)
                            )
        if reserve:
            reservation = Reserva(reserve[0][0], reserve[0][1], reserve[0][2],reserve[0][3], reserve[0][4])
            return reservation
        else:
            return None

    def insert_review(self, user_id, book_id, comentario, nueva_puntuacion):
        existing_review = db.select("SELECT * FROM Resenna WHERE UsuarioIdU = ? AND LibroIdLibro = ?",
                                    (user_id, book_id))

        if existing_review:  # Actualizar la existente
            db.update("UPDATE Resenna SET Comentario = ?, puntuacion = ? WHERE UsuarioIdU = ? AND LibroIdLibro = ?",
                      (comentario, nueva_puntuacion, user_id, book_id))
        else:  # Insertar una nueva
            db.insert("INSERT INTO Resenna (UsuarioIdU, LibroIdLibro, Comentario, puntuacion) VALUES (?, ?, ?, ?)",
                      (user_id, book_id, comentario, nueva_puntuacion))

    def get_book_id_from_reservation(self, copy_id):
        if copy_id:
            book_id = db.select("SELECT LibroidLibro FROM CopiaLibro WHERE IdCopia = ?", (copy_id,))
            if book_id:
                return book_id[0][0]
        return None

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

    def get_all_users(self):
        users_data = db.select("SELECT * FROM User")
        users = [
            User(user[0], user[1], user[2], user[3])
            for user in users_data
        ]
        return users

    def delete_user(self, user_id):
        result = db.delete("DELETE FROM User WHERE id = ?", (user_id,))
        return result > 0

    def create_book(self, title, author_id, description):
        book_id = db.insert("INSERT INTO Book(title, author, description, cover) VALUES (?, ?, ?, '')",
                            (title, author_id, description))

        if book_id:
            return Book(book_id, title, author_id, '', description)
        else:
            print('error')
            return None
    
    def get_forum_topics(self):
        tema_foros = db.select("SELECT * FROM Tema")
        return tema_foros
    
    def get_topic_id(self, tema_id):
        tema= db.select("SELECT * FROM Tema WHERE IdTema = ?", (tema_id,))
        if tema:
            return tema[0]
        else:
            return None
    
    def create_tema(self, autor, nombre, descripcion):
        tema_id = db.insert("INSERT INTO Tema(TemaNombre, TemaDescr, TemaAutor) VALUES (?, ?, ?)",
                            (nombre, descripcion, autor))

        if tema_id:
            tema = Tema(tema_id, autor, nombre, descripcion)
            return tema
        else:
            print('Hubo un error al crear el tema.')
            return None

    def create_mensaje(self, idTopic, userId, receptor, texto):
        fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mensaje_id = db.insert("INSERT INTO Mensaje(UsuarioIdU, TemaIdTema, receptor, Mensaje, FechaHora) VALUES (?, ?, ?, ?, ?)",
                            (userId, idTopic, receptor, texto, fechaHora))
        
        if mensaje_id:
            mensaje = Mensaje(mensaje_id, userId, idTopic, receptor, texto, fechaHora)
            return mensaje
        else:
            print('Hubo un error al crear el mensaje.')
            return None
        
    def get_comments_for_topic(self, topic_id):
        comments = db.select("SELECT * FROM Mensaje WHERE TemaIdTema = ?", (topic_id,))
        return comments
