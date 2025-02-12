from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect, jsonify
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()
userAutenticado = False

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

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user' in dir(request) and request.user and request.user.rol == 1:
            return func(*args, **kwargs)
        else:
            return redirect('/')
    return wrapper


@app.route('/')
def index():
	user = getattr(request, 'user', None)
	if 'user' in dir(request) and request.user and request.user.token:
		listaRecomendaciones = library.generarListaRecomendaciones(request.user)
	else:
		listaRecomendaciones = None
	return render_template('index.html', books=listaRecomendaciones, user=user)


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
		num_available_copies = len(library.get_available_copies(bookId))
		return render_template('book.html', book=book, resennas=resennas, num_available_copies=num_available_copies)
	else:
		print("Libro no encontrado")
		msj= f"El libro con el ID {bookId} no ha sido encontrado"
		return render_template('error.html', book=book, msj=msj)


@app.route('/perfil')
def perfil():
	userId = request.values.get("id", -1)
	if userId == -1:
		user = request.user
		reservados = user.get_libros_reservados()
	else:
		user = library.get_user_id(userId)
		reservados = None
	historial = user.get_libros_leidos()
	return render_template('perfil.html', user=user, libros_en_reserva=reservados, historial_lectura=historial)


@app.route('/devolverUnLibro', methods=['GET', 'POST'])
def devolver_libro():
	user_id = request.user.id if 'user' in dir(request) and request.user else None
	bookId = request.values.get("id", "")
	reserva = library.get_reserva(bookId,user_id)
	if reserva is not None:
		reserva.devolver_libro()
		return redirect("/perfil")
	else:
		return redirect('/')

@app.route('/resennar', methods=['POST'])
def resennar():
	if 'user' in dir(request) and request.user:
		user_id = request.user.id if 'user' in dir(request) and request.user else None
		book_id = request.values.get("id", "")
		comentario = request.form.get("comentario")
		puntuacion = request.form.get("puntuacion")

		libro_id = library.get_book_id_from_reservation(book_id)

		if user_id and libro_id:  # Verificar que haya un usuario y un ID de libro válido
			library.insert_review(user_id, libro_id, comentario, puntuacion)
			return redirect('/perfil')
		else:
			return redirect('/login')
	else:
		return redirect('/login')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve_book(ultima_reserva_tiempo=None):
	if userAutenticado:
		if ultima_reserva_tiempo and (get_current_time() - ultima_reserva_tiempo).seconds < 300:
			msj = b'Ya has realizado una reserva recientemente. Por favor, espera un momento antes de intentarlo de nuevo.'
			return render_template('error.html', msj=msj)

		user_id = request.user.id if 'user' in dir(request) and request.user else None
		bookId = request.values.get("id", "")
		print(f"bookId recibido para reservar: {bookId}")
		print(f"persona que realiza la reserva: {user_id}")
		reservation_time = get_current_time()

		ultima_reserva_tiempo = get_current_time()

		reserva = library.reserve_copy(user_id, bookId, reservation_time)
		return render_template('reserva.html', user=user_id, bookId=bookId, book=book, time=reservation_time, reserva=reserva)
	else:
		return redirect('login')


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
		global userAutenticado
		userAutenticado = True
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect("/")
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

        if password != confirm_password:
            return render_template('registro.html', error="Las contraseñas no coinciden")

        user = library.create_user(nombre, email, password)

        if user:
            session = user.new_session()
            resp = redirect("/")
            resp.set_cookie('token', session.hash)
            resp.set_cookie('time', str(session.time))
            return resp
        else:
            return render_template('registro.html', error="Error en el registro. Intenta nuevamente.")
    else:
        return render_template('registro.html')

@app.route('/administrar_usuarios')
@admin_required
def administrar_usuarios():
    users = library.get_all_users()
    return render_template('administrar_usuarios.html', users=users)

@app.route('/crear_usuario', methods=['POST'], endpoint='crear_usuario_admin')
@admin_required
def crear_usuario():
    nombre = request.form.get("nombre", "")
    email = request.form.get("email", "")
    contrasena = request.form.get("contrasena", "")

    library.create_user(nombre, email, contrasena)

    return redirect('/administrar_usuarios')

@app.route('/eliminar_usuario/<int:user_id>', methods=['POST'], endpoint='eliminar_usuario_admin')
@admin_required
def eliminar_usuario(user_id):
    library.delete_user(user_id)

    return 'Usuario eliminado con éxito'

@app.route('/anadir_libro', methods=['GET'], endpoint='anadir_libro_admin1')
@admin_required
def mostrar_formulario_anadir_libro():
    return render_template('anadir_libro.html')

@app.route('/anadir_libro', methods=['POST'], endpoint='crear_usuario_admin2')
@admin_required
def anadir_libro():
    title = request.form.get('titulo')
    id_author = request.form.get('id_author')
    description = request.form.get('descripcion')

    library.create_book(title, id_author, description)

    return redirect('/')
def get_current_time():
	current_time = datetime.now()
	return current_time.strftime("%Y-%m-%d %H:%M")

@app.route('/forum')
def foros():
    temas_foro = library.get_forum_topics()
    print(temas_foro)
    return render_template('forum.html', temas_foro=temas_foro)

@app.route('/crear-tema',  methods=['GET', 'POST'])
def crear_tema():
    userId = request.values.get("id", -1)
    user_info = str(request.user)
    nombre = user_info.split(' (')[0]
    
    if request.method == 'POST':
        
        nombre_tema = request.form['nombreTema']
        descripcion_tema = request.form['descripcionTema']
        userId = request.user.id
        
        tema = library.create_tema(userId, nombre_tema, descripcion_tema)
		
        return redirect('/forum')
    
    return render_template('crear_tema.html', user=nombre)

@app.route('/ver-tema-<int:topic_id>', methods=['GET', 'POST'])
def ver_tema(topic_id):
    if request.method == 'POST':
        userId = request.user.id
        is_response = request.form.get('isResponse')
        
        if is_response == 'True':
            parent_comment_id = request.form.get('parentCommentId')
            response_text = request.form.get('responseText')
            
            if response_text:
                library.create_mensaje(topic_id, userId, parent_comment_id, response_text)
        else:
            comment_text = request.form.get('commentText')
            
            if comment_text:
                library.create_mensaje(topic_id, userId, None, comment_text)
        
    comments = library.get_comments_for_topic(topic_id) 
    tema_data = library.get_topic_id(topic_id)
    user = library.get_user_id(tema_data[3])
    autor_nombre = str(user).split(' (')[0]
    
    main_comments=[]
    responses = []
    
    for comment in comments:
        if comment[3] == None:  
            
            main_comments.append(comment)
        else:
            
            responses.append(comment)

    return render_template('ver-tema.html', topic=tema_data, autor=autor_nombre, comments=comments, main_comments=main_comments, responses=responses)






