import hashlib
import sqlite3
import json

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
	CREATE TABLE Libro(
		idLibro integer primary key AUTOINCREMENT,
		titulo varchar(50),
		autor varchar(40),
		genero varchar(50),
		disponible boolean,
		fechaHora date,
		FOREIGN KEY(autor) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE User(
		idU integer primary key AUTOINCREMENT,
		nombre varchar(20),
		rol integer(1)
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
		usuarioIdU integer(20)
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
		usuarioIdU2 integer(10)
		aceptada boolean,
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(usuarioIdU2) REFERENCES Usuario(idU)
	)
""")

cur.execute("""
	CREATE TABLE Recomendacion(
		usuarioIdU integer(10),
		libroIdLibro integer(10)
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(libroIdLibro) REFERENCES LIbro(idLibro)
	)
""")

cur.execute("""
	CREATE TABLE Reserva(
		usuarioIdU integer(10),
		copiaLibroIdCopia integer(10),
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(libroIdLibro) REFERENCES CopiaLibro(idCopia)
	)
""")

cur.execute("""
	CREATE TABLE Resenna(
		usuarioIdU integer(10),
		libroIdLibro integer(10),
		texto varchar(255),
		FOREIGN KEY(usuarioIdU) REFERENCES Usuario(idU),
		FOREIGN KEY(libroIdLibro) REFERENCES Libro(idLibro)
	)
""")

cur.execute("""
	CREATE TABLE CopiaLibro( 
		idCopia integer primary key AUTOINCREMENT,
		LibroidLibro integer,
		FechaHora date
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
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r') as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description in libros:
	res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	if res.rowcount == -1:
		cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
		con.commit()
		res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	author_id = res.fetchone()[0]

	cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author_id, cover, description.strip()))

	con.commit()



