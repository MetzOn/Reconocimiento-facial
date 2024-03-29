from TransferObject.ImagenDTO import Imagen
from DataAccessObject.ImagenDAO import Image
from TransferObject.SospechosoDTO import Sospechoso

class ImagenLOG:
    def __init__(self):
        self.ImagenLOG=Image()
    
    def guardarImagen(self,imagen):
        if isinstance(imagen, Imagen):
            mensajeAgMiem=True
            if(self.ImagenLOG.insertarDatosImagen(imagen)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem
        else:
            print("Error BO IMAGEN, guardar")
    def eliminarImagenID(self, id):
        mensajeAgMiem=True
        if(self.ImagenLOG.eliminarImagenesID(id)):
            mensajeAgMiem=True
        else:
            mensajeAgMiem=False
        return mensajeAgMiem
        
    def eliminarImagenIdSosp(self,sospechoso):
        if isinstance(sospechoso, Sospechoso):
            mensajeAgMiem=True
            if(self.ImagenLOG.eliminarImagenesIDSOS(sospechoso)):
                mensajeAgMiem=True
            else:
                mensajeAgMiem=False
            return mensajeAgMiem
        else:
            print("Error BO IMAGEN, EliminarImagenxid")
        
    def listarImagenxId(self,id):
        lista=self.ImagenLOG.mostrarImagenesPorIDSos(id)
        return lista
    
    def MostrarImagenPorIDimagen(self,idImagen):
        imagen=self.ImagenLOG.VisualizarImagenPorID(idImagen)
        if imagen is not None and imagen.any():
            return imagen
        else:
            print("Error al obtener la imagen")
            return None