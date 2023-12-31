import unittest

from . import BaseTestClass
from bs4 import BeautifulSoup
class test_annadirActualizarResenna(BaseTestClass):

    # Comprobar que a un libro SI devuelto SIN reseña, se le añade correctamente una reseña

    # Comprobar que a un libro SI devuelto CON resena, se le actualiza la reseña anterior

    # Comprobar que a un libro NO devuelto, no se le puede realizar reseña

if __name__ == '__main__':
    unittest.main()
