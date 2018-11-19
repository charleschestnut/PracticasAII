'''
Created on 19.11.2018

@author: Lisa
'''
'''
Created on 19.11.2018

@author: Lisa
'''
from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, NUMERIC
from whoosh.qparser import QueryParser
import urllib.request
from bs4 import BeautifulSoup
import datetime
from _datetime import date


dirindextemas="Index"
#return Schema
def get_schema():
    return Schema(titulo=TEXT(stored=True), description = TEXT (stored=True), categoria=TEXT(stored=True), fecha=DATETIME(stored=True))
   

def extractXML():
    return None

#Crea un indice desde los documentos contenidos en dirdocs
#El indice lo crea en un directorio (dirindex) 
def index():
    if not os.path.exists(dirindextemas):
        os.mkdir(dirindextemas)

    ix = create_in(dirindextemas, schema=get_schema())
    writer = ix.writer()
    
    # Extraemos los datos usando BeautifulSoup
    #Missing
    l = extractXML()

    i=0
    #Todo: Extract the attributes
    #for item in l:      
        #writer.add_document(titulo = titulo, antetitulo = antetitulo, link = link, description= description, fecha = fecha)
        #i+=1
   

    writer.add_document(titulo = "test", description = "test", categoria = "test cag",  fecha = datetime.datetime.now())        
    messagebox.showinfo("Temas indexados", "Se han indexado "+str(i)+ " temas")

    writer.commit()

def searchByDate():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindextemas)      
        with ix.searcher() as searcher:
            #Change names of attribute in which you will search
            query = QueryParser("fecha", ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['titulo'])
                lb.insert(END,r['fecha'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Búsqueda por autor")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca un autor:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)
     
def searchByTitle():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindextemas)      
        with ix.searcher() as searcher:
            query = QueryParser("titulo", ix.schema).parse("%"+str(en.get())+"%")
            results = searcher.search(query)
            for r in results:
                #Change names of attributes 
                lb.insert(END,r['titulo'])
                lb.insert(END,r['categoria'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Búsqueda por títulos")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una palabra:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview) 
  
    
def searchByCategory():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindextemas)      
        with ix.searcher() as searcher:
            query = QueryParser("categoria", ix.schema).parse("%"+str(w.get())+"%")
            results = searcher.search(query)
            for r in results:
                #Change names of attributes 
                lb.insert(END,r['titulo'])
                lb.insert(END,r['fecha'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Búsqueda por títulos")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una palabra:")
    l.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview) 
    
    values=[]
    #Todo fill Spinbox
    for i in "":
        values.append(i)
    w = Spinbox(v, values=(values))

    button = Button(v, text="Search!", command=mostrar_lista)
    w.pack(side=LEFT)
    button.pack(side=LEFT)
      

def create():
    root = Tk()
    
    menubar = Menu(root)
    
    firstmenu = Menu(menubar, tearoff=0)
    firstmenu.add_command(label="Cargar", command=index)
    firstmenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="Datos", menu=firstmenu)
    
    seccondmenu = Menu(menubar, tearoff=0)
    seccondmenu.add_command(label="Titulo y Descripcion", command=searchByTitle)
    seccondmenu.add_command(label="Fecha", command= searchByDate)
    seccondmenu.add_command(label="Categoria", command=searchByCategory)
    menubar.add_cascade(label="Buscar", menu=seccondmenu)
    
    root.config(menu=menubar)
    root.mainloop()
    
if __name__ == '__main__':
    create()