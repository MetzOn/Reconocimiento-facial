from DataAccessObject.EntrenamientoDAO import Entrenamiento

class EntrenamientoLOG:
    def __init__(self):
        self.EntrenamientSistLOG=Entrenamiento()
    
    def ObtenerListasSospNom_Cont(self):
       facesData,labels,Diccionario=self.EntrenamientSistLOG.ObtenerContenidoNombresSosp()
       return facesData,labels,Diccionario
    