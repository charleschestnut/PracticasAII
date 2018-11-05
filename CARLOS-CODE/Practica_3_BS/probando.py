#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup


html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# Esto lo que nos hace es poner en bune formato los datos que hay dentro
# de la variable.
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())

# Aquí tenemos varias maneras de navegar por la estructura de datos.
soup.title

soup.title.name

soup.title.string

soup.title.parent.name

soup.p

soup.p['class']

soup.a

soup.find_all('a')

soup.find(id="link3")


# Una práctica muy común es extraer las diferentes URLs encontradas
# en la página usando con etiqueta <a>:

for link in soup.find_all('a'):
    print(link.get('href'))


# Otra práctica común es extraer texto de toda la página

print(soup.get_text())

