from controller.GestorUsuario import GestorUsuario

class Sistema:
    
    def __init__(self) -> None:
        self.gestorUsuario = GestorUsuario()

    def generarListaRecomendaciones(self, userid: int):
        historialReservas = self.gestorUsuario.obtenerHistorialReservas(userid)
        print(historialReservas)