import hashlib
import random
import sqlite3
import json
import os
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), '..', 'datos.db')
if os.path.exists(db_path):
    os.remove(db_path)

salt = "library"

con = sqlite3.connect(db_path)
cur = con.cursor()

###Create tables
cur.execute("""
	CREATE TABLE Author(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE Book(
		id integer primary key AUTOINCREMENT,
		title varchar(50),
		author integer,
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		Nombre varchar(255),
		Rol integer(10),
		Email varchar(30),
		Password varchar(32)
	)
""")

cur.execute("""
	CREATE TABLE Tema(
		IdTema integer primary key AUTOINCREMENT,
  		TemaNombre integer(10),
        TemaDescr varchar(255),
        TemaAutor integer(10)
   
	)
""")

cur.execute("""
	CREATE TABLE Origen(
		TemaIdTema integer(10),
		MensajeIdM integer(10),
		MensajeUsuarioIdU integer(10),
		MensajeTemaIdTema integer(10),
		FOREIGN KEY(TemaIdTema) REFERENCES Mensaje(TemaIdTema),
		FOREIGN KEY(MensajeIdM) REFERENCES Mensaje(IdM)
	)
""")

cur.execute("""
	CREATE TABLE Mensaje(
		IdM integer primary key AUTOINCREMENT,
		UsuarioIdU integer(20),
		TemaIdTema integer(20),
		Receptor integer(20),
		Mensaje varchar(255),
		FechaHora date,
		FOREIGN KEY(UsuarioIdU) REFERENCES User(IdU),
		FOREIGN KEY(TemaIdTema) REFERENCES Tema(IdTema)
	)
""")

cur.execute("""
	CREATE TABLE Solicitud(
		UsuarioIdU integer(10),
		UsuarioIdU2 integer(10),
		Aceptada boolean,
		FOREIGN KEY(UsuarioIdU) REFERENCES User(IdU),
		FOREIGN KEY(UsuarioIdU2) REFERENCES User(IdU)
	)
""")

cur.execute("""
	CREATE TABLE Recomendacion(
		UsuarioIdU integer(10),
		LibroIdLibro integer(10),
		FOREIGN KEY(UsuarioIdU) REFERENCES User(IdU),
		FOREIGN KEY(LibroIdLibro) REFERENCES Book(id)
	)
""")

cur.execute("""
	CREATE TABLE Reserva(
		IdReserva integer primary key AUTOINCREMENT,
		UsuarioIdU integer(10),
		IdCopiaLibro integer(10),
		FechaHoraInicio date, 
		FechaEntrega date,
		FOREIGN KEY(UsuarioIdU) REFERENCES Usuario(IdU),
		FOREIGN KEY(IdCopiaLibro) REFERENCES CopiaLibro(IdCopia)
	)
""")

cur.execute("""
	CREATE TABLE Resenna(
		IdResenna integer primary key AUTOINCREMENT,
		UsuarioIdU integer(10),
		LibroIdLibro integer(10),
		Comentario varchar(255),
		puntuacion integer(10),
		FOREIGN KEY(UsuarioIdU) REFERENCES User(IdU),
		FOREIGN KEY(LibroIdLibro) REFERENCES Book(id)
	)
""")

cur.execute("""
	CREATE TABLE CopiaLibro( 
		IdCopia integer primary key AUTOINCREMENT,
		LibroidLibro integer,
		FOREIGN KEY(LibroIdLibro) REFERENCES Book(id)
	)
""")

cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES User(IdU)
	)
""")

con.commit()

### Insert users
users_path = os.path.join(os.path.dirname(__file__), '..', 'usuarios.json')

with open(users_path, 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', {user['rol']}, '{user['email']}', '{dataBase_password}')""")
	con.commit()


#### Insert books
books_path = os.path.join(os.path.dirname(__file__), '..', 'libros.tsv')
with open(books_path, 'r', encoding='utf-8') as f:
	libros = [x.split("\t") for x in f.readlines()]

book_count = 0
for author, title, cover, description in libros:
	res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	if res.rowcount == -1:
		cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
		con.commit()
		res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	author_id = res.fetchone()[0]

	cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author_id, cover, description.strip()))

	libro_id= cur.lastrowid #id del último libro
	random.seed(42)
	random_range = int(hashlib.sha256(str(libro_id).encode()).hexdigest(), 16) % 5 + 1
	total_copies = random.randint(1, random_range)
	for _ in range(1, total_copies + 1):
		cur.execute("INSERT INTO CopiaLibro (LibroIdLibro) VALUES (?)", (libro_id,))

	con.commit()
	if book_count >= 100:
		break
	book_count += 1


# Reseñas
cur.execute("INSERT INTO Resenna VALUES (NULL, ?, ?, ?, ?)",
		            (1, 2, "Muy bueno.", 4))
cur.execute("INSERT INTO Resenna VALUES (NULL, ?, ?, ?, ?)",
		            (2, 2, "Excelente.", 5))
cur.execute("INSERT INTO Resenna VALUES (NULL, ?, ?, ?, ?)",
		            (3, 1, "No me ha gustado.", 1))
cur.execute("INSERT INTO Resenna VALUES (NULL, ?, ?, ?, ?)",
		            (2, 1, "Recomendable.", 4))
cur.execute("INSERT INTO Resenna VALUES (NULL, ?, ?, ?, ?)",
		            (1, 1, "Guay.", 3))
con.commit()

# Reservas
cur.execute("INSERT INTO Reserva VALUES (NULL, ?, ?, ?, ?)",
		            (1, 2, datetime.now(), None))
cur.execute("INSERT INTO Reserva VALUES (NULL, ?, ?, ?, ?)",
		            (1, 3, datetime.now(), None))
con.commit()

# Historial de Lectura
cur.execute("INSERT INTO Reserva VALUES (NULL, ?, ?, ?, ?)",
		            (1, 1, datetime.now(), "2023-12-31 21:09:07.939378"))
cur.execute("INSERT INTO Reserva VALUES (NULL, ?, ?, ?, ?)",
		            (1, 6, datetime.now(), "2023-12-31 21:09:07.939378"))
con.commit()

# Insertar Foros predeterminados
temas_path = os.path.join(os.path.dirname(__file__), '..', 'temas.json')	
print(temas_path)

with open(temas_path, 'r', encoding='utf-8') as f:
    temas_data = json.load(f)['temas']


for tema in temas_data:
    autor = tema['autor']
    nombre = tema['nombre']
    descripcion = tema['descripcion']
    
    cur.execute("INSERT INTO Tema DEFAULT VALUES")
    tema_id = cur.lastrowid  # Obtener el ID del tema recién insertado
    
    cur.execute("UPDATE Tema SET TemaNombre = ?, TemaDescr = ?, TemaAutor = ? WHERE IdTema = ?", (nombre, descripcion, autor, tema_id))
    #cur.execute("INSERT INTO Mensaje (UsuarioIdU, TemaIdTema, Mensaje, FechaHora) VALUES (?, ?, ?, ?)",(autor, tema_id, texto, datetime.now()))
	
con.commit()
