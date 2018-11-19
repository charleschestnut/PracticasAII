# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from sqlite3 import *
from tkinter import *
import urllib.request
import re
import os
from Practica_2.resuelto1 import imprimir_etiqueta




#####################################################################################################
#### PRIMERA PARTE #####
#####################################################################################################

def extraer_datos(arbol):
    # Filtramos para tener directamente la lista de TEMAS
    noticias = arbol.find("div", id="newswrap")
    titulos = []
    enlaces = []
    autores = []
    #fechas_horas = []
    contenidos = []
         
        
    for noticia in noticias.find_all("div", class_="center-content"):
    
        titulo = noticia.find("h2").find('a').string.strip()
        titulos.append(titulo)
        #print(titulo)
        
        enlace = noticia.find("h2").find('a')['href']    # Como es un enlace externo, no debemos ponerle nada más.
        enlaces.append(enlace)
        #print(enlace)
        
        autor_div = noticia.find('div', class_='news-submitted')
        autor_as = autor_div.find_all('a')
        autor = autor_as[1].text
        autores.append(autor)
        #print(autor)
        
        #fecha_hora = noticia.find("span", class_="ts visible")
        #fechas_horas.append(fecha_hora.text)
        #print(fecha_hora)"""
        
        contenido = noticia.find("div", class_="news-content")
        contenidos.append(contenido.text)
        #print(contenido.text)
        
        print(autores)
        print(contenidos)

       
    return titulos, enlaces, autores, contenidos

# CARGAMOS LOS ARCHIVOS DE LA WEB EN LA BASE DE DATOS.
# CARGAMOS LOS ARCHIVOS DE LA WEB EN LA BASE DE DATOS.
def cargar_bd(arbol):
    conn = connect('test.db')
    conn.text_factory = str 
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")
    conn.execute('''CREATE TABLE NOTICIAS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        ENLACE TEXT NOT NULL,
        AUTOR TEXT NOT NULL,
        CONTENIDO TEXT NOT NULL);''')
    
    titulos, enlaces, autores, contenidos = extraer_datos(arbol)
    contador = 0
   
    for i in titulos: 
        conn.execute("""INSERT INTO NOTICIAS (TITULO, ENLACE, AUTOR, CONTENIDO) VALUES (?,?,?,?)""", (titulos[contador], enlaces[contador], autores[contador], contenidos[contador]))
        contador = contador + 1
        
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \n Hay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    

def listar_bd():
    conn = connect('test.db')
    conn.text_factory = str 
    cursor = conn.execute("SELECT TITULO, ENLACE, AUTOR, CONTENIDO FROM NOTICIAS")
    imprimir_etiqueta(cursor)

def salir_():
    exit()


def modificar_autor(autor:str):
    real_autor = autor[6:]    # El autor viene en forma de enlace /user/nombreAutor
    return real_autor




def convertirWebEnArbol (d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, 'html.parser')
    return documento


#####################################################################################################
#### SEGUNDA PARTE #####
#####################################################################################################


def buscar_bd(tipo:str):

    def listar_busqueda(tipo:str):
        conn = connect('test.db')
        conn.text_factory = str
        s = "%" + en.get() + "%"
        print(s)
        if tipo == "titulo":
            cursor = conn.execute("""SELECT TITULO, AUTOR, ENLACE FROM NOTICIAS WHERE TITULO LIKE ?""", (s,))
            
        else:
            cursor = conn.execute("""SELECT TITULO, AUTOR, FECHA FROM NOTICIAS WHERE FECHA >= ?""", (s,))
        
        imprimir_etiqueta(cursor)
        conn.close()
    
    if tipo == "titulo":
        texto = "Introduzca un tema: "
            
    elif tipo == "autor":
        texto = "Introduzca un autor: "
    else:
        texto = "Introduzca una fecha (dd/mm/yyyy): "
    
    v = Toplevel()
    lb = Label(v, text=texto)
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", lambda event:listar_busqueda(tipo))
    en.pack(side=LEFT)
    
    
   

def buscar_autores():
    def list():
        noticias = conn.execute('''SELECT TITULO, AUTOR, ENLACE FROM NOTICIAS WHERE AUTOR LIKE ?''', (w.get(),))
        imprimir_etiqueta(noticias)
    
    conn = connect('test.db')
    conn.text_factory = str
    
    autores = conn.execute("SELECT AUTOR FROM NOTICIAS")
    v = Toplevel()
    label = Label(v, text="Busca para el autor: ")
    values=[]
    for i in autores:
        values.append(i)
    
    w = Spinbox(v, values=(values))
    
    button = Button(v, text="¡Busca!", command=list)
    label.grid(row=0, column= 0)
    w.grid(row=0, column = 1)
    button.grid(row=1, column=1)










def ventana_principal():
    top = Tk()
    # DATOS: CON TRES OPCIONES: CARGAR, MOSTRAR, SALIR.
    cargar = Button(top, text="Cargar", command=lambda:cargar_bd(web))
    cargar.pack(side=LEFT)
    
    listar = Button(top, text="Listar", command=listar_bd)
    listar.pack(side=LEFT)
    
    salir = Button(top, text="Salir", command=salir_)
    salir.pack(side=LEFT)
    
    buscar_tema = Button(top, text="Noticia", command=lambda:buscar_bd("titulo"))
    buscar_tema.pack(side=LEFT)
    
    buscar_autor = Button(top, text="Autor", command=buscar_autores)
    buscar_autor.pack(side=LEFT)
    
    buscar_fecha = Button(top, text="Fecha", command=lambda:buscar_bd("fecha"))
    buscar_fecha.pack(side=LEFT)
    
    top.mainloop()

web = convertirWebEnArbol("https://www.meneame.net/")

ventana_principal()
