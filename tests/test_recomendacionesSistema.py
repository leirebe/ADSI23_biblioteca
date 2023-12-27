from . import BaseTestClass
from bs4 import BeautifulSoup


class TestRecomendacionesSistema(BaseTestClass):

    def test_recomendar_con_reserva(self):
        # Login
        res = self.login('james@gmail.com', '123456')
        # Obtener info.......
        id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]
        reservas = [title[0] for title in self.db.select("""
				SELECT Book.title
				FROM Reserva
				JOIN CopiaLibro ON Reserva.IdCopiaLibro = CopiaLibro.IdCopia
				JOIN Book ON CopiaLibro.LibroIdLibro = Book.id
				WHERE Reserva.UsuarioIdU = ? AND Reserva.FechaEntrega IS NULL
			""", (id,))]
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        recomendaciones = page.find_all('h5', class_='card-title')
        self.assertEqual(20, len(recomendaciones))
        for recomendacion in recomendaciones:
            title = recomendacion.get_text()
            self.assertNotIn(title, reservas)
        # Logout
        self.client.get('/logout')
    
    def test_recomendar_sin_reserva(self):
        #print(self.app.logout)

        data = {
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo_usuario3@gmail.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        # Se crea el usuario
        res_post = self.client.post('/registro', data=data, follow_redirects=True)
        #self.assertEqual(200, res_post.status_code)
        
        # Se hace login del nuevo usuario
        self.login('nuevo_usuario3@gmail.com', 'password123')
        
        id = self.db.select("SELECT id from User where Email = ?", ('nuevo_usuario3@gmail.com',))[0][0]
        reservas = [title[0] for title in self.db.select("""
				SELECT Book.title
				FROM Reserva
				JOIN CopiaLibro ON Reserva.IdCopiaLibro = CopiaLibro.IdCopia
				JOIN Book ON CopiaLibro.LibroIdLibro = Book.id
				WHERE Reserva.UsuarioIdU = ? AND Reserva.FechaEntrega IS NULL
			""", (id,))]
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        recomendaciones = page.find_all('h5', class_='card-title')
        self.assertEqual(20, len(recomendaciones))
        for recomendacion in recomendaciones:
            title = recomendacion.get_text()
            self.assertNotIn(title, reservas)
        # Logout
        self.client.get('/logout')



