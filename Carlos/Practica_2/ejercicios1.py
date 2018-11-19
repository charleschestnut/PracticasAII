#-*- coding: utf-8 -*-



# La base de datos debe almacenar la siguiente informaci�n de cada pel�cula: t�tulo, a�o de
#estreno, director y g�neros (terror, comedia, ciencia-ficci�n, drama, aventuras, comedia,
#etc�). Puede tener m�s de un g�nero. 
from sqlite3 import *
from tkinter import *

def almacenar_bd():
    conn = connect('test.db')
    conn.text_factory = str 
    conn.execute("DROP TABLE IF EXISTS PELICULAS")
    conn.execute('''CREATE TABLE PELICULAS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        DIRECTOR TEXT NOT NULL);''')
    
    conn.execute("DROP TABLE IF EXISTS TIENE_GENEROS")
    conn.execute('''CREATE TABLE TIENE_GENEROS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        GENEROID INTEGER NOT NULL);''')
    
    conn.execute("DROP TABLE IF EXISTS GENEROS")
    conn.execute('''CREATE TABLE GENEROS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GENERO TEXT NOT NULL);''')
    
    conn.commit()
    


# APARTADO A: Crear una ventana con el men� principal con tres opciones: INICIO, EDITAR Y BUSCAR
def ventana_principal_1():
    top = Tk()
    inicio = Button(top, text="Inicio")
    inicio.pack(side = LEFT)
    editar = Button(top, text="Editar")
    editar.pack(side= LEFT)
    buscar = Button(top, text="Buscar")
    buscar.pack(side= LEFT)


#APARTADO B: La opci�n Inicio despliega un men� con dos comandos:

# 1. Listar.- Abre un ventana con una cuadro de lista que muestre todas las pel�culas (T�tulo y a�o de estreno) ordenadas por a�o. 

# 2. Salir.- Que sale de la aplicaci�n.

def ventana_principal_2():
    top = Tk()
    menu1 = Menu(top)
    inicioMenu =Menu(menu1, tearoff = 0)
    inicioMenu.add_command(label="Listar", command = listar_bd())
    inicioMenu.add_command(label="Salir", command = salir_menu())
    
    menu1.add_cascade(label = "Inicio", menu = inicioMenu)
    inicioMenu.pack(side = LEFT)
    
    editar = Button(top, text="Editar")
    editar.pack(side= LEFT)
    buscar = Button(top, text="Buscar")
    buscar.pack(side= LEFT)

    
def listar_bd():
    conn = connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, FECHA FROM PELICULAS")
    conn.close()

def salir_menu():
    
 


#APARTADO C: La opci�n Editar despliega un men� con tres comandos:
# 1. Nueva.- Abre una ventana para dar de alta una nueva pel�cula.
# 2. Modificar.- Abre una ventana que nos permite buscar una pel�cula por su t�tulo, mostrarla y modificarla.
# 3. Borrar.- Abre una ventana que nos permite buscar una pel�cula por su t�tulo, mostrarla y borrarla. 



#APARTADO D:  La opci�n Buscar abre una ventana con un grupo con dos botones de opci�n, los cuales
#nos permite seleccionar el criterio: a�o o g�nero. Y nos muestra un cuadro de lista con
#los datos de las pel�culas de dicho a�o o g�nero. 
