class Alerta:
    def __init__(self,id_A,fecha_A,descripcion_A,nombre_UAler,id_SAler):
        self.__id_A=id_A
        self.__fecha_A=fecha_A
        self.__descripcion_A=descripcion_A
        self.__nombre_UAler=nombre_UAler
        self.__id_SAler=id_SAler
    
    def get_idA(self):
        return self.__id_A
    def set_idA(self,idA):
        self.__id_A=idA
        
        
    def get_fechaA(self):
        return self.__fecha_A
    def set_fechaA(self,fechaA):
        self.__fecha_A=fechaA
        
    
    def get_descripcionA(self):
        return self.__descripcion_A
    def set_descripcionA(self,descripcionA):
        self.__descripcion_A=descripcionA
    
    def get_nombreUAler(self):
        return self.__nombre_UAler
    def set_nombreUAler(self,nombreUAler):
        self.__nombre_UAler=nombreUAler
    
    def get_idSAler(self):
        return self.__id_SAler
    def set_idSAler(self,idSAler):
        self.__id_SAler=idSAler
        