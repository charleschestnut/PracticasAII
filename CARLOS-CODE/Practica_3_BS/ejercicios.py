# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import os
import re
from django.core.files.base import File
from sqlite3 import *
from tkinter import *
from builtins import str
from Practica_2.resuelto1 import imprimir_etiqueta
from Practica_1.resuelto1 import buscar_fecha

# TENEMOS QUE CONSTRUIR UN PROGRAMA CON TKINTER CON UN MENÚ CON TRES OPCIONES:
# DATOS: CON TRES OPCIONES: CARGAR, MOSTRAR, SALIR.
# BUSCAR: TEMA, AUTOR, FECHA
# ESTADÍSTICAS: TEMAS MÁS POPULARES, TEMAS MÁS ACTIVOS


def convertirWebEnArbol (d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, 'html.parser')
    return documento


def extraer_datos(arbol):
    # Filtramos para tener directamente la lista de TEMAS
    temas = arbol.find("ol", id="threads")
    titulos = []
    enlaces = []
    autores = []
    fechas_horas = []
    respuestas = []
    visitas = []
    
    for tema in temas.find_all("li", class_="threadbit"):
    
        titulo = tema.find("a", class_="title")
        titulos.append(titulo.text)
        
        enlace = tema.find("a", class_="title")
        enlace = "https://foros.derecho.com/" + enlace.get('href')  # Como no nos dan la raíz, debemos añadírsela nosotros a cada enlace.
        enlaces.append(enlace)
        
        autor = tema.find("a", class_="username understate")
        autores.append(autor.text)
        
        fecha_hora = autor.next_sibling
        fecha_hora = modificar_formato(fecha_hora)
        fechas_horas.append(fecha_hora)
        
        respuesta = tema.find("ul", class_="threadstats")
        respuesta = respuesta.find("a", class_="understate")
        respuesta = int(respuesta.text)
        respuestas.append(respuesta)
        
        visita = tema.find("ul", class_="threadstats")
        visita = tema.find(string=re.compile("Visitas"))
        visita = visita[-1:]
        visita = int(visita)
        visitas.append(visita)
       
    return titulos, enlaces, autores, fechas_horas, respuestas, visitas
    

# CARGAMOS LOS ARCHIVOS DE LA WEB EN LA BASE DE DATOS.
def cargar_bd(arbol):
    conn = connect('test.db')
    conn.text_factory = str 
    conn.execute("DROP TABLE IF EXISTS TEMAS")
    conn.execute('''CREATE TABLE TEMAS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        ENLACE TEXT NOT NULL,
        AUTOR TEXT NOT NULL,
        FECHA TEXT NOT NULL,
        RESPUESTAS INT NOT NULL,
        VISITAS INT NOT NULL);''')
    titulos, enlaces, autores, fechas, respuestas, visitas = extraer_datos(arbol)
    contador = 0
   
    for i in titulos: 
        conn.execute("""INSERT INTO TEMAS (TITULO, ENLACE, AUTOR, FECHA, RESPUESTAS, VISITAS) VALUES (?,?,?,?,?,?)""", (titulos[contador], enlaces[contador], autores[contador], fechas[contador], respuestas[contador], visitas[contador]))
        contador = contador + 1
        
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM TEMAS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


# MODIFICAMOS EL STRING QUE CONTIENE A LA FECHA DE LOS TEMAS.
def modificar_formato(date:str):
    # Me aparece con el formato ,\xa0DD/MM/YYYY\xa0HH:mm
    real_date = date[2:-6] + " " + date[-5:]
    return real_date


# LISTAR LOS TÍTULOS, AUTORES Y FECHAS DE TODOS LOS TEMAS.
def mostrar_bd():
    conn = connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, AUTOR, FECHA FROM TEMAS")
    imprimir_etiqueta(cursor)
    conn.close()
    

def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)
     
        
def salir_ventana():
    exit()


####  SEGUNDA PARTE  ####
def buscar_bd(tipo:str):

    def listar_busqueda(tipo:str):
        conn = connect('test.db')
        conn.text_factory = str
        s = "%" + en.get() + "%"
        print(s)
        if tipo == "titulo":
            cursor = conn.execute("""SELECT TITULO, AUTOR, FECHA FROM TEMAS WHERE TITULO LIKE """, (s,))
            texto = "Introduzca un tema: "
            
        elif tipo == "autor":
            cursor = conn.execute("""SELECT TITULO, AUTOR, FECHA FROM TEMAS WHERE AUTOR LIKE ?""", (s,))
            texto = "Introduzca un autor: "
        else:
            cursor = conn.execute("""SELECT TITULO, AUTOR, FECHA FROM TEMAS WHERE FECHA LIKE ?""", (s,))
            texto = "Introduzca una fecha (dd/mm/yyyy): "
        
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


#### TERCERA PARTE ####
def estadistica(busqueda):
    conn = connect('test.db')
    conn.text_factory = str
    if busqueda == "visitas":
        cursor = conn.execute("""SELECT TITULO, AUTOR, FECHA FROM TEMAS ORDER BY VISITAS ASC LIMIT 5""")
    
    else:
        cursor = conn.execute("""SELECT TITULO, AUTOR, FECHA FROM TEMAS ORDER BY RESPUESTAS ASC LIMIT 5""")
    imprimir_etiqueta(cursor)
    conn.close()   


def ventana_principal():
    top = Tk()
    # DATOS: CON TRES OPCIONES: CARGAR, MOSTRAR, SALIR.
    cargar = Button(top, text="Cargar", command=lambda:cargar_bd(web))
    cargar.pack(side=LEFT)
    
    listar = Button(top, text="Listar", command=mostrar_bd)
    listar.pack(side=LEFT)
    
    salir = Button(top, text="Salir", command=salir_ventana)
    salir.pack(side=LEFT)
    
    # BUSCAR: TEMA, AUTOR, FECHA
    buscar_tema = Button(top, text="Buscar titulo", command=lambda:buscar_bd("titulo"))
    buscar_tema.pack(side=LEFT)
    
    buscar_autor = Button(top, text="Buscar autor", command=lambda:buscar_bd("autor"))
    buscar_autor.pack(side=LEFT)
    
    buscar_fecha = Button(top, text="Buscar fecha", command=lambda:buscar_bd("fecha"))
    buscar_fecha.pack(side=LEFT)
    
    # ESTADÍSTICA VISITAS, ESTADÍSTICA RESPUESTAS
    visitas = Button(top, text="Las más visitadas", command=lambda:estadistica("visitas"))
    visitas.pack(side=LEFT)
    respuestas = Button(top, text="Las más respondidas", command=lambda:estadistica("respuestas"))
    respuestas.pack(side=LEFT)
    top.mainloop()


web = convertirWebEnArbol("https://foros.derecho.com/foro/20-Derecho-Civil-General")

# cargar_bd(web)
# mostrar_bd()

ventana_principal()


