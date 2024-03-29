#Generar las funciones para cada accion que el programa va a realizar con la BD

import sys
sys.path.append('c:\\Users\\DARMUX\\Desktop\\ReconocimientoF_Proyect\\DataSource')
sys.path.insert(0, 'c:\\Users\\DARMUX\\Desktop\\ReconocimientoF_Proyect\\DataSource')

print(sys.path)

from DataSource.ConexionBD import Conexion
from TransferObject.MiembroDTO import Miembro

class PerfilMiembrosDAO:
    def __init__(self):
        self.conexion_manager=Conexion()
        
    def insertarDatosMiemb(self,miembro):
        resp = False
        con=None
        cursor=None
        if isinstance(miembro, Miembro):
            nombre=miembro.get_nombreM()
            correo= miembro.get_correoM()
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''INSERT INTO miembro (nombre_m,correo_m) VALUES('{}','{}')'''.format(nombre,correo)
            resp=cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al agregar datos de Miembro: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
        return resp
    
    def mostrarDatosMiemb(self):
        con=None
        cursor=None
        miembros = []
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql="SELECT * FROM miembro"
            cursor.execute(sql)
            datos= cursor.fetchall()
            for tupla in datos:
                id=tupla[0]
                nombre = tupla[1]
                correo = tupla[2]
                miembro = Miembro()
                miembro.set_idM(id)
                miembro.set_nombreM(nombre)
                miembro.set_correoM(correo)
                miembros.append(miembro)
            con.commit()
        except Exception as e:
            print(f'Error al Obtener datos: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
        return miembros
        
    def eliminarDatosMiemb(self,id):
        resp = None
        con=None
        cursor=None
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''DELETE FROM miembro WHERE id_m='{}' '''.format(int(id))
            resp=cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al Obtener datos: {e}')
            resp =False
        finally:
            self.conexion_manager.desconectar(con, cursor)
        return resp
            
    def actualizarDatosMiemb(self,miembro):
        resp =None
        con=None
        cursor=None
        if isinstance(miembro, Miembro):
            nombre=miembro.get_nombreM()
            correo= miembro.get_correoM()
            id= miembro.get_idM()
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''UPDATE miembro SET nombre_m='{}',correo_m= '{}' WHERE id_m= '{}' '''.format(nombre,correo,id)
            resp=cursor.execute(sql)
            dato=cursor.rowcount
            con.commit()
            return dato
        except Exception as e:
            print(f'Error al Obtener datos: {e}')
            resp =False
        finally:
            self.conexion_manager.desconectar(con, cursor)
        return resp
            
            
        
            
lista=PerfilMiembrosDAO()
LISTA=lista.mostrarDatosMiemb
print (LISTA)