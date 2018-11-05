#-*- coding: utf-8 -*-

# Para parsear un documento, tenemos que pasarla por el constructor de BS.
# Puedes pasar un string o un nombre de archivo 
from bs4 import BeautifulSoup

#with open("index.html") as fp:
#    soup = BeautifulSoup(fp)

soup = BeautifulSoup("<html>data</html>")

#Primero es convertido a Unicode, y las entidades HTML a caracteres unicode también.

a = BeautifulSoup("Sacr&eacute; bleu!")
print(a)
# Se convierte en:  <html><head></head><body>Sacré bleu!</body></html>

