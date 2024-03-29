class Miembro:
    def __init__(self,id_M=None,nombre_M=None,correo_M=None):
        if id_M is None and nombre_M is None and correo_M is None :
            self.__id_M=None
            self.__nombre_M=None
            self.__correo_M=None
        else:
            self.__id_M=id_M
            self.__nombre_M=nombre_M
            self.__correo_M=correo_M

        
    def get_idM(self):
        return self.__id_M
    def set_idM(self,idM):
        self.__id_M=idM
        
        
    def get_nombreM(self):
        return self.__nombre_M
    def set_nombreM(self,nombreM):
        self.__nombre_M=nombreM
        
    
    def get_correoM(self):
        return self.__correo_M
    def set_correoM(self,correoM):
        self.__correo_M=correoM