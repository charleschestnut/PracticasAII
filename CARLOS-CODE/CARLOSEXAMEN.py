from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, NUMERIC
from whoosh.qparser import QueryParser
import urllib.request

from bs4 import BeautifulSoup
import urllib.request
import ssl

def extraer_web():
    f = urllib.request.urlopen("https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades",
                            context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    s = BeautifulSoup(f,"html.parser")
    return s

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


if __name__ == '__main__':
    extraer_datos()