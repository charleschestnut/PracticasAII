from bs4 import BeautifulSoup
from tkinter import *
from sqlite3 import *
from urllib import request


def main_window():
    top = Tk()
    store_view = Button(top, text="Store", command=store_data)
    store_view.pack(side=LEFT)
    list_view = Button(top, text="List", command=list_data)
    list_view.pack(side=LEFT)
    search_title_view = Button(top, text="Search by title", command=lambda: search_data("title"))
    search_title_view.pack(side=LEFT)
    search_author_view = Button(top, text="Search by author", command=lambda: search_data("author"))
    search_author_view.pack(side=LEFT)
    search_date_view = Button(top, text="Search by date", command=lambda: search_data("date"))
    search_date_view.pack(side=LEFT)
    order_answers_view = Button(top, text="Order by answers", command=lambda: order_data("answers"))
    order_answers_view.pack(side=LEFT)
    order_views_view = Button(top, text="Order by views", command=lambda: order_data("views"))
    order_views_view.pack(side=LEFT)
    exit_view = Button(top, text="Exit", command=lambda: exit())
    exit_view.pack(side=LEFT)
    top.mainloop()


def store_data():
    conn = connect('test.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS TEMAS")
    conn.execute('''CREATE TABLE TEMAS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        lINK TEXT NOT NULL,
        AUTOR TEXT NOT NULL,
        FECHA TEXT NOT NULL,
        RESPUESTAS NUMBER NOT NULL,
        VISITAS NUMBER NOT NULL);''')
    data = retrieve_data("https://foros.derecho.com/foro/20-Derecho-Civil-General")
    for i in data:
        cursor = conn.execute(
            """INSERT INTO TEMAS (TITULO, LINK, AUTOR, FECHA, RESPUESTAS, VISITAS) VALUES (?,?,?,?,?,?)""", i)
        cursor.close()
    conn.commit()
    conn.close()


def retrieve_data(d: str):
    data = []
    page = retrieve_page(d)
    for child in page.find("ol", id="threads").findAll("li", class_="threadbit"):
        item = [
            child.find("h3", class_="threadtitle").a.text,
            "https://foros.derecho.com/" + child.find("h3", class_="threadtitle").a["href"],
            child.find("a", class_="username understate").text,
            child.dd.next_sibling.next_sibling.text,
            child.find("ul", class_="threadstats").contents[1].a.text,
            child.find("ul", class_="threadstats").contents[3].text.split(":", 1)[1].strip()
        ]
        data.append(item)
    return data


def retrieve_page(d: str):
    file = request.urlopen(d)
    doc = BeautifulSoup(file, "lxml")
    return doc


def list_data():
    conn = connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO,LINK,AUTOR,FECHA,RESPUESTAS,VISITAS FROM TEMAS")
    print_theme(cursor)
    conn.close()


def print_theme(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, row[3])
        lb.insert(END, row[4])
        lb.insert(END, row[5])
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def search_data(search_type: str):
    def show_search(entry):
        conn = connect('test.db')
        conn.text_factory = str
        entry_text = entry.get()
        s = "%" + entry_text + "%"
        if search_type == "title":
            if entry_text:
                cursor = conn.execute("""SELECT * FROM TEMAS WHERE TITULO LIKE ?""", (s,))  # THE COMMA IS NECESSARY.
            else:
                cursor = conn.execute("""SELECT * FROM TEMAS""")
        elif search_type == "author":
            if entry_text:
                cursor = conn.execute("""SELECT * FROM TEMAS WHERE AUTOR LIKE ?""", (s,))  # THE COMMA IS NECESSARY.
            else:
                cursor = conn.execute("""SELECT * FROM TEMAS""")
        elif search_type == "date":
            if entry_text:
                cursor = conn.execute("""SELECT * FROM TEMAS WHERE FECHA LIKE ?""", (s,))  # THE COMMA IS NECESSARY.
            else:
                cursor = conn.execute("""SELECT * FROM TEMAS""")
        print_theme(cursor)
        conn.close()

    if search_type == "title":
        search_text = "Type a theme: "
    elif search_type == "author":
        search_text = "Type an author: "
    elif search_type == "date":
        search_text = "Type a date (dd/mm/yyyy): "
    v = Toplevel()
    lb = Label(v, text=search_text)
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", lambda event: show_search(en))
    en.pack(side=LEFT)


def order_data(order_type:str):
    conn = connect('test.db')
    conn.text_factory = str
    if order_type == "views":
        cursor = conn.execute("""SELECT * FROM TEMAS ORDER BY VISITAS ASC LIMIT 5""")
    elif order_type == "answers":
        cursor = conn.execute("""SELECT * FROM TEMAS ORDER BY RESPUESTAS ASC LIMIT 5""")
    print_theme(cursor)
    conn.close()


if __name__ == "__main__": main_window()
