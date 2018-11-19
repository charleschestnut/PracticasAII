'''
Created on 7 nov. 2018

@author: cami_
'''
from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, NUMERIC
from whoosh.qparser import QueryParser
import urllib.request
from bs4 import BeautifulSoup
import datetime

dirindextemas = "IndexTemas"
dirindexrespuestas = "IndexRespuestas"


# Crea un indice desde los documentos contenidos en dirdocs
# El indice lo crea en un directorio (dirindex)
def index():
    if not os.path.exists(dirindextemas):
        os.mkdir(dirindextemas)

    ix = create_in(dirindextemas, schema=get_schema_tema())
    writer = ix.writer()

    if not os.path.exists(dirindexrespuestas):
        os.mkdir(dirindexrespuestas)

    ix2 = create_in(dirindexrespuestas, schema=get_schema_respuesta())
    writer2 = ix2.writer()

    # Extraemos los datos usando BeautifulSoup
    url = urllib.request.urlopen("https://foros.derecho.com/foro/20-Derecho-Civil-General")
    soup = BeautifulSoup(url, 'html.parser')
    url.close()

    items = soup.findAll(class_="threadinfo")

    i = 0
    x = 0
    for index, item in enumerate(items):
        if index != 0:
            titulo = item.findAll(class_="title")[0].text
            enlace = "https://foros.derecho.com/" + item.findAll(class_="title", href=True)[0]['href'].split("?")[0]
            autor = item.findAll(class_="username understate")[0].text
            fecha = item.find(class_="author").span.text.split(",")[1].strip()
            fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y %H:%M")
            numRespuestas = soup.findAll(class_="threadstats td alt")[index - 1].li.a.text
            numVisitas = \
                soup.findAll(class_="threadstats td alt")[index - 1].li.find_next_sibling("li").text.split(":")[
                    1].strip().replace(",", "")
            writer.add_document(titulo=titulo, link=enlace, autor=autor, fecha=fecha, numRespuestas=numRespuestas,
                                numVisitas=numVisitas)
            i += 1

            # Guardamos las respuestas
            urlResCopia = enlace
            urlRes = urllib.request.urlopen(enlace.encode('ascii', 'ignore').decode('ascii'))
            soupRes = BeautifulSoup(urlRes, 'html.parser')
            urlRes.close()

            items2 = soupRes.findAll(class_="postcontainer")
            for b, item2 in enumerate(items2):
                itemX = item2.find(class_="postcontent")
                user = item2.find(class_="username")
                date = item2.find(class_="date")
                response = itemX.text
                user = user.text
                date = datetime.datetime.strptime(date.text.replace(",", ""), "%d/%m/%Y %H:%M")
                writer2.add_document(link=urlResCopia, fecha=date, texto=response, autor=user)
                x += 1

    messagebox.showinfo("Temas indexados", "Se han indexado " + str(i) + " temas")
    messagebox.showinfo("Respuestas indexadass", "Se han indexado " + str(x) + " respuestas")
    writer2.commit()
    writer.commit()


def get_schema_tema():
    return Schema(titulo=TEXT(stored=True), link=TEXT(stored=True), autor=TEXT(stored=True),
                  fecha=DATETIME(stored=True), numRespuestas=NUMERIC(stored=True), numVisitas=NUMERIC(stored=True))


def get_schema_respuesta():
    return Schema(link=TEXT(stored=True), fecha=DATETIME(stored=True), texto=TEXT(stored=True), autor=TEXT(stored=True))


def searchByTitle():
    def mostrar_lista(event):
        lb.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindextemas)
        with ix.searcher() as searcher:
            query = QueryParser("titulo", ix.schema).parse("%" + str(en.get()) + "%")
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['titulo'])
                lb.insert(END, r['autor'])
                lb.insert(END, r['fecha'])
                lb.insert(END, '')

    v = Toplevel()
    v.title("Búsqueda por títulos")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una palabra:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)


def searchByAuthor():
    def mostrar_lista(event):
        lb.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindextemas)
        with ix.searcher() as searcher:
            query = QueryParser("autor", ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['titulo'])
                lb.insert(END, r['autor'])
                lb.insert(END, r['fecha'])
                lb.insert(END, '')

    v = Toplevel()
    v.title("Búsqueda por autor")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca un autor:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)


def searchByText():
    def mostrar_lista(event):
        lb.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindexrespuestas)
        ix2 = open_dir(dirindextemas)
        with ix.searcher() as searcher:
            query = QueryParser("texto", ix.schema).parse("%" + en.get() + "%")
            results = searcher.search(query)
            for r in results:
                with ix2.searcher() as searcher2:
                    query = QueryParser("link", ix.schema).parse(r['link'])
                    results2 = searcher2.search(query)
                    for r2 in results2:
                        lb.insert(END, r2['titulo'])
                        lb.insert(END, r2['autor'])
                        lb.insert(END, r2['fecha'])
                        lb.insert(END, '')

    v = Toplevel()
    v.title("Búsqueda por respuestas")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una palabra:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)


if __name__ == '__main__':
    root = Tk()

    root.geometry("270x100+50+50")

    menubar = Menu(root)

    helpmenu = Menu(menubar)
    menuinicio = Menu(menubar)
    nested_menu1 = Menu(helpmenu)
    nested_menu1.add_command(label='Título', command=searchByTitle)
    nested_menu1.add_command(label='Autor', command=searchByAuthor)
    menuinicio.add_command(label='Indexar', command=index)
    menuinicio.add_command(label='Salir', command=root.quit)
    nested_menu2 = Menu(helpmenu)
    nested_menu2.add_command(label='Texto', command=searchByText)

    menu2_nested = Menu(nested_menu2)

    helpmenu.add_cascade(label='Temas', menu=nested_menu1)
    helpmenu.add_cascade(label='Respuestas', menu=nested_menu2)

    menubar.add_cascade(label="Inicio", menu=menuinicio)
    menubar.add_cascade(label="Buscar", menu=helpmenu)

    root.config(menu=menubar)
    root.mainloop()