from DataSource.ConexionBD import Conexion
from TransferObject.ImagenDTO import Imagen
from TransferObject.SospechosoDTO import Sospechoso
import cv2
import numpy as np

class Image:
    def __init__(self):
        self.conexion_manager=Conexion()
        
        
    def insertarDatosImagen(self,imag):
        con=None
        cursor=None
        if isinstance(imag, Imagen):
            
            nombre=imag.get_nombreI()
            contenido=imag.get_contenidoI()
            Id_Sospechoso= imag.get_idSIma()
            
            
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql="INSERT INTO imagen (nombre_i, contenido_i, id_s) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, contenido, Id_Sospechoso))
            con.commit()
        except Exception as e:
            print(f'Error al agregar Imagen: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
            
    def eliminarImagenesID(self,id):
        con=None
        cursor=None
        resp=None
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''DELETE FROM imagen WHERE id_i='{}' '''.format(id)
            resp=cursor.execute(sql)
            con.commit()
            return resp
        except Exception as e:
            print(f'Error al Eliminar Imagen: {e}')
            return resp
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
    def eliminarImagenesIDSOS(self,sospechoso):
        con=None
        cursor=None
        if isinstance(sospechoso, Sospechoso):
            idSosp=sospechoso.get_idS()
 
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''DELETE FROM imagen WHERE id_s='{}' '''.format(idSosp)
            cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al Eliminar Imagenes: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
    def mostrarImagenesPorIDSos(self,idPIm):
        con=None
        cursor=None
        ImagenesxID = []
        try:
            con=self.conexion_manager.conectar()
            cursor=con.cursor()
            sql='''SELECT * FROM imagen WHERE id_s='{}' '''.format(idPIm)
            cursor.execute(sql)
            datos= cursor.fetchall()
            for tupla in datos:
                id=tupla[0]
                nombre = tupla[1]
                contenido=tupla[2]
                ImagenM = Imagen(id,nombre,contenido,idPIm)
                ImagenesxID.append(ImagenM)
            return ImagenesxID
        except Exception as e:
            print(f'Error al Obtener Imagenes por ID: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
    
    def VisualizarImagenPorID(self,idImagen):
        con=None
        cursor=None
        
        try:
            con=self.conexion_manager.conectar()
            cursor=con.cursor()
            sql='''SELECT contenido_i FROM imagen WHERE id_i='{}' '''.format(idImagen)
            cursor.execute(sql)
            contenido_i =cursor.fetchone()
            if contenido_i:
                # Procesar la imagen desde el contenido binario
                image_array = np.frombuffer(contenido_i[0], np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)
            return image
    
        except Exception as e:
            print(f'Error al visualizar Imagen: {e}')
            return None
        finally:
            self.conexion_manager.desconectar(con, cursor)
        