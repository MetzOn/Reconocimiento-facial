#Generar el control de errores de las funciones que el programa va a ralizar con la BD (Uso del if, else, 
# true=se realizo la accion, false=Mostrar el error)


from TransferObject.MiembroDTO import Miembro
from DataAccessObject.PerfilMiemDAO import PerfilMiembrosDAO

class PerfilMiemLOG:
    def __init__(self):
        self.MiembroLOG=PerfilMiembrosDAO()

       
    def guardarDatosMiemLOG(self,miembro):
        if isinstance(miembro, Miembro):
            mensajeAgMiem=True
            if(self.MiembroLOG.insertarDatosMiemb(miembro)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem
        else:
            print("Error BO MIEMBRO")
        
    def eliminarDatosMiemLOG(self,id):
            if(self.MiembroLOG.eliminarDatosMiemb(id)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem

        
    
    def actualizarDatosMiemLOG(self,miembro):
        if isinstance(miembro, Miembro):
            mensajeAgMiem=True
            if(self.MiembroLOG.actualizarDatosMiemb(miembro)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem
        else: 
            return mensajeAgMiem
        
    def mostrarDatosMiemLOG(self):
       lista=self.MiembroLOG.mostrarDatosMiemb()
       return lista
   
