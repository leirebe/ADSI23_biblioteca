from . import BaseTestClass
from bs4 import BeautifulSoup


class TestAdmin(BaseTestClass):

    def test_administrar_usuario(self):
        res = self.login('admin@gmail.com', 'admin')

        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)
        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        self.assertIn('Administrar Usuarios', page.find_all('div', class_='row')[0].get_text())

    def test_anadir_libro(self):
        res = self.login('admin@gmail.com', 'admin')

        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        self.assertIn('Añadir Libro', page.find_all('div', class_='row')[0].get_text())

    def test_noadmin_administar_usuario(self):
        res = self.login('james@gmail.com', '123456')
        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        self.assertNotIn('Administrar Usuarios', page.find_all('div', class_='row')[0].get_text())

    def test_noadmin_anadir_libro(self):
        res = self.login('james@gmail.com', '123456')

        self.assertEqual(302, res.status_code)
        self.assertEqual('/', res.location)

        res2 = self.client.get('/')
        page = BeautifulSoup(res2.data, features="html.parser")
        self.assertNotIn('Añadir Libro', page.find_all('div', class_='row')[0].get_text())

    def test_crear_usuario(self):
        res_login = self.login('admin@gmail.com', 'admin')
        self.assertEqual(302, res_login.status_code)
        self.assertEqual('/', res_login.location)

        users_before = len(self.db.select("SELECT * FROM User"))

        data = {
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo_usuario@gmail.com',
            'rol': 1,
            'contrasena': 'password123',
        }
        res_post = self.client.post('/crear_usuario', data=data, follow_redirects=True)
        self.assertEqual(200, res_post.status_code)

        users_after = len(self.db.select("SELECT * FROM User"))
        self.assertEqual(users_before + 1, users_after)

    def test_noadmin_crear_usuario(self):
        res_login = self.login('james@gmail.com', '123456')
        self.assertEqual(302, res_login.status_code)
        self.assertEqual('/', res_login.location)

        users_before = len(self.db.select("SELECT * FROM User"))

        data = {
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo_usuario1@gmail.com',
            'rol': 1,
            'contrasena': 'password123',
        }
        res_post = self.client.post('/crear_usuario', data=data, follow_redirects=True)
        self.assertEqual(200, res_post.status_code)

        users_after = len(self.db.select("SELECT * FROM User"))
        self.assertEqual(users_before, users_after)

    def test_eliminar_usuario(self):
        res_login = self.login('admin@gmail.com', 'admin')
        self.assertEqual(302, res_login.status_code)
        self.assertEqual('/', res_login.location)

        users_before = len(self.db.select("SELECT * FROM User"))

        user_id = self.db.select("SELECT id FROM User WHERE email = 'nuevo_usuario@gmail.com'")[0][0]

        res_delete = self.client.post(f'/eliminar_usuario/{user_id}', follow_redirects=True)
        self.assertEqual(200, res_delete.status_code)

        users_after_delete = len(self.db.select("SELECT * FROM User"))
        self.assertEqual(users_before - 1, users_after_delete)

    def test_noadmin_eliminar_usuario(self):
        res_login = self.login('james@gmail.com', '123456')
        self.assertEqual(302, res_login.status_code)
        self.assertEqual('/', res_login.location)

        users_before = len(self.db.select("SELECT * FROM User"))

        user_id = self.db.select("SELECT id FROM User WHERE email = 'james@gmail.com'")[0][0]

        res_delete = self.client.post(f'/eliminar_usuario/{user_id}', follow_redirects=True)
        self.assertEqual(200, res_delete.status_code)

        users_after_delete = len(self.db.select("SELECT * FROM User"))
        self.assertEqual(users_before, users_after_delete)



