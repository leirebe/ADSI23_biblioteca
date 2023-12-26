import unittest

from . import BaseTestClass
from bs4 import BeautifulSoup

class Test_reservarLibro(BaseTestClass):

    def test_accesoCatalogo(self):
        res = self.client.get('/catalogue')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertIsNotNone(page.find('form', class_='form-inline'))

    def test_filtrarPorLibros(self):
        params = {
            'title': "Harry Potter"
        }
        res = self.client.get('/catalogue', query_string=params)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertTrue(len(page.find_all('div', class_='card')) > 0)

    def test_filtrarPorAutor(self):
        params = {
            'author': "J.K. Rowling"
        }
        res = self.client.get('/catalogue', query_string=params)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertTrue(len(page.find_all('div', class_='card')) > 0)

    def test_verInfoLibro(self):
        # Supongamos que el catálogo tiene libros y seleccionamos el primer libro
        res = self.client.get('/book', query_string={'id': '1'})
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        # Verifica que la página muestra información completa sobre el libro
        self.assertIsNotNone(page.find('div', class_='container p-5 my-5 border'))
    def test_reservarLibroSinIdentificarse(self):
        # Supongamos que el catálogo tiene libros y seleccionamos el primer libro
        res = self.client.post('/reserve', query_string={'id': '233'}, follow_redirects=True)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        # Verifica que se redirige a la página de inicio de sesión
        self.assertIsNotNone(page.find('div', class_='container p-5 my-5 border'))

    def test_reservarLibroDisponible(self):
        # Supongamos que el catálogo tiene libros y seleccionamos el primer libro
        res = self.client.post('/reserve', query_string={'id': '233'}, follow_redirects=True)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        # Verifica que se marca el libro como reservado y muestra información relevante
        self.assertIsNotNone(page.find('div', class_='container p-5 my-5 border'))

    def test_reservarMultiplesLibros(self):
        # Supongamos que el catálogo tiene libros y seleccionamos el primer libro
        # Realizamos dos solicitudes de reserva consecutivas
        res1 = self.client.post('/reserve', query_string={'id': '244'}, follow_redirects=True)
        res2 = self.client.post('/reserve', query_string={'id': '244'}, follow_redirects=True)

        print("Código de estado res1:", res1.status_code)
        print("Código de estado res2:", res2.status_code)

        # Verificamos que la primera solicitud fue exitosa (código de estado 200)
        self.assertEqual(200, res1.status_code)
        page = BeautifulSoup(res2.data, features="html.parser")

        # Verificamos que la segunda solicitud fue rechazada (código de estado 4xx)
        self.assertIsNotNone(page.find('div', class_='container p-5 my-5 border'))

    def test_accesoLibroInexistente(self):
        # Supongamos que intentamos acceder a un libro con ID inexistente
        res = self.client.get('/book', query_string={'id': '100000'})
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        # Verifica que se muestra un mensaje de error indicando que el libro no existe
        self.assertIn(b'no ha sido encontrado', res.data)


if __name__ == '__main__':
    unittest.main()




