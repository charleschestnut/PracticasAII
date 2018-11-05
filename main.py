from bs4 import BeautifulSoup
from tkinter import *
from sqlite3 import *
from urllib import request


def main_window():
    top = Tk()
    store_view = Button(top, text="Almacenar Productos", command=store_data)
    store_view.pack(side=LEFT)
    list_view = Button(top, text="Ordenar por Precio Unitario", command=order_data())
    list_view.pack(side=LEFT)
    list_view = Button(top, text="Mostrar Marca", command=list_data())
    list_view.pack(side=LEFT)
    list_view = Button(top, text="Buscar Rebajas", command=search_data())
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
            PRECIO_FINAL DOUBLE NOT NULL);''')
    data = retrieve_data("https://www.ulabox.com/en/campaign/productos-sin-gluten#gref")
    for i in data:
        cursor = conn.execute(
            """INSERT INTO PRODUCTOS (DENOMINACION, MARCA, PRECIO_KILO, PRECIO_FINAL) VALUES (?,?,?,?)""", i)
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


def retrieve_data(d: str):
    return  # TODO: retrieve the necessary data from the URL in parameter d as an array


def retrieve_page(d: str):
    file = request.urlopen(d)
    doc = BeautifulSoup(file, "lxml")
    return doc


def list_data():
    return  # TODO: Retrieve the data from the database and show them in the interface


def search_data():
    return  # TODO: Search the database applying some filter


def order_data():
    return  # TODO: Sort the data from the database using some criteria


if __name__ == "__main__": main_window()
