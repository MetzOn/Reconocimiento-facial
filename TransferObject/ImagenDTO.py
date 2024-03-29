class Imagen:
    def __init__(self,id_I=None,nombre_I=None,contenido_I=None,id_S=None):
        if id_I is None and nombre_I is None and contenido_I is None and id_S is None:
            self.__id_I=None
            self.__nombre_I=None
            self.__contenido_I=None
            self.__id_SIma=None
        else:
            self.__id_I=id_I
            self.__nombre_I=nombre_I
            self.__contenido_I=contenido_I
            self.__id_SIma=id_S
    
    def get_idI(self):
        return self.__id_I
    def set_idI(self,idI):
        self.__id_I=idI
        
        
    def get_nombreI(self):
        return self.__nombre_I
    def set_nombreI(self,nombreI):
        self.__nombre_I=nombreI
        
    
    def get_contenidoI(self):
        return self.__contenido_I
    def set_contenidoI(self,contenidoI):
        self.__contenido_I=contenidoI
    
    def get_idSIma(self):
        return self.__id_SIma
    def set_idSIma(self,idSIma):
        self.__id_SIma=idSIma