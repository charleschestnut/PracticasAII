# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from tkinter import *
from sqlite3 import *
from tkinter import messagebox
from urllib import request


def main_window():
    top = Tk()
    store_view = Button(top, text="Almacenar Productos", command=store_data)
    store_view.pack(side=LEFT)
    list_view = Button(top, text="Ordenar por Precio Unitario", command=lambda: order_data())
    list_view.pack(side=LEFT)
    list_view = Button(top, text="Mostrar Marca", command=lambda: list_data())
    list_view.pack(side=LEFT)
    list_view = Button(top, text="Buscar Rebajas", command=lambda: search_data())
    list_view.pack(side=LEFT)
    exit_view = Button(top, text="Salir", command=lambda: exit())
    exit_view.pack(side=LEFT)
    top.mainloop()


def store_data():
    conn = connect('test.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute('''CREATE TABLE PRODUCTOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            DENOMINACION TEXT NOT NULL,
            MARCA TEXT NOT NULL,
            PRECIO_KILO DOUBLE NOT NULL,
            PRECIO_ANTIGUO DOUBLE,
            PRECIO_FINAL DOUBLE NOT NULL);''')
    arbol = retrieve_page("https://www.ulabox.com/en/campaign/productos-sin-gluten#gref")
    denominaciones, marcas, precio_vars, precios, precio_ants = retrieve_data(arbol)
    contador = 0
    for i in denominaciones:
        cursor = conn.execute(
            """INSERT INTO PRODUCTOS (DENOMINACION, MARCA, PRECIO_KILO, PRECIO_ANTIGUO, PRECIO_FINAL) VALUES (?,?,?,?,?)""",
            (denominaciones[contador], marcas[contador], precio_vars[contador], precio_ants[contador], precios[contador]))
        contador = contador + 1
        cursor.close()
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    values = cursor.fetchone()
    popup_count(values[0])
    conn.close()


def popup_count(count: int):
    win = Toplevel()
    win.wm_title("Resultado")

    l = Label(win, text="Se han añadido " + str(count) + " entradas.")
    l.grid(row=0, column=0)

    b = Button(win, text="Ok", command=win.destroy)
    b.grid(row=1, column=0)


def retrieve_data(arbol):
    def modificar_precio(precio: str):
        real_precio = precio[4:8]
        real_precio = real_precio.strip()
        real_precio = real_precio.replace(",", ".")
        real_precio = float(real_precio)
        return real_precio

    # Filtramos para tener directamente la lista de PRODUCTOS
    productos = arbol.find("div", id="product-list")
    denominaciones = []
    marcas = []
    precio_vars = []
    precios = []
    precio_ants = []

    for producto in productos.find_all("div", class_="grid__item m-one-whole t-one-third d-one-third dw-one-quarter | js-product-grid-grid"):
        denominacion = producto.find('h3').find('a')
        denominaciones.append(denominacion.text.strip())
        print(denominacion.text.strip())

        marca = producto.find('h4').find('a')
        marcas.append(marca.text.strip())
        print(marca.text.strip())

        precio_var = producto.find('small', class_="product-item__ppu nano")
        precio_var = modificar_precio(precio_var.text)
        precio_vars.append(precio_var)
        print(precio_var)

        precio_int = producto.find('span', class_='delta')
        precio_dec = producto.find('span', class_="milli")
        precio = int(precio_int.text) + 0.01 * float(precio_dec.text[1:-1].strip())
        precios.append(precio)

        if len(producto.find("span", class_="product-grid-footer__price").contents) == 2:
            precio_ant = producto.find("span", class_="product-grid-footer__price").find_all("del")[0].string
        else:
            precio_ant = None
        precio_ants.append(precio_ant)

    return denominaciones, marcas, precio_vars, precios, precio_ants


def retrieve_page(d: str):
    file = request.urlopen(d)
    doc = BeautifulSoup(file, "html.parser")
    return doc


def list_data():
    def list():
        cursor = conn.execute('''SELECT * FROM PRODUCTOS WHERE MARCA LIKE ?''', (w.get(),))
        print_product(cursor)

    conn = connect('test.db')
    brands = conn.execute('''SELECT MARCA FROM PRODUCTOS''')

    v = Toplevel()
    label = Label(v, text="Buscar Marca: ")
    values = []
    for i in brands:
        values.append(i)
    w = Spinbox(v, values=(values))

    button = Button(v, text="¡Buscar!", command=list)
    label.grid(row=0, column=0)
    w.grid(row=0, column=1)
    button.grid(row=1, column=1)


def search_data():
    conn = connect('test.db')
    cursor = conn.execute('''SELECT * FROM PRODUCTOS WHERE PRECIO_ANTIGUO !=  NULL''')
    print_product(cursor)
    conn.close()


def order_data():
    conn = connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT * FROM PRODUCTOS ORDER BY PRECIO_KILO ASC""")
    print_product(cursor)
    conn.close()


def print_product(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    if cursor != None:
        for row in cursor:
            lb.insert(END, "Nombre: " + str(row[1]))
            lb.insert(END, "Precio antiguo: " + str(row[4]))
            lb.insert(END, "Precio final: " + str(row[5]))
            lb.insert(END, '')
    else:
        messagebox.showinfo("Error", "No se obtuvieron resultados...")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


if __name__ == "__main__": main_window()
