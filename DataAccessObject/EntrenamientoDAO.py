from DataSource.ConexionBD import Conexion
import cv2
import numpy as np


class Entrenamiento:
    def __init__(self):
        self.conexion_manager=Conexion()
        
    def ObtenerContenidoNombresSosp(self):
        con=None
        cursor=None
        facesData = []
        labels = []
        sospechoso_name_mapping = {}  # Un diccionario para hacer un seguimiento de los nombres de los sospechosos
        current_label = 0
        try:
            con = self.conexion_manager.conectar()
            cursor = con.cursor()
            sql = ''' SELECT imagen.contenido_i, sospechoso.nombre_s
                      FROM imagen
                      INNER JOIN sospechoso ON imagen.id_s = sospechoso.id_s'''
            cursor.execute(sql)
            for contenido_i, nombre_s in cursor:
                # Procesar la imagen desde el contenido binario
                image_array = np.frombuffer(contenido_i, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)  # Leer en escala de grises
                # Agregar la imagen
                facesData.append(image)
                # Asociar una etiqueta única al nombre del sospechoso
                if nombre_s not in sospechoso_name_mapping:
                    sospechoso_name_mapping[nombre_s] = current_label
                    current_label += 1
                labels.append(sospechoso_name_mapping[nombre_s])
            
            return facesData, labels, sospechoso_name_mapping
        
        except Exception as e:
            print(f'Error al Eliminar Imagen: {e}')
            return None
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
