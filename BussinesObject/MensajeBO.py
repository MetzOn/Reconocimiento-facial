#Generar el control de errores de las funciones que el programa va a ralizar con la BD (Uso del if, else, 
# true=se realizo la accion, false=Mostrar el error)

from TransferObject.AlertaDTO import Alerta
from DataAccessObject.MensajeDAO import Mensaje

class PerfilMiemLOG:
    def __init__(self):
        self.MensajeLOG=Mensaje()

    def InsertarMensaje(self,alerta):
        self.MensajeLOG.InsertarMensaje(alerta)
        return
        