import sqlite3

from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect
from datetime import datetime
from controller.Sistema import Sistema

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	sistema = Sistema()
	sistema.generarListaRecomendaciones(1)
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)

@app.route('/resenna')
def resenna():

	return render_template('resenna.html')

#¿LIBRO EN PARTICULAR?
""""@app.route('/resenna/<int:libro_id>', methods=['GET'])
def formulario_resena(libro_id):
    # Aquí podrías pasar el ID del libro a la plantilla del formulario de reseña
    return render_template('resenna.html', libro_id=libro_id)"""

@app.route('/book')
def book():
	bookId = request.values.get("id", "")
	print(f"bookId recibido: {bookId}")
	book = library.getBook(bookId)
	if book:
		resennas = book.getResennas()
		return render_template('book.html', book=book, resennas=resennas)
	else:
		print("Libro no encontrado")
		return render_template('book_not_found.html')


@app.route('/perfil')
def perfil():
	userId = request.values.get("id", -1)
	if userId==-1:
		user = request.user
		reservados = user.get_libros_reservados()
	else:
		user = library.get_user_id(userId)
		reservados = None
	historial = user.get_libros_leidos()

	return render_template('perfil.html', user=user, libros_en_reserva=reservados, historial_lectura=historial)

@app.route('/devolverUnLibro')
def devolver_libro():
	if not ('user' in dir(request) and request.user and request.user.token):
		return redirect('/')
	libroId = request.values.get("libroId", "")
	reserva=library.get_reserva(libroId,request.user.id)
	if(reserva is not None):
		reserva.devolver_libro()
		return redirect("/perfil")
	else:
		return redirect('/')



@app.route('/reserve')
def reserve_book():
	user_id = request.user.id if 'user' in dir(request) and request.user else None
	bookId = request.values.get("id", "")
	reservation_time = get_current_time()
	res = library.reserve_copy(user_id, bookId, reservation_time)
	return render_template('reserva.html', result=res)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token: #esta linea indica que el user ha iniciado sesion
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'user' in dir(request) and request.user and request.user.token:
        return redirect('/')

    if request.method == 'POST':
        nombre = request.form.get("nombre", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validar si las contraseñas coinciden
        if password != confirm_password:
            return render_template('registro.html', error="Las contraseñas no coinciden")

        # Crear un nuevo usuario
        user = library.create_user(nombre, email, password)

        if user:
            # Iniciar sesión automáticamente después del registro
            session = user.new_session()
            resp = redirect("/")
            resp.set_cookie('token', session.hash)
            resp.set_cookie('time', str(session.time))
            return resp
        else:
            return render_template('registro.html', error="Error en el registro. Intenta nuevamente.")
    else:
        return render_template('registro.html')


def get_current_time():
	current_time = datetime.now()
	return current_time.strftime("%Y-%m-%d %H:%M")
