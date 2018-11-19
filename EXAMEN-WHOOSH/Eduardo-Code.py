from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser

dirdocs = "Correos"
dirindex = "Index"


# Crea un indice desde los documentos contenidos en dirdocs
# El indice lo crea en un directorio (dirindex)
def apartado_a():
    if not os.path.exists(dirdocs):
        print("Error: no existe el directorio de documentos " + dirdocs)
    else:
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)

    # STEP 2: https://whoosh.readthedocs.io/en/latest/indexing.html#creating-an-index-object
    ix = create_in(dirindex, schema=get_schema())
    writer = ix.writer()
    i = 0
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs + docname):
            add_doc(writer, dirdocs, docname)
            i += 1
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " correos")

    writer.commit()


def apartado_b():
    def mostrar_lista(event):
        lb.delete(0, END)
        # STEP 4.1: https://whoosh.readthedocs.io/en/latest/searching.html
        # STEP 4.2: https://whoosh.readthedocs.io/en/latest/parsing.html
        ix = open_dir(dirindex)
        with ix.searcher() as searcher:
            parser = QueryParser("remitente", ix.schema)
            query = parser.parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END, r['destinatarios'])
                lb.insert(END, r['asunto'])
                lb.insert(END, '')

    v = Toplevel()
    v.title("Busqueda por rttes")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el correo del rtte:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lb.yview)


# STEP 1: https://whoosh.readthedocs.io/en/latest/schema.html
def get_schema():
    return Schema(remitente=TEXT(stored=True), destinatarios=KEYWORD(stored=True), asunto=TEXT(stored=True),
                  contenido=TEXT(stored=True))


def add_doc(writer, path, docname):
    fileobj = open(path + '\\' + docname, "rb")
    # IMPORTANTE: Convertir el contenido del fichero a Unicode
    rte = str(fileobj.readline().strip())
    dtos = str(fileobj.readline().strip())
    ast = str(fileobj.readline().strip())
    ctdo = str(fileobj.read())
    fileobj.close()

    # STEP 3: https://whoosh.readthedocs.io/en/latest/indexing.html#indexing-documents
    writer.add_document(remitente=rte, destinatarios=dtos, asunto=ast, contenido=ctdo)


def ventana_principal():
    top = Tk()
    indexar = Button(top, text="Indexar", command=apartado_a)
    indexar.pack(side=TOP)
    Buscar = Button(top, text="Buscar por Rtte", command=apartado_b)
    Buscar.pack(side=TOP)
    top.mainloop()


if __name__ == '__main__':
    ventana_principal()