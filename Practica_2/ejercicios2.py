#-*- coding: utf-8 -*-

#Escribir un programa que me cree tres ventanas: ALMACENAR, LISTAR, BUSCAR
#ALMACENAR: se almacenará en una base de datos los nombres, links y fecha de todas
#las noticias de http://www.us.es/rss/feed/portada y muestre en una ventana el mensaje "BD creada correctamente"
from builtins import str
from sqlite3 import *
from tkinter import *, Toplevel

def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar", command = almacenar_bd)
    almacenar.pack(side = LEFT)
    listar = Button(top, text="Listar", command = listar_bd)
    listar.pack(side= LEFT)
    buscar = Button(top, text="Buscar", command = buscar_bd)
    buscar.pack(side= LEFT)
    

def almacenar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str 
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")
    conn.execute('''CREATE TABLE NOTICIAS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        lINK TEXT NOT NULL,
        FECHA TEXT NOT NULL);''')
    l = parse("file.txt")
    for i in l:
        conn.execute("""INSERT INTO NOTICIAS (TITULO, LINK, FECHA) VALUES (?,?,?)""")
        conn.commit()
        cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
        message.
        


def extraer_datos():
    fichero = "noticias"
    

    
def listar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, LINK, FECHA FROM NOTICIAS")
    imprimir_pelicula(cursor)
    conn.close()


def imprimir_noticia(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill = Y)
    lb = Listbox(v, width =150, yscrollcommand = sc.set)
    for row in cursor:
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, '')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command= lb.yview)


def buscar_bd():
    def listar_busqueda(event):
    