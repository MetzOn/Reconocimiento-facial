#Generar las funciones para cada accion que el programa va a realizar con la BD
from DataSource.ConexionBD import Conexion
from TransferObject.SospechosoDTO import Sospechoso

class PerfilSospDAO:
    def __init__(self):
        self.conexion_manager=Conexion()
        
    def insertarDatosSosp(self,sospechoso):
        con=None
        cursor=None
        resp=None
        if isinstance(sospechoso, Sospechoso):
            nombre=sospechoso.get_nombreS()
            usuario= sospechoso.get_nombreUSos()
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''INSERT INTO Sospechoso (nombre_s,nombre_u) VALUES('{}','{}')'''.format(nombre,usuario)
            resp=cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al agregar datos de Miembro: {e}')
            resp=False
        finally:
            self.conexion_manager.desconectar(con, cursor)
        return resp
            
    
            
    def eliminarDatosSosp(self,id):
        resp = None
        con=None
        cursor=None
        
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''DELETE FROM sospechoso WHERE id_s='{}' '''.format(id)
            resp=cursor.execute(sql)
            con.commit()
        except Exception as e:
            print(f'Error al Obtener datos: {e}')
            resp =False
        finally:
            self.conexion_manager.desconectar(con, cursor)
        return resp
    def actualizarDatosSosp(self,sospechoso):
        con=None
        cursor=None
        if isinstance(sospechoso, Sospechoso):
            nombre=sospechoso.get_nombreS()
            usuario= sospechoso.get_nombreUSos()
            id= sospechoso.get_idS()
            
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql='''UPDATE sospechoso SET nombre_s='{}',nombre_u= '{}' WHERE id_s= '{}' '''.format(nombre,usuario,id)
            cursor.execute(sql)
            dato=cursor.rowcount
            con.commit()
            return dato
        except Exception as e:
            print(f'Error al Obtener datos: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
        
    def obtenerIdSospechoso(self,nombre):
        try:
            con=self.conexion_manager.conectar()
            con.autocommit=False
            cursor=con.cursor()
            sql = '''SELECT id_s FROM sospechoso WHERE nombre_s ='{}' '''.format(nombre)
            cursor.execute(sql)
            resultado = cursor.fetchone()
            con.commit()
            if resultado:
                id_obtenido = resultado[0]
                return id_obtenido
            else:
                return None
        except Exception as e:
            print("Error al obtener el ID del sospechoso:", e)
            return None
        finally:
            self.conexion_manager.desconectar(con, cursor)
    def mostrarDatosSosp(self):
        con=None
        cursor=None
        sospechosos = []
        try:
            con=self.conexion_manager.conectar()
            cursor=con.cursor()
            sql="SELECT * FROM sospechoso"
            cursor.execute(sql)
            datos= cursor.fetchall()
            for tupla in datos:
                id=tupla[0]
                nombre = tupla[1]
                usuario = tupla[2]
                sospechosoM = Sospechoso(id,nombre, usuario)
                sospechosos.append(sospechosoM)
            return sospechosos
        except Exception as e:
            print(f'Error al Obtener datos: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
        
    def obtenerNombresSospechosos(self):
        nombres = []
        try:
            con=self.conexion_manager.conectar()
            cursor=con.cursor()
            sql="SELECT nombre_s FROM sospechoso"
            cursor.execute(sql)
            nombres = [row[0] for row in cursor.fetchall()]
            return nombres
        except Exception as e:
            print(f'Error al Obtener nombres de sospechosos: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)
            
    def obtenerNombreSosxID(self,id):
        try:
            con=self.conexion_manager.conectar()
            cursor=con.cursor()
            sql='''SELECT nombre_s FROM sospechoso where id_s='{}' '''.format(id)
            cursor.execute(sql)
            nombre = cursor.fetchone()  
            return nombre[0] if nombre else None
        except Exception as e:
            print(f'Error al Obtener nombres de sospechosos: {e}')
        finally:
            self.conexion_manager.desconectar(con, cursor)