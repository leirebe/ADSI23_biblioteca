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
	else:
		user = library.get_user_id(userId)

	return render_template('perfil.html',user=user)


@app.route('/reserve')
def reserve_book():
	user_id = request.user.id if 'user' in dir(request) and request.user else None
	bookId = request.values.get("id", "")
	copyId = request.values.get("copyId", "")
	reservation_time = get_current_time()
	res = library.reserve_copy(user_id, bookId, copyId, reservation_time)
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


def get_current_time():
	current_time = datetime.now()
	return current_time.strftime("%Y-%m-%d %H:%M")
