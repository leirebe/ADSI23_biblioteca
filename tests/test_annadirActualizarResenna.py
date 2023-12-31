import unittest

from . import BaseTestClass
from bs4 import BeautifulSoup
class test_annadirActualizarResenna(BaseTestClass):

    # Comprobar que a un libro SI devuelto SIN reseña, se le añade correctamente una reseña
    def test_anadir_resena_a_libro_devuelto_sin_resena(self):
        # Hacer login del usuario
        self.login('james@gmail.com', '123456')

        # Obtener el ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID de un libro devuelto sin ninguna reseña asociada (asegúrate de tener un libro con esta condición en tu base de datos)
        libro_devuelto_sin_resena_id = 6

        # Verificar que el libro está devuelto pero sin reseñas asociadas
        libro_devuelto_sin_resena = self.book_has_no_review(libro_devuelto_sin_resena_id, user_id)
        self.assertTrue(libro_devuelto_sin_resena,
                        f"El libro con ID {libro_devuelto_sin_resena_id} está devuelto pero sin reseña")

        # Añadir una reseña al libro devuelto sin reseña
        comentario = "¡Genial!"
        puntuacion = 5

        res = self.client.post('/resennar', data={"id": libro_devuelto_sin_resena_id, "comentario": comentario,
                                                  "puntuacion": puntuacion}, follow_redirects=True)
        self.assertEqual(200, res.status_code)

        # Verificar que ahora el libro tiene una reseña asociada
        libro_con_resena = self.book_has_no_review(libro_devuelto_sin_resena_id, user_id)
        self.assertTrue(libro_con_resena,
                        f"El libro con ID {libro_devuelto_sin_resena_id} ahora tiene una reseña asociada")

        # Logout después de la prueba
        self.client.get('/logout')

    def book_has_no_review(self, book_id, user_id):
        # Verificar si el libro tiene reseñas asociadas para el usuario proporcionado
        reviews = self.db.select("SELECT * FROM Resenna WHERE UsuarioIdU = ? AND LibroIdLibro = ?", (user_id, book_id))
        return len(reviews) == 0

    # Comprobar que a un libro SI devuelto CON resena, se le actualiza la reseña anterior

    def test_actualizar_resena_libro_devuelto_con_resena(self):
        # Hacer login del usuario
        self.login('james@gmail.com', '123456')

        # Obtener el ID del usuario
        user_id = self.db.select("SELECT id from User where Email = ?", ('james@gmail.com',))[0][0]

        # Obtener el ID de un libro devuelto con una reseña existente asociada (asegúrate de tener un libro con esta condición en tu base de datos)
        libro_devuelto_con_resena_id = 1

        # Verificar que el libro está devuelto y tiene una reseña asociada
        libro_devuelto_con_resena = self.book_has_review(libro_devuelto_con_resena_id, user_id)
        self.assertTrue(libro_devuelto_con_resena,
                        f"El libro con ID {libro_devuelto_con_resena_id} está devuelto y tiene una reseña")

        # Añadir una nueva reseña al libro devuelto con reseña existente
        nuevo_comentario = "¡Una reseña actualizada para un libro genial!"
        nueva_puntuacion = 4

        res = self.client.post('/resennar', data={"id": libro_devuelto_con_resena_id, "comentario": nuevo_comentario,
                                                  "puntuacion": nueva_puntuacion}, follow_redirects=True)
        self.assertEqual(200, res.status_code)

        # Verificar que la reseña existente se ha actualizado con los nuevos valores
        reseña_actualizada = self.review_has_updated(libro_devuelto_con_resena_id, user_id, nuevo_comentario,
                                                     nueva_puntuacion)
        self.assertTrue(reseña_actualizada,
                        f"La reseña del libro con ID {libro_devuelto_con_resena_id} se ha actualizado con los nuevos valores")

        # Logout después de la prueba
        self.client.get('/logout')

    def book_has_review(self, book_id, user_id):
        # Verificar si el libro tiene una reseña asociada para el usuario proporcionado
        review = self.db.select("SELECT * FROM Resenna WHERE UsuarioIdU = ? AND LibroIdLibro = ?", (user_id, book_id))
        return len(review) > 0

    def review_has_updated(self, book_id, user_id, nuevo_comentario, nueva_puntuacion):
        # Verificar si la reseña del libro se ha actualizado con los nuevos valores
        review = self.db.select(
            "SELECT * FROM Resenna WHERE UsuarioIdU = ? AND LibroIdLibro = ? AND Comentario = ? AND puntuacion = ?",
            (user_id, book_id, nuevo_comentario, nueva_puntuacion))
        return len(review) > 0

if __name__ == '__main__':
    unittest.main()
