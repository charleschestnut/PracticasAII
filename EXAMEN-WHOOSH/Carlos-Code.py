'''
Created on 5 nov. 2018

@author: Javier Moreno
'''

import urllib.request

from bs4 import BeautifulSoup
import urllib.request
import ssl

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
        titulo = evento.find("span", class_="summary")
        titulo = titulo.text
        atributos.append(titulo)

        fechaInicio = evento.find("abbr", class_="dtstart")
        if fechaInicio is None:
            atributos.append("")
        else:
            atributos.append(fechaInicio.get('title'))

        fechaFin = evento.find("abbr", class_="dtend")
        if fechaFin is None:
            atributos.append("")
        else:
            atributos.append(fechaFin.get('title'))

        description = evento.find("p", class_="description")
        if description is None:
            atributos.append("")
        else:
            atributos.append(description.text)

        categoria = evento.find("li", class_="category")
        categoria = categoria.find("span")
        categoria = categoria.text

    print(atributos)
    return atributos
