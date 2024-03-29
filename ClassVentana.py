
import sys


print(sys.path)


import customtkinter
import tkinter.messagebox as messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import cv2.face
from email.message import EmailMessage
import smtplib
import time
import json
import imutils 
import numpy as np
import re
from io import BytesIO
from PIL import Image, ImageTk
import os
from BussinesObject.PerfilMiemBO import PerfilMiemLOG
from TransferObject.MiembroDTO import Miembro
from BussinesObject.PerfilSospBO import PerfilSospLOG
from TransferObject.SospechosoDTO import Sospechoso
from BussinesObject.imagenBO import ImagenLOG
from TransferObject.ImagenDTO import Imagen
from BussinesObject.EntrenamientoBO import EntrenamientoLOG
import imghdr
from datetime import datetime
import pygame




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Creacion de ventana
        pygame.init()
        self.sonido_emergente = pygame.mixer.Sound('D:/ojp/ReconocimientoF_Proyect/Interfaz/audio/MensajeAlerta.wav')
        self.title("RECONOCIMIENTO FACIAL")
        self.geometry("1000x600")
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=90)
        self.grid_rowconfigure(0, weight=1)
        self.cap=None
        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.face_recognizer= cv2.face.LBPHFaceRecognizer_create()
        self.miembro=Miembro()
        self.BOMiembro=PerfilMiemLOG()
        self.BOSospechoso=PerfilSospLOG()
        self.sospechoso=Sospechoso()
        self.BOImagen=ImagenLOG()
        self.Imagen=Imagen()
        self.BOEntrenamiento=EntrenamientoLOG()
        self.ListImagenesC=[]
        self.ListImagenesN=[]
        self.NombresSos=[]
        self.indicesReconocimiento=[]
        self.Diccionario={}
        self.etiqueta_sospechoso_mapping = {etiqueta: nombre for nombre, etiqueta in self.Diccionario.items()}
        self.tiempo_inicio_nombre = None
        self.nombre_detectado_actual = None
        self.nombre_guardado = None
        self.captura_pausada = False
        
        #Creacion de Frames
        self.frame_A = customtkinter.CTkFrame(self)
        self.frame_A.grid(row=0, column=0, padx=(10, 2), sticky="nswe")
        self.frame_B = customtkinter.CTkFrame(self)
        self.frame_B.grid(row=0, column=1, padx=(10, 2), sticky="nswe")
        self.frame_C = customtkinter.CTkFrame(self)
        self.frame_C.grid(row=0, column=1, padx=(10, 2), sticky="nswe")
        self.frame_D = customtkinter.CTkFrame(self)
        self.frame_D.grid(row=0, column=1, padx=(10, 2), sticky="nswe")
        self.frame_E = customtkinter.CTkFrame(self)
        self.frame_E.grid(row=0, column=1, padx=(10, 2), sticky="nswe")
        
        #OCULTAMOS FRAME_C
        self.frame_C.grid_remove()
        self.frame_D.grid_remove()
        self.frame_E.grid_remove()
        
        #################################################
        ################# FRAME A - Botones##############
        #################################################
        
        #Darle proporcion a los Frames
        self.frame_A.grid_columnconfigure(0, weight=1)
        self.frame_A.grid_rowconfigure(0, weight=10)
        self.frame_A.grid_rowconfigure(1, weight=5)
        self.frame_A.grid_rowconfigure(2, weight=85)
      
        #Creacion de Sub FRAMES
        self.frame_A_1Image = customtkinter.CTkFrame(self.frame_A)
        self.frame_A_1Image.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nswe")
        
        self.frame_A_2Admin = customtkinter.CTkFrame(self.frame_A)
        self.frame_A_2Admin.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
        self.frame_A_3Botones = customtkinter.CTkFrame(self.frame_A)
        self.frame_A_3Botones.grid( row=2, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
       
        
        #Centrar datos
        self.frame_A_1Image.grid_columnconfigure(0, weight=1)
        self.frame_A_1Image.grid_rowconfigure(0, weight=1)
        
        self.frame_A_2Admin.grid_columnconfigure(0, weight=1)
        self.frame_A_2Admin.grid_rowconfigure(0, weight=1)
        self.frame_A_2Admin.grid_rowconfigure(1, weight=1)
       
        #AGREGAR IMAGEN A FRAME A1IMAGEN
        try:
            self.imagenAdmin = customtkinter.CTkImage(light_image=Image.open("D:/ReconocimientoF_Proyect/Interfaz/Image/userIcon.png"),
                                                      dark_image=Image.open("D:/ReconocimientoF_Proyect/Interfaz/Image/userIcon.png"),
                                                      size=(200,200))
            self.labelContenedorImagen = customtkinter.CTkLabel(self.frame_A_1Image, image=self.imagenAdmin,text="") 
            self.labelContenedorImagen.grid(row=0, column=0, padx=3, pady=(3, 3))
            
        except  Exception as e:
            if type(e) == FileNotFoundError:
                # Si se trata de un error de tipo FileNotFoundError, muestra un mensaje
                messagebox.showerror("Error", "La imagen no se ha encontrado")
            else:
                messagebox.showerror("Error", f"{e}")
        
        #Agregar datos del Admin:
        self.lblNombre = customtkinter.CTkLabel(self.frame_A_2Admin, text="Nombre: User",font=("Hevelica",16))
        self.lblNombre.grid( row=0, column=0, padx=5, pady=(5, 3), sticky="we")
        
        self.lblEstado = customtkinter.CTkLabel(self.frame_A_2Admin, text="Estado: Activo",font=("Hevelica",16))
        self.lblEstado.grid( row=1, column=0, padx=5, pady=(0, 3), sticky="we")
        
        #Agregar Botones:
        self.btnVisualizarCam = customtkinter.CTkButton(self.frame_A_3Botones, text="Visualizar Camara",command=self.mostrarFrameB)
        self.btnVisualizarCam.grid(row=0, column=0, padx=10, pady=(5,5), sticky="ew")
        self.btnMiembros = customtkinter.CTkButton(self.frame_A_3Botones, text="Miembros",command=self.mostrarFrameD)
        self.btnMiembros.grid(row=1, column=0, sticky="ew", padx=10,pady=(5,5))
        self.btnSubirImagenBD = customtkinter.CTkButton(self.frame_A_3Botones, text="Sospechoso",command=self.mostrarFrameC)
        self.btnSubirImagenBD.grid(row=2, column=0, padx=10, pady=(5,5), sticky="ew")
        self.btnImagenGest= customtkinter.CTkButton(self.frame_A_3Botones, text="Imagen",command=self.mostrarFrameE)
        self.btnImagenGest.grid(row=3, column=0, padx=10, pady=(5,5), sticky="ew")
        self.btnSalir = customtkinter.CTkButton(self.frame_A_3Botones, text="Salir",command=self.salir)
        self.btnSalir.grid(row=4, column=0, sticky="ew", padx=10,pady=(5,5))
        


        #Centrar botones
        self.frame_A_3Botones.grid_columnconfigure(0, weight=1)
        self.frame_A_2Admin.grid_rowconfigure(0, weight=10)
        self.frame_A_2Admin.grid_rowconfigure(1, weight=10)
        self.frame_A_2Admin.grid_rowconfigure(2, weight=80)
        
        #################################################
        #################### FRAME B ####################
        #################################################
        
        #Darle proporcion a los Frames
        self.frame_B.grid_columnconfigure(0, weight=1)
        self.frame_B.grid_rowconfigure(0, weight=10)
        self.frame_B.grid_rowconfigure(1, weight=80)
        self.frame_B.grid_rowconfigure(2, weight=10)
        
         #Creacion de Sub FRAMES
        self.frame_B_1Encabezado = customtkinter.CTkFrame(self.frame_B)
        self.frame_B_1Encabezado.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nswe")
        
        self.frame_B_2Video = customtkinter.CTkFrame(self.frame_B)
        self.frame_B_2Video.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
        self.frame_B_3Footer = customtkinter.CTkFrame(self.frame_B)
        self.frame_B_3Footer.grid( row=2, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
         #Centrar datos
        self.frame_B_1Encabezado.grid_columnconfigure(0, weight=1)
        self.frame_B_1Encabezado.grid_rowconfigure(0, weight=1)
        self.frame_B_1Encabezado.grid_rowconfigure(1, weight=1)
        
        self.frame_B_2Video.grid_columnconfigure(0, weight=1)
        self.frame_B_2Video.grid_rowconfigure(0, weight=1)
        
        self.frame_B_3Footer.grid_columnconfigure(0, weight=1)
        
        #CREACION DE WIDGETS:
        self.lblInfo1=customtkinter.CTkLabel(self.frame_B_1Encabezado,text="VIDEO DE ENTRADA")
        self.lblInfo1.grid(column=0,row=0)
        
        self.BtnIniciarVideo= customtkinter.CTkButton(self.frame_B_1Encabezado,text="INICIAR VIDEO",command=self.video_de_entrada)
        self.BtnIniciarVideo.grid(column=0, row=1)
        
        self.lblVideo = Label(self.frame_B_2Video,text="",bg="#333333")
        self.lblVideo.grid(column=0,row=2)
        
        self.btnEnd= customtkinter.CTkButton(self.frame_B_3Footer,text="Finalizar Visualizacion", state="disable",command=self.finalizar_video)
        self.btnEnd.grid(column=0, row=1, pady=(40,0), sticky="ns")

        #################################################
        ############## FRAME C SOSPECHOSO ###############
        #################################################
        
        #Darle proporcion a los Frames
        self.frame_C.grid_columnconfigure(0, weight=1)
        self.frame_C.grid_rowconfigure(0, weight=10)
        self.frame_C.grid_rowconfigure(1, weight=90)
       
        
         #Creacion de Sub FRAMES
        self.frame_C1Title = customtkinter.CTkFrame(self.frame_C)
        self.frame_C1Title.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nswe")
        
        self.frame_C2SubirImagen = customtkinter.CTkFrame(self.frame_C)
        self.frame_C2SubirImagen.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
    
        
         #CREACION DE WIDGETS:
        self.lblTitulo=customtkinter.CTkLabel(self.frame_C1Title,text="CREAR PERFIL DE SUJETO SOSPECHOSO")
        self.lblTitulo.grid(column=0,row=0)
        self.tfC1ID=customtkinter.CTkEntry(self.frame_C1Title, width=50, height=20)
        self.tfC1ID.grid(column=1,row=0,sticky="e", padx=3)
        self.tfC1ID.configure(state="disabled")
        
        
        self.lblNombreS=customtkinter.CTkLabel(self.frame_C2SubirImagen,text="Nombre del sospechoso:")
        self.lblNombreS.grid(column=0,row=1,pady=(20, 10))
        
        self.tfDatoNombreS=customtkinter.CTkEntry(self.frame_C2SubirImagen, placeholder_text="Ingrese el nombre")
        self.tfDatoNombreS.grid(column=1,row=1,pady=(20, 10))
        
        self.BtnC1RecortarI= customtkinter.CTkButton(self.frame_C2SubirImagen,text="Recortar Imagenes",command=self.recortarRostrosEnImagenes)
        self.BtnC1RecortarI.grid(column=0, row=2,pady=(10, 10))
        self.BtnC1SubImagen= customtkinter.CTkButton(self.frame_C2SubirImagen,text="Subir Imagenes",command=self.subir_imagenGuarddatos)
        self.BtnC1SubImagen.grid(column=1, row=2,pady=(10, 10))
        
        #TABLA
        self.TablaC1Tabla = ttk.Treeview(self.frame_C2SubirImagen,columns=("ID","Nombre","Usuario","#Imagenes"))
        self.TablaC1Tabla.grid(column=0,row=3,padx=10,pady=10,columnspan=2)
        self.TablaC1Tabla.bind('<ButtonRelease-1>', self.cargar_datos_seleccionadosS)
     
        self.TablaC1Tabla.column("#0", width=0)
        self.TablaC1Tabla.column("#1", width=90)
        self.TablaC1Tabla.column("#2", width=200)
        self.TablaC1Tabla.column("#3", width=200)
        self.TablaC1Tabla.column("#4", width=150)
        
        self.TablaC1Tabla.heading('#1',text="ID")
        self.TablaC1Tabla.heading('#2',text="NOMBRE")
        self.TablaC1Tabla.heading('#3',text="USUARIO")
        self.TablaC1Tabla.heading('#4',text="#IMAGENES")
        
        
        self.BtnC1GuardarDat= customtkinter.CTkButton(self.frame_C2SubirImagen,text="Guardar",command=self.GuardarDatosSospechoso)
        self.BtnC1GuardarDat.grid(column=0, row=4,pady=(10, 5))
        
        self.BtnC1MostrarDat= customtkinter.CTkButton(self.frame_C2SubirImagen,text="Mostrar",command=self.listarSospechoso)
        self.BtnC1MostrarDat.grid(column=1, row=4,pady=(10, 5))
        
        self.BtnC1EliminarDat= customtkinter.CTkButton(self.frame_C2SubirImagen,text="Eliminar",command=self.eliminarSos)
        self.BtnC1EliminarDat.grid(column=0, row=5,pady=(5, 5))
        
        self.BtnC1ActualizarDat= customtkinter.CTkButton(self.frame_C2SubirImagen,text="Actualizar",command=self.ActualizarDatos)
        self.BtnC1ActualizarDat.grid(column=1, row=5,pady=(5, 5))
        
        
        
        #Centrar datos
        self.frame_C1Title.grid_columnconfigure(0, weight=1)
        self.frame_C1Title.grid_rowconfigure(0, weight=1)
        
        self.frame_C2SubirImagen.grid_columnconfigure(0, weight=1)
        self.frame_C2SubirImagen.grid_columnconfigure(1, weight=1)
        
        
        
        #################################################
        ############### FRAME D-MIEMBROS ################
        #################################################
        
        #Darle proporcion a los Frames
        self.frame_D.grid_columnconfigure(0, weight=1)
        self.frame_D.grid_rowconfigure(0, weight=50)
        self.frame_D.grid_rowconfigure(1, weight=50)
        
        #Creacion de Sub FRAMES
        self.frame_D1Form = customtkinter.CTkFrame(self.frame_D)
        self.frame_D1Form.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nswe")
        
        self.frame_D1Table = customtkinter.CTkFrame(self.frame_D)
        self.frame_D1Table.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
        #CREACION DE WIDGETS:
            #### FORM ######
        self.lblD1Titulo=customtkinter.CTkLabel(self.frame_D1Form,text="AÑADIR NUEVO MIEMBRO")
        self.lblD1Titulo.grid(column=0,row=0, columnspan=2)
        
        self.tfD1ID=customtkinter.CTkEntry(self.frame_D1Form, width=100, height=20)
        self.tfD1ID.grid(column=1,row=0,sticky="e", padx=3)
        self.tfD1ID.configure(state="disabled")
        
        
        self.lblD1NombreM=customtkinter.CTkLabel(self.frame_D1Form,text="Nombre del Miembro:")
        self.lblD1NombreM.grid(column=0,row=1,sticky="e", padx=10)
        
        self.lblD1CorreoM=customtkinter.CTkLabel(self.frame_D1Form,text="Correo del Miembro:")
        self.lblD1CorreoM.grid(column=0,row=2,sticky="e",padx=10)
        
        self.tfD1NombreM=customtkinter.CTkEntry(self.frame_D1Form, placeholder_text="Ingrese el Nombre")
        self.tfD1NombreM.grid(column=1,row=1,sticky="w", padx=10)
        
        self.tfD1CorreoM=customtkinter.CTkEntry(self.frame_D1Form, placeholder_text="Ejemplo@gmail.com")
        self.tfD1CorreoM.grid(column=1,row=2,sticky="w", padx=10)
        
        self.BtnD1AñadirM= customtkinter.CTkButton(self.frame_D1Form,text="Agregar Miembro",command=self.guardarDatMiem)
        self.BtnD1AñadirM.grid(column=0, row=3)
        
        self.BtnD1ActualizarM= customtkinter.CTkButton(self.frame_D1Form,text="Actualizar Miembro",command=self.actualizarInfoMiemb)
        self.BtnD1ActualizarM.grid(column=1, row=3)
        
        ###Table##
  
        
        self.BtnD1MostrarM= customtkinter.CTkButton(self.frame_D1Table,text="Listar Miembros",command=self.listarMiembros)
        self.BtnD1MostrarM.grid(column=0, row=0,pady=(10,3))
        self.BtnD1EliminarM= customtkinter.CTkButton(self.frame_D1Table,text="Eliminar Miembro",command=self.eliminarMiem)
        self.BtnD1EliminarM.grid(column=1, row=0,pady=(10,3))
        self.TablaD1Tabla = ttk.Treeview(self.frame_D1Table,columns=("ID","Nombre","Correo"))
        self.TablaD1Tabla.grid(column=0,row=1,padx=10,pady=(0,10),columnspan=2)
        
        self.TablaD1Tabla.bind('<ButtonRelease-1>', self.cargar_datos_seleccionados)


     
        self.TablaD1Tabla.column("#0", width=0)
        self.TablaD1Tabla.heading('#1',text="ID")
        self.TablaD1Tabla.heading('#2',text="NOMBRE")
        self.TablaD1Tabla.heading('#3',text="CORREO")
        
        
        ###Centrar##
        
        self.frame_D1Form.grid_columnconfigure(0, weight=50)
        self.frame_D1Form.grid_columnconfigure(1, weight=50)
        self.frame_D1Form.grid_rowconfigure(0, weight=10)
        self.frame_D1Form.grid_rowconfigure(1, weight=30)
        self.frame_D1Form.grid_rowconfigure(2, weight=30)
        self.frame_D1Form.grid_rowconfigure(3, weight=30)
        
        self.frame_D1Table.grid_columnconfigure(0, weight=50)
        self.frame_D1Table.grid_columnconfigure(1, weight=50)
        self.frame_D1Table.grid_rowconfigure(0, weight=10)
        self.frame_D1Table.grid_rowconfigure(1, weight=90)
        
        #################################################
        ################# FRAME E- IMAGEN ###############
        #################################################
        
        #Darle proporcion a los Frames
        self.frame_E.grid_columnconfigure(0, weight=1)
        self.frame_E.grid_rowconfigure(0, weight=20)
        self.frame_E.grid_rowconfigure(1, weight=80)
        
        #Creacion de Sub FRAMES
        self.frame_E1Form = customtkinter.CTkFrame(self.frame_E)
        self.frame_E1Form.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
        self.frame_E1Table = customtkinter.CTkFrame(self.frame_E)
        self.frame_E1Table.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nswe")
        
        #CREACION DE WIDGETS:
            #### FORM ######
        self.lblE1Titulo=customtkinter.CTkLabel(self.frame_E1Form,text="GESTIONAR IMAGENES")
        self.lblE1Titulo.grid(column=0,row=0, columnspan=2)
        
        self.lblE1NombreS=customtkinter.CTkLabel(self.frame_E1Form,text="Elije un sospechoso:")
        self.lblE1NombreS.grid(column=0,row=1)
        
        self.cbSospechosos = ttk.Combobox(self.frame_E1Form)
        self.cbSospechosos.grid(column=1,row=1)
        
        self.cbSospechosos.bind("<<ComboboxSelected>>", self.ListarImagenes)

        
        
        self.lblE1ID=customtkinter.CTkLabel(self.frame_E1Form,text="ID")
        self.lblE1ID.grid(column=0,row=2)
        
        self.lblE1Nombre=customtkinter.CTkLabel(self.frame_E1Form,text="NOMBRE")
        self.lblE1Nombre.grid(column=1,row=2)
        
        self.tfE1ID=customtkinter.CTkEntry(self.frame_E1Form, width=100, height=20)
        self.tfE1ID.grid(column=0,row=3, padx=3)
        
        self.tfE1nombreI=customtkinter.CTkEntry(self.frame_E1Form, width=100, height=20)
        self.tfE1nombreI.grid(column=1,row=3, padx=3)
        
        self.BtnE1Limpiar= customtkinter.CTkButton(self.frame_E1Form,text="Limpiar casillas",command=self.limpiarCasillas)
        self.BtnE1Limpiar.grid(column=0, row=4)
        
        self.BtnE1Recortar= customtkinter.CTkButton(self.frame_E1Form,text="Recortar Imagen",command=self.recortarRostrosEnImagenes)
        self.BtnE1Recortar.grid(column=1, row=4)
                
        self.lblE1Titulo=customtkinter.CTkLabel(self.frame_E1Table,text="IMAGENES")
        self.lblE1Titulo.grid(column=0,row=0, columnspan=2)
        
        self.TablaE1Tabla = ttk.Treeview(self.frame_E1Table,columns=("ID","Nombre","ID Sospechoso"))
        self.TablaE1Tabla.grid(column=0,row=1,padx=10,pady=(0,10),columnspan=2)
        
        self.TablaE1Tabla.column("#0", width=0)
        self.TablaE1Tabla.heading('#1',text="ID")
        self.TablaE1Tabla.heading('#2',text="NOMBRE")
        self.TablaE1Tabla.heading('#3',text="ID SOSPECHOSO")
        
        self.TablaE1Tabla.bind('<ButtonRelease-1>', self.cargarDatosSeleccionadosImagen)
        
        self.BtnE1EliminarI= customtkinter.CTkButton(self.frame_E1Table,text="Eliminar Imagen",command=self.eliminarImagenPorID)
        self.BtnE1EliminarI.grid(column=1, row=2,sticky="n")
        
        self.BtnE1AñadirI= customtkinter.CTkButton(self.frame_E1Table,text="Agregar Imagen",command=self.agregarImagenes)
        self.BtnE1AñadirI.grid(column=0, row=2,sticky="n")
        
        self.frame_E1Form.grid_columnconfigure(0, weight=50)
        self.frame_E1Form.grid_columnconfigure(1, weight=50)
        self.frame_E1Form.grid_rowconfigure(0, weight=10)
        self.frame_E1Form.grid_rowconfigure(1, weight=24)
        self.frame_E1Form.grid_rowconfigure(2, weight=22)
        self.frame_E1Form.grid_rowconfigure(3, weight=22)
        self.frame_E1Form.grid_rowconfigure(4, weight=22)
        
        self.frame_E1Table.grid_columnconfigure(0, weight=50)
        self.frame_E1Table.grid_columnconfigure(1, weight=50)
        self.frame_E1Table.grid_rowconfigure(0, weight=10)
        self.frame_E1Table.grid_rowconfigure(1, weight=50)
        self.frame_E1Table.grid_rowconfigure(2, weight=40)
        
        
        
        #################################################
        #################### METODOS ####################
        #################################################    

    #DESPLAZAMIENTOS ENTRE FRAMES#
    def mostrarFrameB(self):
        # Ocultar los frame
        self.frame_C.grid_remove()
        self.frame_D.grid_remove()
        self.frame_E.grid_remove()
        # Mostrar el frame 
        self.frame_B.grid()
       

    def mostrarFrameC(self):
        # Ocultar los frame
        self.frame_B.grid_remove()
        self.frame_D.grid_remove()
        self.frame_E.grid_remove()
        # Mostrar el frame 
        self.frame_C.grid()
        self.listarSospechoso()
        
    def mostrarFrameD(self):
        # Ocultar los frame 
        self.frame_B.grid_remove()
        self.frame_C.grid_remove()
        self.frame_E.grid_remove()
        
        # Mostrar el frame 
        self.frame_D.grid()
        self.listarMiembros()
        
    def mostrarFrameE(self):
        # Ocultar los frame
        self.frame_B.grid_remove()
        self.frame_C.grid_remove()
        self.frame_D.grid_remove()
        
        self.NombresSos= self.BOSospechoso.listarNombresSosLOG()
        if(len(self.NombresSos) == 0):
            messagebox.showinfo("Error", "Error al Obtener los nombres de los sospechosos, procure crear un perfil de sospechoso primero")
            self.frame_B.grid()
        else:
            self.frame_E.grid()
            self.cbSospechosos ['values']=self.NombresSos
        
 
    
    def salir(self):
        self.quit()
        
    
    #####################################
    ##########DETECCION FACIAL###########
    #####################################
        
    def deteccion_Facial(self,frame):
        gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces= self.faceClassif.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            frame=cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            
        return frame
    
    #btn iniciar video y end
    def video_de_entrada(self):
        self.btnEnd.configure(state="active")
        self.BtnIniciarVideo.configure(state="disabled")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.entrenarSistema()
        self.visualizar()

    def visualizar(self):
        if not self.captura_pausada:
            self.face_recognizer.read('ModeloFacesFrontalData2023.xml')
            ret, frame = self.cap.read()

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = gray.copy()
                faces = self.faceClassif.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    rostro = auxFrame[y:y + h, x:x + w]
                    rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                    result = self.face_recognizer.predict(rostro)
                    cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

                    if result[1] < 80:
                        nombre = self.etiqueta_sospechoso_mapping.get(result[0], "No encontrado")
                        if nombre != "No encontrado":
                            name = nombre
                        else:
                            name = "Nombre no encontrado"  # O alguna otra acción adecuada

                        cv2.putText(frame, name, (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        self.procesar_nombre(name)
                        
                    else:
                        cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.lblVideo.configure(image=img)
                self.lblVideo.image = img
                self.lblVideo.after(10, self.visualizar)
            else:
                self.finalizar_video()

    def finalizar_video(self):
        self.lblVideo.image = None
        self.BtnIniciarVideo.configure(state="active")
        self.btnEnd.configure(state="disabled")
        self.cap.release()

    def detener_captura_video(self):
        self.captura_pausada = True

    def reiniciar_captura_video(self):
        
        self.captura_pausada = False
        self.tiempo_inicio_nombre = None
        self.nombre_detectado_actual = None
        self.nombre_guardado = None
        print("reiniciando...")
        self.face_recognizer.read('ModeloFacesFrontalData2023.xml')
            
        
        
    def procesar_nombre(self, nombre_detectado):
            if self.nombre_detectado_actual == nombre_detectado:
                # Si el nombre es el mismo que el detectado previamente, incrementa el temporizador
                tiempo_actual = time.time()
                if self.tiempo_inicio_nombre is None:
                    self.tiempo_inicio_nombre = tiempo_actual
                elif tiempo_actual - self.tiempo_inicio_nombre >= 2:
                    # Si el temporizador ha alcanzado los 2 segundos, guarda el nombre
                    self.nombre_guardado = nombre_detectado
                    # Detén momentáneamente la captura de video
                    self.detener_captura_video()
                    self.mostrar_ventana_emergente(self.nombre_guardado)
                    

            else:
                # Si el nombre es diferente, reinicia el temporizador y almacena el nuevo nombre
                self.tiempo_inicio_nombre = time.time()
                self.nombre_detectado_actual = nombre_detectado
  
      
    #####################################
    ########ENTRENAMIENTO FACIAL#########
    #####################################
    def entrenarSistema(self):
        facesData,self.indicesReconocimiento,self.Diccionario=self.BOEntrenamiento.ObtenerListasSospNom_Cont()
        
        self.etiqueta_sospechoso_mapping = {etiqueta: nombre for nombre, etiqueta in self.Diccionario.items()}

        model = cv2.face.LBPHFaceRecognizer_create()
        message_window = tk.Toplevel(self)
        message_label = tk.Label(message_window, text="Entrenando...")
        message_label.pack()
        model.train(facesData, np.array(self.indicesReconocimiento))
        
        message_window.destroy()

        # Guardar el modelo entrenado en un archivo XML
        model.write("ModeloFacesFrontalData2023.xml")
        
        messagebox.showinfo("Entrenamiento Completado", "El modelo ha sido entrenado y guardado.")
        
    ###################################
    ############# ALERTA ##############
    ###################################
  

    def mostrar_ventana_emergente(self,nombre):
        ventana_emergente = tk.Toplevel(self)  # Crea una nueva ventana emergente
        ventana_emergente.title("DETECCION")  # Establece el título de la ventana

        etiqueta = tk.Label(ventana_emergente, text="Persona detectada:¿ENVIAR MENSAJE DE ALERTA?")
        etiqueta.pack(padx=10, pady=10)
        self.sonido_emergente.play()
        boton = tk.Button(ventana_emergente, text="Enviar mensaje", command= lambda: self.enviar_correo(ventana_emergente, nombre))
        boton.pack(pady=10)
        ventana_emergente.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana_emergente(ventana_emergente))
        
  
    def enviar_correo(self,ventana,nombre):
        destinatarios= self.BOMiembro.mostrarDatosMiemLOG()
        directorio_actual = os.path.dirname(os.path.abspath(__file__)) # SE BUSCA EL DIRECTORIO 
        ruta_credenciales = os.path.join(directorio_actual, "credenciales.json") #ENCUENTRA EL ARCHIVO JSON

        with open(ruta_credenciales, "r") as file: #LE DE EL PERMISO DE LEER AL CODIGO EL JSON
            data = json.load(file)#GUARDA LA DATA EN LA VARIABLE data 

        correo = data["CORREO"] #CORREO DE LA PERSONA QUE ENVIARA EL MENSAJE 
        access = data["SMTP_ACCESS"] #PROTOCOLO SMTP (credenciales)
        password = data["PASSWORD_ACCESS"] #Key de acceso 
        
        for destinatario in destinatarios:
            remitente = correo  
            hora_actual = datetime.now()  #PUEDE OBTENER LA FECHA EXACTA DE LA PC 
            hora_formateada = hora_actual.strftime("%Y-%m-%d %H:%M:%S") #DEFINE COMO SE VA A ENVIAR (AÑO/MES/DIA/HORA)
            mensaje = "EL SOSPECHOSO HA SIDO CAPTADO EN EL LOCAL"+ hora_formateada+"El nombre es: "+nombre #AQUI PUEDES DEFINIR EL MENSAJE 

      
            email = EmailMessage() #AQUI SE DEFINE PARA ENVIAR LA PETICIÓN AL PROTOCOLO 
            email["From"] = remitente
            email["To"] = destinatario.get_correoM()
            email["Subject"] = "Test"
            email.set_content(mensaje)
            #PIDE ACCESO A LOS KOTENS, KEYS, COMO LO QUIERAS LLAMAR. AL FINAL CIERRA EL SMTP 
            smtp = smtplib.SMTP_SSL(access)
            smtp.login(remitente, password)
            smtp.send_message(email)
            smtp.quit()
        self.reiniciar_captura_video()
        self.finalizar_video()
        time.sleep(1)
        
        ventana.destroy()
        self.video_de_entrada()
            
    def cerrar_ventana_emergente(self,ventana):
        # Ejecutar los métodos al cerrar la ventana
        
        self.reiniciar_captura_video()
        self.finalizar_video()
        time.sleep(1)
        ventana.destroy()
        self.video_de_entrada()
    ###################################
    ############ MIEMBROS #############
    ###################################

    
    def validarCorreo(self,Correo):
        esValido=True
        
        
        EMAIL_RE=re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
        esValido=False if not EMAIL_RE.match(Correo)else True
        return esValido
    
    def guardarDatMiem(self):
        nombre=self.tfD1NombreM.get()
        correo=self.tfD1CorreoM.get()
        if(self.validarCorreo(correo)):
            self.miembro.set_nombreM(nombre)
            self.miembro.set_correoM(correo)
            if not self.BOMiembro.guardarDatosMiemLOG(self.miembro):
                messagebox.showinfo("Info", "Se guardaron correctamente los datos")
                self.listarMiembros()
            else:
                messagebox.showinfo("Error", "No se Logro Guardar los Datos")
        else:
            messagebox.showinfo("Error", "Asegurese de seguir el formato email: ejemplo@hotmail.com")
            
    def listarMiembros(self):
        self.TablaD1Tabla.delete(*self.TablaD1Tabla.get_children())
        lista= self.BOMiembro.mostrarDatosMiemLOG()
        for item in lista:
            self.TablaD1Tabla.insert("", "end", values=(item.get_idM(), item.get_nombreM(), item.get_correoM()))
            
    def cargar_datos_seleccionados(self,event):
        # Obtener el índice de la fila seleccionada
        seleccion = self.TablaD1Tabla.selection()
        if seleccion:
            fila = seleccion[0]  # Tomar la primera fila seleccionada (puedes ajustar esto si permite selección múltiple)

            # Obtener los valores de la fila seleccionada
            valores_fila = self.TablaD1Tabla.item(fila, 'values')

            # Colocar los valores en los campos de texto
            self.tfD1ID.configure(state="normal")
            self.tfD1ID.delete(0, 'end')
            self.tfD1ID.insert(0, int(valores_fila[0]))
            self.tfD1ID.configure(state="disabled")
            
            self.tfD1NombreM.delete(0, 'end')
            self.tfD1NombreM.insert(0, valores_fila[1])
            self.tfD1CorreoM.delete(0, 'end')
            self.tfD1CorreoM.insert(0, valores_fila[2])
            
    def eliminarMiem(self):
        self.tfD1ID.configure(state="normal")
        id=self.tfD1ID.get() 
        
        if(not self.BOMiembro.eliminarDatosMiemLOG(id)):
           messagebox.showinfo("Info", "Se elimino correctamente")
           self.listarMiembros()
           
        else:
           messagebox.showinfo("Error", "Fallo al eliminar")
           
           
        self.tfD1ID.configure(state="disabled")
    
    
    def actualizarInfoMiemb(self):
        self.tfD1ID.configure(state="normal")
        
        id=int(self.tfD1ID.get())
        nombre=self.tfD1NombreM.get() 
        correo=self.tfD1CorreoM.get() 
        actualizarDat=Miembro(id,nombre,correo)
    
        if(self.BOMiembro.actualizarDatosMiemLOG(actualizarDat)):
            messagebox.showinfo("Info", "Se Actualizo correctamente")
            self.listarMiembros()
        else:
            messagebox.showinfo("Error", "No se pudo actualizar")
            
        self.tfD1ID.configure(state="disabled")
        

    ###################################
    ############# SOSPECHOSO ##########
    ###################################

    
    def subir_imagen(self):
        imagenes=[]
        nombre=[]
        # Definir las extensiones de archivo permitidas (por ejemplo, .jpg, .jpeg, .png, .gif, etc.)
        filetypes = [('Archivos de imagen', '*.jpg *.jpeg *.png')]

        # Abrir un cuadro de diálogo para seleccionar múltiples imágenes
        file_paths = filedialog.askopenfilenames(filetypes=filetypes)

        if not file_paths:
            print("No se seleccionaron imágenes.")
        else:
            for file_path in file_paths:
                # Leer el contenido de la imagen seleccionada
                
                with open(file_path, 'rb') as file:
                    imagen_data = file.read()
                # Obtén el nombre del archivo sin la ruta completa
                nombre_archivo = os.path.basename(file_path)
                imagenes.append(imagen_data)
                nombre.append(nombre_archivo)
        return imagenes,nombre
    
    def subir_imagenGuarddatos(self):
        self.ListImagenesC.clear()
        self.ListImagenesN.clear()
        
        # Definir las extensiones de archivo permitidas (por ejemplo, .jpg, .jpeg, .png, .gif, etc.)
        filetypes = [('Archivos de imagen', '*.jpg *.jpeg *.png')]

        # Abrir un cuadro de diálogo para seleccionar múltiples imágenes
        file_paths = filedialog.askopenfilenames(filetypes=filetypes)

        if not file_paths:
            print("No se seleccionaron imágenes.")
        else:
            for file_path in file_paths:
                # Leer el contenido de la imagen seleccionada
                image = cv2.imread(file_path)
                with open(file_path, 'rb') as file:
                    imagen_data = file.read()
                    
                # Obtén el nombre del archivo sin la ruta completa
                if image.shape ==(720,720,3):
                    nombre_archivo = os.path.basename(file_path)
                    self.ListImagenesC.append(imagen_data)
                    self.ListImagenesN.append(nombre_archivo)
                else:
                    messagebox.showinfo("Error", "Asegurese de primero recortar las imagenes para poder subirlas")
    
    
    
    
    def recortarRostrosEnImagenes(self):
        
        if self.frame_C.winfo_viewable():
        # Código a ejecutar si el frame C está visible
            personName = self.tfDatoNombreS.get()
        
        elif self.frame_E.winfo_viewable():
        # Código a ejecutar si el frame E está visible
            personName = self.cbSospechosos.get()
        
            
        if personName == "" or personName is None:
            messagebox.showinfo("Error", "Ingrese primero el nombre del sospechoso")
        else:
            dataPath ='D:/ojp/ReconocimientoF_Proyect/ImagenesRecortadas'
            personPath=dataPath + '/'+personName
            ######################################################
            
            #Crear carpeta en Data
            if not os.path.exists(personPath):
                print('Carpeta Creada: ',personPath)
                os.makedirs(personPath)

            # Cargamos el clasificador Haar para la detección de rostros
            faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            imagenes, nombres = self.subir_imagen()
            
            for image_content, image_name in zip(imagenes, nombres):
                # Decodificar el contenido de la imagen
                image_array = np.frombuffer(image_content, np.uint8)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                
                frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                # Convertir la imagen a escala de grises para la detección de rostros
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Realizar la detección de rostros en la imagen
                faces = faceClassif.detectMultiScale(gray, 1.3, 5)

                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        # Recortar la región del rostro
                        rostro = frame[y:y + h, x:x + w]
                        rostro = cv2.resize(rostro, (720, 720), interpolation=cv2.INTER_CUBIC)
                        cv2.imshow('frame', rostro)
                        cv2.waitKey(1000)
                        cv2.imwrite(personPath+'/{}_{}.jpg'.format(personName,timestamp),rostro)
    
                        
                
                
    def GuardarDatosSospechoso(self):
        nombreSOS=self.tfDatoNombreS.get()
        usuario="Alexis"#Se debe jalar el usuario de la base de datos
        lista= self.BOSospechoso.listarNombresSosLOG()
        print(lista)
        if(len(self.ListImagenesC) == 0):
            messagebox.showinfo("Error", "Asegurese de subir al menos una imagen del sospechoso o de que las imagenes contengan el rostro del sospechoso")
        else:
            if nombreSOS == "" :
                 messagebox.showinfo("Error", "Ingrese un nombre para el sospechoso")
            else:
                if nombreSOS in lista:
                    messagebox.showinfo("Error", "Ya existe un sospechoso con ese nombre, si desea agregar imagenes dirijase a la seccion de imagen")
                else:
                    self.sospechoso.set_nombreS(nombreSOS)
                    self.sospechoso.set_nombreUSos(usuario)
                    if(not self.BOSospechoso.guardarDatosSosLOG(self.sospechoso)):
                        idSospechoso=self.BOSospechoso.obtenerIdSos(nombreSOS)
                        print(idSospechoso)
                        for i in range(len(self.ListImagenesC)):
                            contenido=self.ListImagenesC[i]
                            nombreImagen= self.ListImagenesN[i]
                            print(nombreImagen)
                            self.Imagen.set_nombreI(nombreImagen)
                            self.Imagen.set_contenidoI(contenido)
                            self.Imagen.set_idSIma(idSospechoso)
                            self.BOImagen.guardarImagen(self.Imagen)
                        
                        messagebox.showinfo("Info", "Se agrego correctamente el sospechoso")
                        self.ListImagenesC.clear()
                        self.ListImagenesN.clear()
                        self.listarSospechoso()
                        self.entrenarSistema()
                            
                            
                    else:
                        messagebox.showinfo("Error", "No se guardo la informacion del sospechoso")
    def listarSospechoso(self):
        self.TablaC1Tabla.delete(*self.TablaC1Tabla.get_children())
        lista= self.BOSospechoso.listarDatosSosLOG()
        for item in lista:
            self.TablaC1Tabla.insert("", "end", values=(item.get_idS(), item.get_nombreS(), item.get_nombreUSos()))
            
    def cargar_datos_seleccionadosS(self,event):
        # Obtener el índice de la fila seleccionada
        seleccion = self.TablaC1Tabla.selection()
        if seleccion:
            fila = seleccion[0]  # Tomar la primera fila seleccionada (puedes ajustar esto si permite selección múltiple)

            # Obtener los valores de la fila seleccionada
            valores_fila = self.TablaC1Tabla.item(fila, 'values')

            # Colocar los valores en los campos de texto
            self.tfC1ID.configure(state="normal")
            self.tfC1ID.delete(0, 'end')
            self.tfC1ID.insert(0, int(valores_fila[0]))
            self.tfC1ID.configure(state="disabled")
            
            self.tfDatoNombreS.delete(0, 'end')
            self.tfDatoNombreS.insert(0, valores_fila[1])
            self.tfD1CorreoM.delete(0, 'end')
            self.tfD1CorreoM.insert(0, valores_fila[2])
            
    def eliminarSos(self):
        self.tfC1ID.configure(state="normal")
        id=self.tfC1ID.get() 
        if(id==''):
            messagebox.showinfo("Error", "Asegurese que selecciono un sospechoso")
        else:
            if(not self.BOSospechoso.eliminarDatosSosLOG(id)):
                messagebox.showinfo("Datos Eliminados", "Se a Eliminado correctamente los datos del Sospechoso")
            
            else:
                messagebox.showinfo("Error", "Fallo en eliminar")
            self.listarSospechoso()
           
        self.tfD1ID.configure(state="disabled")
    def ActualizarDatos(self):
        self.tfC1ID.configure(state="normal")
        
        id=int(self.tfC1ID.get())
        nombre=self.tfDatoNombreS.get() 
        Usuario="Alexis" #Debe ser cambiado a la obtencion desde BD
        actualizarDat=Sospechoso(id,nombre,Usuario)
        if(id==''):
            messagebox.showinfo("Error", "Asegurese que selecciono un sospechoso")
        else:
            if(self.BOSospechoso.actualizarDatosSosLOG(actualizarDat)):
                messagebox.showinfo("Datos Actualizados", "Se a Actualizado correctamente los datos del Sospechoso")
                self.listarSospechoso()
           
            else:
                messagebox.showinfo("Error", "No se a Actualizado correctamente los datos del Sospechoso")
                self.listarSospechoso()
            
            self.tfC1ID.configure(state="disabled")
    

    ###################################
    ############## IMAGEN #############
    ###################################

    def ListarImagenes(self,event):
        self.TablaE1Tabla.delete(*self.TablaE1Tabla.get_children())
        nombreSOS=self.cbSospechosos.get()
        print(nombreSOS)
        idSospechoso=self.BOSospechoso.obtenerIdSos(nombreSOS)
        print(idSospechoso)
        if idSospechoso is None or not idSospechoso:
            messagebox.showinfo("Error", "Asegurese que selecciono un sospechoso") 
        else:
            lista= self.BOImagen.listarImagenxId(idSospechoso)
            for item in lista:
                self.TablaE1Tabla.insert("", "end", values=(item.get_idI(), item.get_nombreI(), item.get_idSIma()))
                
    def ListarImagenxID(self,nombreS):
        self.TablaE1Tabla.delete(*self.TablaE1Tabla.get_children())
        print(nombreS)
        idSospechoso=self.BOSospechoso.obtenerIdSos(nombreS)
        print(idSospechoso)
        if idSospechoso is None or not idSospechoso:
            messagebox.showinfo("Error", "Asegurese que selecciono un sospechoso") 
        else:
            lista= self.BOImagen.listarImagenxId(idSospechoso)
            for item in lista:
                self.TablaE1Tabla.insert("", "end", values=(item.get_idI(), item.get_nombreI(), item.get_idSIma()))
    
    def cargarDatosSeleccionadosImagen(self,event):
        # Obtener el índice de la fila seleccionada
        seleccion = self.TablaE1Tabla.selection()
        if seleccion:
            fila = seleccion[0]  # Tomar la primera fila seleccionada (puedes ajustar esto si permite selección múltiple)

            # Obtener los valores de la fila seleccionada
            valores_fila = self.TablaE1Tabla.item(fila, 'values')

            # Colocar los valores en los campos de texto
            self.tfE1ID.configure(state="normal")
            self.tfE1ID.delete(0, 'end')
            self.tfE1ID.insert(0, int(valores_fila[0]))
            self.tfE1ID.configure(state="disabled")
            
            self.tfE1nombreI.configure(state="normal")
            self.tfE1nombreI.delete(0, 'end')
            self.tfE1nombreI.insert(0, valores_fila[1])
            self.tfE1nombreI.configure(state="disabled")
            
            imagenSeleccionada=self.BOImagen.MostrarImagenPorIDimagen(int(valores_fila[0]))
            cv2.imshow("Imagen desde la base de datos", imagenSeleccionada)
            # Esperar hasta que se presione una tecla y luego cerrar la ventana
            cv2.waitKey(0)
            
    def limpiarCasillas(self):
        self.tfE1ID.configure(state="normal")
        self.tfE1nombreI.configure(state="normal")
        self.tfE1ID.delete(0, 'end')
        self.tfE1nombreI.delete(0, 'end')
        self.tfE1ID.configure(state="disabled")
        self.tfE1nombreI.configure(state="disabled")
        
    def agregarImagenes(self):
        nombreSOS=self.cbSospechosos.get()
        print(nombreSOS)
        idSospechoso=self.BOSospechoso.obtenerIdSos(nombreSOS)
        print(idSospechoso)
        if idSospechoso is None or not idSospechoso:
            messagebox.showinfo("Error", "Asegurese que selecciono un sospechoso") 
        else:
            self.ListImagenesC.clear()
            self.ListImagenesN.clear()
            # Definir las extensiones de archivo permitidas (por ejemplo, .jpg, .jpeg, .png)
            filetypes = [('Archivos de imagen', '*.jpg *.jpeg *.png')]

            # Abrir un cuadro de diálogo para seleccionar múltiples imágenes
            file_paths = filedialog.askopenfilenames(filetypes=filetypes)

            if not file_paths:
                print("No se seleccionaron imágenes.")
            else:
                for file_path in file_paths:
                    image = cv2.imread(file_path)
                    # Leer el contenido de la imagen seleccionada
                    with open(file_path, 'rb') as file:
                        imagen_data = file.read()
                    # Obtén el nombre del archivo sin la ruta completa
                    if image.shape ==(720,720,3):
                        nombre_archivo = os.path.basename(file_path)
                        self.ListImagenesC.append(imagen_data)
                        self.ListImagenesN.append(nombre_archivo)
                    else:
                        messagebox.showinfo("Error", "Asegurese de primero recortar las imagenes para poder subirlas")
            if(len(self.ListImagenesC) == 0):
                messagebox.showinfo("Error", "Asegurese de subir al menos una imagen del sospechoso")
            else:
                for i in range(len(self.ListImagenesC)):
                    contenido=self.ListImagenesC[i]
                    nombreImagen= self.ListImagenesN[i]
                    self.Imagen.set_nombreI(nombreImagen)
                    self.Imagen.set_contenidoI(contenido)
                    self.Imagen.set_idSIma(idSospechoso)
                    self.BOImagen.guardarImagen(self.Imagen)
                messagebox.showinfo("Info", "Se agregaron las imagenes correctamente")
                self.ListarImagenxID(nombreSOS)
                self.entrenarSistema()
                self.ListImagenesC.clear()
                self.ListImagenesN.clear()
            
    def eliminarImagenPorID(self):
        self.tfE1ID.configure(state="normal") 
        nombreSOS=self.cbSospechosos.get() 
        id=self.tfE1ID.get() 
        if(id==''):
            messagebox.showinfo("Error", "Asegurese que selecciono una Imagen")
        else:
            if(not self.BOImagen.eliminarImagenID(id)):
                messagebox.showinfo("Datos Eliminados", "Se a Eliminado correctamente la imagen")
            else:
                messagebox.showinfo("Error", "Fallo en eliminar")
            self.ListarImagenxID(nombreSOS)
           
        self.tfE1ID.configure(state="disabled")
        
        
                 
                
                
          
app = App()
app.mainloop()
