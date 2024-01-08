import unittest
from . import BaseTestClass
from bs4 import BeautifulSoup
from .LibraryController import LibraryController

library = LibraryController()

class TestForo(BaseTestClass):
    
    def test_creacion_de_tema(self):
        # Prueba para verificar la creación de un nuevo tema
        res = self.login('jhon@gmail.com', '123')
        res = self.client.get('/forum')
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        select_element = page.find('select', id='selectTopic')
        options = select_element.find_all('option')
        self.assertEqual(3, len(options))
        
        tema = library.create_tema(1, "Libros sobre asesinos", "Busco libros sobre asesinos en serie")
        
        res = self.client.get('/forum')
        page = BeautifulSoup(res.data, features="html.parser")
        select_element = page.find('select', id='selectTopic')
        options = select_element.find_all('option')
        self.assertEqual(3, len(options))
  

class TestTemas(BaseTestClass):

    def test_agregar_mensaje_a_tema(self):
        res = self.login('jhon@gmail.com', '123')
        res = self.client.get('/ver-tema-3')
        page = BeautifulSoup(res.data, features="html.parser")
        
        self.assertTrue(len(page.find_all('div', class_='comment')) == 3)
        mensaje = library.crear_mensaje('1', '1', None , "asdfasdfasdfadsf")
        self.assertTrue(len(page.find_all('div', class_='comment')) == 4)
    


if __name__ == '__main__':
    unittest.main()
