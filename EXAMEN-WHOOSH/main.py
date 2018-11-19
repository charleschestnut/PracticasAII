from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in, open_dir
from whoosh import fields
from whoosh.qparser import QueryParser, MultifieldParser
import datetime
from bs4 import BeautifulSoup
import urllib.request
import ssl
from datetime import datetime
from whoosh.qparser.dateparse import DateParserPlugin


dirindextemas = "Index"


# return Schema
def get_schema():
    return fields.Schema(titulo=fields.TEXT(stored=True), start=fields.DATETIME(stored=True), end=fields.DATETIME(stored=True),
                  descripcion=fields.TEXT(stored=True), categoria=fields.TEXT(stored=True))


def extraer_web():
    f = urllib.request.urlopen("https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades",
                            context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    s = BeautifulSoup(f,"html.parser")
    return s


#PASO: TITULO, FECHAINICIO, FECHAFIN, DESCRIPCIÓN, CATEGORÍA
def extraer_datos():

    arbol = extraer_web()

    eventos = arbol.find("div", id="content-core")

    eventos = arbol.findAll("div", class_="cal_info clearfix")

    atributos = []
    for evento in eventos:
        array = []
        titulo = evento.find("span", class_="summary")
        titulo = titulo.text
        array.append(titulo)

        fechaInicio = evento.find("abbr", class_="dtstart")
        if fechaInicio is None:
            array.append("")
        else:
            array.append(fechaInicio.get('title'))

        fechaFin = evento.find("abbr", class_="dtend")
        if fechaFin is None:
            array.append("")
        else:
            array.append(fechaFin.get('title'))

        description = evento.find("p", class_="description")
        if description is None:
            array.append("")
        else:
            array.append(description.text)

        categoria = evento.find("li", class_="category")
        categoria = categoria.find("span")
        categoria = categoria.text
        array.append(categoria)

        atributos.append(array)

    print(atributos)
    return atributos


# Crea un indice desde los documentos contenidos en dirdocs
# El indice lo crea en un directorio (dirindex)
def index():
    if not os.path.exists(dirindextemas):
        os.mkdir(dirindextemas)

    ix = create_in(dirindextemas, schema=get_schema())
    writer = ix.writer()

    # Extraemos los datos usando BeautifulSoup
    l = extraer_datos()


    i = 0
    for item in l:
        writer.add_document(titulo = item[0], start = to_date_start(item[1]), end = to_date_end(item[2]), descripcion= item[3], categoria = item[4])
        i+=1

    messagebox.showinfo("Temas indexados", "Se han indexado " + str(i) + " eventos")

    writer.commit()


def to_date_start(texto):
    if (texto == ""):
        return datetime.fromtimestamp(1284286794)
    return datetime.strptime(texto[:10], "%Y-%m-%d")

def to_date_end(texto):
    if (texto == ""):
        return datetime.today()
    return datetime.strptime(texto[:10], "%Y-%m-%d")

def searchByDate():
    def mostrar_lista(event):
        lb.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindextemas)
        with ix.searcher() as searcher:
            # Change names of attribute in which you will search
            fecha = str(en.get())
            parser = MultifieldParser(["start", "end"], ix.schema)
            parser.add_plugin(DateParserPlugin(free=True))
            query = parser.parse(u"start: before " + fecha + " AND end: after " + fecha)
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['titulo'])
                lb.insert(END, str(r['start']))
                lb.insert(END, str(r['end']))
                lb.insert(END, '')

    v = Toplevel()
    v.title("Búsqueda por autor")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una fecha:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)


def searchByTitle():
    def mostrar_lista(event):
        lb.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindextemas)
        with ix.searcher() as searcher:
            query = MultifieldParser(["titulo", "descripcion"], ix.schema).parse("%" + str(en.get()) + "%")
            results = searcher.search(query)
            for r in results:
                # Change names of attributes
                lb.insert(END, r['titulo'])
                lb.insert(END, str(r['start']))
                lb.insert(END, str(r['end']))
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


def searchByCategory():
    def mostrar_lista():
        lb.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindextemas)
        with ix.searcher() as searcher:
            query = QueryParser("categoria", ix.schema).parse("%" + str(w.get()) + "%")
            results = searcher.search(query)
            for r in results:
                # Change names of attributes
                lb.insert(END, r['titulo'])
                lb.insert(END, str(r['start']))
                lb.insert(END, str(r['end']))
                lb.insert(END, '')

    v = Toplevel()
    v.title("Búsqueda por categoria")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una palabra:")
    l.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)

    values = []
    ix = open_dir(dirindextemas)
    with ix.searcher() as searcher:
        cat = list(searcher.lexicon("categoria"))
        if not (cat in values):
            values = values + cat
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
    seccondmenu.add_command(label="Fecha", command=searchByDate)
    seccondmenu.add_command(label="Categoria", command=searchByCategory)
    menubar.add_cascade(label="Buscar", menu=seccondmenu)

    root.config(menu=menubar)
    root.mainloop()


if __name__ == '__main__':
    create()