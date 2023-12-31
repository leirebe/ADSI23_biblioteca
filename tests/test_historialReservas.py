import unittest

from . import BaseTestClass
from bs4 import BeautifulSoup

class test_HistorialReservas(BaseTestClass):

    # Comprobar que un libro SI devuelto SI se encuentra en el Historial de Lectura

    # Comprobar que un libro NO devuelto (pero SI reservado) SI se encuentra en el Historial de Lectura

    # Comprobar que un libro NO reservado) NO se encuentra en el Historial de Lectura

if __name__ == '__main__':
    unittest.main()
