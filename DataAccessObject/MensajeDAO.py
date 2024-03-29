from DataSource.ConexionBD import Conexion
from TransferObject.AlertaDTO import Alerta

class Mensaje:
    def __init__(self):
        self.conexion_manager=Conexion()
        
    def InsertarMensaje(self,alert):
        con=None
        cursor=None
        if isinstance(alert, Alerta):
            id=alert.get_idA
            fecha=alert.get_fechaA
            Descripcion= alert.get_descripcionA
            nombreU=alert.get_nombreUAler
            id_S= alert.get_idSAler
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''INSERT INTO alerta (id_a,fecha_a,descripcion_a,nombre_u,id_s) VALUES('{}','{}','{}','{}','{}')'''.format(id,fecha,Descripcion,nombreU,id_S)
            cursor.execute(sql)
            con.commit()
            return True
        except Exception as e:
            print(f'Error al subir mensaje: {e}')
            return False
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
            
    def eliminarMensajesID(self,alert):
        con=None
        cursor=None
        if isinstance(alert, Alerta):
            id= alert.get_idA
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''DELETE FROM alerta WHERE id_a='{}' '''.format(id)
            cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al Eliminar mensaje: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)    
        