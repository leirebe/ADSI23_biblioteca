import unittest

from . import BaseTestClass
from bs4 import BeautifulSoup
class test_devolverLibro(BaseTestClass):

    #Comprobar que un libro SI se encuentra en la lista de Libros en Reserva
    def test_libroSiEnReservas(self):
        # Hacer login como usuario
        self.login('james@gmail.com', '123456')

        # Obtener ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID de un libro de las reservas del usuario
        libro_esperado_id = 3

        # Verificar la presencia del libro en la lista de reservas del usuario
        libro_en_reservas = self.db.select("""
                   SELECT 1
                   FROM Reserva
                   JOIN CopiaLibro ON Reserva.IdCopiaLibro = CopiaLibro.IdCopia
                   WHERE Reserva.UsuarioIdU = ? AND Reserva.IdCopiaLibro = ? AND Reserva.FechaEntrega IS NULL
               """, (user_id, libro_esperado_id))

        self.assertTrue(libro_en_reservas, f"El libro con ID {libro_esperado_id} está en las reservas del usuario")

        # Realizar logout
        self.client.get('/logout')



    # Comprobar que un libro NO se encuentra en la lista de Libros en Reserva
    def test_libroNoEnReservas(self):

        # Hacer login como usuario
        self.login('james@gmail.com', '123456')

        # Obtener ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID de un libro que se espera encontrar en las reservas del usuario
        libro_esperado_id = 1

        # Verificar la presencia del libro en la lista de reservas del usuario
        libro_en_reservas = self.db.select("""
                   SELECT 1
                   FROM Reserva
                   JOIN CopiaLibro ON Reserva.IdCopiaLibro = CopiaLibro.IdCopia
                   WHERE Reserva.UsuarioIdU = ? AND Reserva.IdCopiaLibro = ? AND Reserva.FechaEntrega IS NULL
               """, (user_id, libro_esperado_id))

        self.assertFalse(libro_en_reservas, f"El libro con ID {libro_esperado_id} no está en las reservas del usuario")

        # Realizar logout
        self.client.get('/logout')



    # Devolver un libro que SI se encuentra en la lista de Reservas
    def test_devolver_libro_en_reservas(self):

        # Hacer login del usuario
        self.login('james@gmail.com', '123456')

        # Verificar si el libro con ID 2 está en la lista de reservas del usuario
        libro_esperado_id = 3
        libro_en_reservas = self.user_has_book_in_reservations(libro_esperado_id)
        self.assertTrue(libro_en_reservas, f"El libro con ID {libro_esperado_id} está en las reservas del usuario")

        # Realizar la acción de devolver el libro
        res = self.client.get('/devolverUnLibro?id=2', follow_redirects=True)
        self.assertEqual(200, res.status_code)

        # Logout después de la prueba
        self.client.get('/logout')

    def user_has_book_in_reservations(self, book_id):

        # Obtener el ID del usuario para la consulta
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Realizar la consulta para verificar si el libro está en las reservas del usuario
        reservations = self.db.select("""
            SELECT * FROM Reserva
            WHERE UsuarioIdU = ? AND IdCopiaLibro = ? AND FechaEntrega IS NULL
            """, (user_id, book_id))

        # Si la consulta devuelve alguna reserva, el libro está en la lista de reservas
        return len(reservations) > 0


if __name__ == '__main__':
    unittest.main()
