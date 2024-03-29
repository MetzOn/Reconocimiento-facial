class Usuario:
    def __init__(self,nom_U,contr_U):
        self.__nom_U=nom_U
        self.__contr_U=contr_U
    
    def get_nombreU(self):
        return self.__nom_U
    
    def set_nombreU(self,nombreU):
        self.__nom_U=nombreU
    
    def get_contraseñaU(self):
        return self.__contr_U
    
    def set_contraseñaU(self,contraseñaU):
        self.__contr_U=contraseñaU
