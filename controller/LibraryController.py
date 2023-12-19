from model import Connection, Book, User, Reserva
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
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count
	def getBook(self,id_):
		res = db.select("""
				SELECT b.* 
				FROM Book b
				WHERE b.id = ?
			""", (id_,))
		if len(res) == 1:
			b = res[0]
			return Book(b[0],b[1],b[2],b[3],b[4])
		else:
			return None

	def reserve_copy(self, user_id, book_id, copy_id, reserve_time):
		book = self.getBook(book_id) #es necesario??
		copy = book.get_copy(copy_id)
		if copy and copy.available:
			copy.available = False
			unique_id= Reserva.generate_unique_id()
			reserva = Reserva(idReserva = unique_id, idUsuario=user_id, idCopiaLIbro=copy_id, devuelto=False,puntuacion=0, resenna="")
			self.db.insert("INSERT INTO Reserva(idReserva, usuarioidU, copiaLibroidCopia, fechaReserva) VALUES (?, ?, ?, ?)",
						   (unique_id, user_id, copy_id, reserve_time ))
			return True
		else:
			return False
	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3])
		else:
			return None

	def get_user_id(self,id):
		user = db.select("SELECT * from User WHERE id = ? ", (id,))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3])
		else:
			return None

