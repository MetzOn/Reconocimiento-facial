#Generar el control de errores de las funciones que el programa va a ralizar con la BD (Uso del if, else, 
# true=se realizo la accion, false=Mostrar el error)

from TransferObject.SospechosoDTO import Sospechoso
from DataAccessObject.PerfilSospDAO import PerfilSospDAO

class PerfilSospLOG : 
    def __init__(self) :
        self.SospechosoLOG=PerfilSospDAO()
        
    def guardarDatosSosLOG(self,sospechoso):
        if isinstance(sospechoso, Sospechoso):
            mensajeAgMiem=True
            if(self.SospechosoLOG.insertarDatosSosp(sospechoso)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem
        else:
            print("Error BO MIEMBRO")
        
    def eliminarDatosSosLOG(self,id):
            if(self.SospechosoLOG.eliminarDatosSosp(id)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem

        
    
    def actualizarDatosSosLOG(self,sospechoso):
        if isinstance(sospechoso, Sospechoso):
            mensajeAgMiem=True
            if(self.SospechosoLOG.actualizarDatosSosp(sospechoso)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem
        else: 
            return mensajeAgMiem
    def obtenerIdSos(self,nombre):
        id=self.SospechosoLOG.obtenerIdSospechoso(nombre)
        return id
        
    def listarDatosSosLOG(self):
       lista=self.SospechosoLOG.mostrarDatosSosp()
       return lista
    def listarNombresSosLOG(self):
        nombres=self.SospechosoLOG.obtenerNombresSospechosos()
        return nombres
    
    def listarNombreSosxID(self,id):
        nombre=self.SospechosoLOG.obtenerNombreSosxID(id)
        return nombre
    