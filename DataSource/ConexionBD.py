#Instalar pip install mysql-connector-python
import mysql.connector

class Conexion():
    def __init__(self):
        self.user= 'root'
        self.password=''
        self.host='localhost'
        self.database='bd_proyecto'
        self.port= '3306'
        
    def conectar(self):
        try:
            # Crea una conexión a la base de datos
            conexion = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database,
                port=self.port,
            )
            print(f'Conexión exitosa: {conexion}')
            return conexion
        except mysql.connector.Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None


    def desconectar(self, conexion, cursor):
        try:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
            print('Conexión cerrada')
        except mysql.connector.Error as e:
            print(f'Error al cerrar la conexión a la base de datos: {e}')
