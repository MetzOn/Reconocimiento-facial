class Sospechoso:
    def __init__(self,id_S=None,nombre_S=None,nombre_U=None):
        if id_S is None and nombre_S is None and nombre_U is None:
            self.__id_S=None
            self.__nombre_S=None
            self.__nombre_U=None
        else:
            self.__id_S=id_S
            self.__nombre_S=nombre_S
            self.__nombre_U=nombre_U
    
    def get_idS(self):
        return self.__id_S
    
    def set_idS(self,idS):
        self.__id_S=idS
        
    def get_nombreS(self):
        return self.__nombre_S
    
    def set_nombreS(self,nombreS):
        self.__nombre_S=nombreS
        
    def get_nombreUSos(self):
        return self.__nombre_U
    
    def set_nombreUSos(self,nombreU):
        self.__nombre_U=nombreU
    
    
    
    