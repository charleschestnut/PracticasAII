#-*- coding: utf-8 -*-


import urllib.request
import os
from django.core.files.base import File

def descargarFichero(url, file):
    try:
        if os.path.exists(file):
            recarga = input("S ó N")
            if recarga == "s":
                urllib.request.urlretrieve(url, file)
        else:
            urllib.request.urlretrieve(url, file)
        return File
    except:
        print("Error al conectarse a la pagina")
        return None


descargarFichero("http://www.us.es/rss/feed/portada", "noticias")
    if abrir_url("enlace", fichero):
        with open(fichero, encoding='uft-8', mode='r') as f:
            s = f.read()
            patron= r'patron'
            

