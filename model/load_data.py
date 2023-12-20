import hashlib
import sqlite3
import json
import os

os.remove("datos.db")

salt = "library"


con = sqlite3.connect("datos.db")
cur = con.cursor()


### Create tables
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
		author varchar(40),
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		nombre varchar(20),
		rol integer(1),
		email varchar(30),
		password varchar(32)
	)
""")

cur.execute("""
	CREATE TABLE Tema(
		idTema integer primary key AUTOINCREMENT
	)
""")

cur.execute("""
	CREATE TABLE Origen(
		temaIdTema integer(20),
		mensajeIdM integer(10),
		FOREIGN KEY(temaIdTema) REFERENCES Mensaje(temaIdTema),
		FOREIGN KEY(mensajeIdM) REFERENCES Mensaje(idM)
	)
""")

cur.execute("""
	CREATE TABLE Mensaje(
		idM integer primary key AUTOINCREMENT,
		usuarioIdU integer(20),
		temaIdTema integer(20),
		receptor integer(20),
		texto varchar(255),
		FechaHora date,
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(TemaIdTema) REFERENCES Tema(idTema)
	)
""")

cur.execute("""
	CREATE TABLE Solicitud(
		usuarioIdU integer(10),
		usuarioIdU2 integer(10),
		aceptada boolean,
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(usuarioIdU2) REFERENCES Usuario(idU)
	)
""")

cur.execute("""
	CREATE TABLE Recomendacion(
		usuarioIdU integer(10),
		libroIdLibro integer(10),
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(libroIdLibro) REFERENCES LIbro(idLibro)
	)
""")

cur.execute("""
	CREATE TABLE Reserva(
		usuarioIdU integer(10),
		copiaLibroIdCopia integer(10),
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(copiaLibroIdCopia) REFERENCES CopiaLibro(idCopia)
	)
""")

cur.execute("""
	CREATE TABLE Resenna(
		usuarioIdU integer(10),
		libroIdLibro integer(10),
		texto varchar(255),
		puntuacion integer,
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(libroIdLibro) REFERENCES Libro(idLibro)
	)
""")

cur.execute("""
	CREATE TABLE CopiaLibro( 
		idCopia integer primary key AUTOINCREMENT,
		LibroidLibro integer,
		FechaHoraInicio date, 
		FechaEntrega date
	)
""")

cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES User(id)
	)
""")

### Insert users

with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', {user['rol']}, '{user['email']}', '{dataBase_password}')""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r', encoding='utf-8') as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description in libros[:100]:
	res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	if res.rowcount == -1:
		cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
		con.commit()
		res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	author_id = res.fetchone()[0]

	cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author_id, cover, description.strip()))

	con.commit()

# Reseñas
cur.execute("INSERT INTO Resenna VALUES (?, ?, ?, ?)",
		            (1, 2, "Muy bueno.", 4))
cur.execute("INSERT INTO Resenna VALUES (?, ?, ?, ?)",
		            (2, 2, "Excelente.", 5))
cur.execute("INSERT INTO Resenna VALUES (?, ?, ?, ?)",
		            (3, 1, "No me ha gustado.", 1))
cur.execute("INSERT INTO Resenna VALUES (?, ?, ?, ?)",
		            (2, 1, "Recomendable.", 4))
con.commit()

