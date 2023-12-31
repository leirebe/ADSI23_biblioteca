import unittest

from . import BaseTestClass
from bs4 import BeautifulSoup

class test_HistorialReservas(BaseTestClass):

    # Comprobar que un libro SI devuelto SI se encuentra en el Historial de Lectura
    def test_libro_en_historial_lectura_despues_devolucion(self):
        # Hacer login del usuario
        self.login('james@gmail.com', '123456')

        # Obtener el ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID del libro que se espera encontrar en el historial de lectura
        libro_esperado_id = 1

        # Verificar si el libro está ahora en el historial de lectura después de la devolución
        libro_en_historial_lectura_despues = self.user_has_book_in_history(user_id, libro_esperado_id)
        self.assertTrue(libro_en_historial_lectura_despues,
                        f"El libro con ID {libro_esperado_id} está ahora en el historial de lectura del usuario después de la devolución")

        # Logout después de la prueba
        self.client.get('/logout')

    def user_has_book_in_history(self, user_id, book_id):
        # Realizar la consulta para verificar si el libro está en el historial de lectura del usuario
        history = self.db.select("""
            SELECT * FROM Reserva
            WHERE UsuarioIdU = ? AND IdCopiaLibro = ? AND FechaEntrega IS NOT NULL
            """, (user_id, book_id))

        # Si la consulta devuelve alguna reserva con FechaEntrega no nula, el libro está en el historial de lectura
        return len(history) > 0



    # Comprobar que un libro NO devuelto (pero SI reservado) NO se encuentra en el Historial de Lectura
    def test_libro_no_en_historial_lectura_sin_devolucion(self):
        # Hacer login del usuario
        self.login('james@gmail.com', '123456')

        # Obtener el ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID del libro que se espera no encontrar en el historial de lectura
        libro_esperado_id = 7

        # Verificar si el libro está inicialmente en el historial de lectura del usuario (antes de devolverlo)
        libro_en_historial_lectura = self.user_has_book_in_history(user_id, libro_esperado_id)
        self.assertFalse(libro_en_historial_lectura,
                         f"El libro con ID {libro_esperado_id} no está en el historial de lectura del usuario antes de devolverlo")

        # Realizar la reserva del libro sin devolverlo
        res = self.client.get('/reserve?id=7',
                              follow_redirects=True)  # Reemplaza 'reserve' por la ruta real de reserva en tu aplicación
        self.assertEqual(200, res.status_code)

        # Verificar si el libro sigue sin estar en el historial de lectura después de reservarlo
        libro_en_historial_lectura_despues = self.user_has_book_in_history(user_id, libro_esperado_id)
        self.assertFalse(libro_en_historial_lectura_despues,
                         f"El libro con ID {libro_esperado_id} sigue sin estar en el historial de lectura del usuario después de reservarlo")

        # Logout después de la prueba
        self.client.get('/logout')

    # Comprobar que un libro NO reservado NO se encuentra en el Historial de Lectura

    def test_libro_no_en_historial_lectura_sin_reserva(self):
        # Hacer login del usuario
        self.login('james@gmail.com', '123456')

        # Obtener el ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID del libro que se espera no encontrar en el historial de lectura
        libro_esperado_id = 10  # Cambia por el ID del libro que sabes que no está reservado

        # Verificar si el libro está inicialmente en el historial de lectura del usuario
        libro_en_historial_lectura = self.user_has_book_in_history(user_id, libro_esperado_id)
        self.assertFalse(libro_en_historial_lectura,
                         f"El libro con ID {libro_esperado_id} no está en el historial de lectura del usuario antes de intentar reservarlo")

        # Intentar reservar el libro que sabemos que no está reservado
        res = self.client.get('/reserve?id=10',
                              follow_redirects=True)  # Reemplaza 'reserve' por la ruta real de reserva en tu aplicación
        self.assertEqual(200, res.status_code)

        # Verificar si el libro sigue sin estar en el historial de lectura después de intentar reservarlo
        libro_en_historial_lectura_despues = self.user_has_book_in_history(user_id, libro_esperado_id)
        self.assertFalse(libro_en_historial_lectura_despues,
                         f"El libro con ID {libro_esperado_id} sigue sin estar en el historial de lectura del usuario después de intentar reservarlo")

        # Logout después de la prueba
        self.client.get('/logout')

if __name__ == '__main__':
    unittest.main()
