import sqlite3

from .Connection import Connection
import datetime

db = Connection()

class Tema:
    def __init__(self, IdTema, autor, text, descr):
        self.TemaId = IdTema
        self.TemaAutor = autor
        self.TemaTexto = text
        self.TemaDescr = descr
        

class Mensaje:
    def __init__(self, idMnsj, usuId, temaId, receptor, texto, fechaHora):
        self.id = idMnsj
        self.idUsu =usuId
        self.idTema = temaId
        self.receptor = receptor
        self.textoMnsj = texto
        self.fechaHora = fechaHora
    
    
    