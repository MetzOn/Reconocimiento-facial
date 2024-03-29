#Generar las funciones para cada accion que el programa va a realizar con la BD
from DataSource.ConexionBD import Conexion
from TransferObject.UsuarioDTO import Usuario

class PerfilUsuario:
    def __init__(self):
        self.conexion_manager=Conexion()
    def insertarDatosUsuario(self,usuar):
        con=None
        cursor=None
        if isinstance(usuar, Usuario):
            nombre=usuar.get_nombreU()
            contraseña= usuar.get_contraseñaU()
            
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''INSERT INTO usuario (nombre_u,contraseña_u) VALUES('{}','{}')'''.format(nombre,contraseña)
            cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al agregar datos de Usuario: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
    def mostrarDatosUsuario(self):
        con=None
        cursor=None
        usuarios = []
        try:
            con=self.conexion_manager.conectar()
            cursor=con.cursor()
            sql="SELECT * FROM usuario"
            cursor.execute(sql)
            datos= cursor.fetchall()
            for tupla in datos:
                nombre=tupla[0]
                contraseña = tupla[1]
                
                usuario = Usuario(nombre, contraseña)
                usuarios.append(usuario)
            return usuarios
        except Exception as e:
            print(f'Error al Obtener datos Usuario: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
    def eliminarDatosUsuario(self,usuar):
        con=None
        cursor=None
        if isinstance(usuar, Usuario):
            id= usuar.get_nombreU()
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''DELETE FROM usuario WHERE nombre_u='{}' '''.format(id)
            cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al Elimiar datos Usuario: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
    def actualizarDatosUsuario(self,usuar):
        con=None
        cursor=None
        if isinstance(usuar, Usuario):
            nombre=usuar.get_nombreU()
            contraseña= usuar.get_contraseñaU()
            
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''UPDATE usuario SET contraseña_u= '{}' WHERE nombre_u= '{}' '''.format(contraseña,nombre)
            cursor.execute(sql)
            dato=cursor.rowcount
            con.commit()
            return dato
        except Exception as e:
            print(f'Error al Actualizar datos Usuario: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
    