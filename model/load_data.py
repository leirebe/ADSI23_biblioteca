import hashlib
import sqlite3
import json
import os
import datetime

os.remove("datos.db")

salt = "library"


con = sqlite3.connect("datos.db")
cur = con.cursor()


### Create tables
#cur.execute("""
#	CREATE TABLE Author(
#		id integer primary key AUTOINCREMENT,
#		name varchar(40)
#	)
#""")

cur.execute("""
	CREATE TABLE Libro(
		idLibro integer primary key AUTOINCREMENT,
		Titulo varchar(50),
		Autor varchar(40),
		Cover varchar(50),
		Descripcion TEXT,
		FechaHora date,
		Disponible boolean,
	)
""")

cur.execute("""
	CREATE TABLE Usuario(
		IdU integer primary key AUTOINCREMENT,
		Nombre varchar(255),
		Rol integer(10),
		Email varchar(30),
		Password varchar(32)
	)
""")

cur.execute("""
	CREATE TABLE Tema(
		IdTema integer primary key AUTOINCREMENT
	)
""")

cur.execute("""
	CREATE TABLE Origen(
		TemaIdTema integer(10),
		MensajeIdM integer(10),
		MensajeUsuarioIdU integer(10),
		MensajeTemaIdTema integer(10),
		FOREIGN KEY(TemaIdTema) REFERENCES Mensaje(TemaIdTema),
		FOREIGN KEY(TensajeIdM) REFERENCES Mensaje(IdM)
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
		FOREIGN KEY(UsuarioIdU) REFERENCES Usuario(IdU),
		FOREIGN KEY(TemaIdTema) REFERENCES Tema(IdTema)
	)
""")

cur.execute("""
	CREATE TABLE Solicitud(
		UsuarioIdU integer(10),
		UsuarioIdU2 integer(10),
		Aceptada boolean,
		FOREIGN KEY(UsuarioIdU) REFERENCES Usuario(IdU),
		FOREIGN KEY(UsuarioIdU2) REFERENCES Usuario(IdU)
	)
""")

cur.execute("""
	CREATE TABLE Recomendacion(
		UsuarioIdU integer(10),
		LibroIdLibro integer(10),
		FOREIGN KEY(UsuarioIdU) REFERENCES Usuario(IdU),
		FOREIGN KEY(LibroIdLibro) REFERENCES LIbro(IdLibro)
	)
""")

cur.execute("""
	CREATE TABLE Reserva(
		IdReserva integer primary key AUTOINCREMENT,
		UsuarioIdU integer(10),
		CopiaLibroIdCopia integer(10),
		Resenna varchar(255),
		Devuelto boolean,
		Puntuacion integer(10),
		FOREIGN KEY(UsuarioIdU) REFERENCES Usuario(IdU),
		FOREIGN KEY(CopiaLibroIdCopia) REFERENCES CopiaLibro(IdCopia)
	)
""")

cur.execute("""
	CREATE TABLE Resenna(
		IdResenna integer primary key AUTOINCREMENT,
		UsuarioIdU integer(10),
		LibroIdLibro integer(10),
		Comentario varchar(255),
		puntuacion integer(10),
		FOREIGN KEY(UsuarioIdU) REFERENCES Usuario(IdU),
		FOREIGN KEY(IibroIdLibro) REFERENCES Libro(IdLibro)
	)
""")

cur.execute("""
	CREATE TABLE CopiaLibro( 
		IdCopia integer primary key AUTOINCREMENT,
		LibroidLibro integer,
		FechaHora date
	)
""")

cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES Usuario(IdU)
	)
""")

### Insert users

with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO Usuario VALUES (NULL, '{user['nombres']}', {user['rol']}, '{user['email']}', '{dataBase_password}')""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r', encoding='utf-8') as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description in libros[:100]:
	now = datetime.now()
	cur.execute("INSERT INTO Libro VALUES (?, ?, ?, ?, ?, true)",
		            (title, author, cover, description.strip(), now))

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
