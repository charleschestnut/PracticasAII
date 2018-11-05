'''
Created on 05.11.2018

@author: Lisa
'''


from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3



def cargar():
    conn = sqlite3.connect('database.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS DATABASE")
    conn.execute('''CREATE TABLE IF NOT EXISTS DATABASE 
    (TITEL     TEXT     NOT NULL,
    LINK     TEXT    NOT NULL,
    AUTHOR    TEXT     NOT NULL,
    STARTDATE    INT    NOT NULL,
    ANSWERS    INT    NOT NULL,
    VISITS    INT    NOT NULL);''')
    
    l = extractXml()
    #print(l)
    for i in l:
            title = i.find("a", class_="title").string.strip()
            #print(title)
            link = "https://foros.derecho.com/" + i.find("a", class_="title")['href']
            #print(link)
            author =i.find("a", class_="username understate").string.strip()
            #print(author)
            starttime = i.find("a", class_="username understate")['title']
            date = re.compile('(\d+).{4}(\d+)').search(starttime).group(0)
            #print(date)
            answers = int(i.find(lambda tag: tag.name == 'a' and tag['class'] == ['understate']).string.strip())
            #print(answers)            
            visits1 = i.find("ul" , class_="threadstats td alt").find("li").find_next_sibling("li")
            visits = re.compile('(\d+)').search(visits1.string.strip()).group(0)
            #print(visits)
            
            conn.execute('''INSERT INTO DATABASE VALUES (?,?,?,?,?,?)''', (title, link, author, date, answers, visits))
    conn.commit()
    cursor = conn.execute('''SELECT COUNT(*) FROM DATABASE''')
    messagebox.showinfo("Load comments", str(cursor.fetchone()[0]) + " comments were loaded!")
            
def extractXml():
     urls = ["https://foros.derecho.com/foro/20-Derecho-Civil-General", "https://foros.derecho.com/foro/20-Derecho-Civil-General/page2", "https://foros.derecho.com/foro/20-Derecho-Civil-General/page3"]
     l= []
     for url in urls:
         f = urllib.request.urlopen("https://foros.derecho.com/foro/20-Derecho-Civil-General") 
         s = BeautifulSoup(f,"lxml")
         l = l + s.find_all("li", class_= ["threadbit "])
     #print(l)
     return l
 
def showData():
    conn = sqlite3.connect('database.db')
    conn.text_factory = str 
    cursor = conn.execute('''SELECT * FROM DATABASE''')
    
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=LEFT, fill=Y)
    lb = Listbox(v, width=200, yscrollcommand=sc.set)
    for row in cursor:
        title = row[0]
        lb.insert(END, "\n")
        lb.insert(END, title)
        author = row[2]
        lb.insert(END, author)
        dates = row[3]
        lb.insert(END, dates)
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command = lb.yview)
    
    conn.close()

def searchTitle():
    def searchfor():
        conn = sqlite3.connect('database.db')
        s = "%"+searchEntry.get()+"%" 
        cursor = conn.execute("""SELECT TITEL, LINK, AUTHOR, STARTDATE, ANSWERS, VISITS FROM DATABASE WHERE TITEL LIKE ?""", (s,))
        showResult(cursor)
        conn.close()
        
    v=Toplevel()
    labelSearch = Label(v, text="Search for Theme: ")
    labelSearch.grid(row=0, column =0)
    searchEntry = Entry(v)
    searchEntry.grid(row=0, column =1)
    search = Button(v, text="Search", command= searchfor)
    search.grid(row=1, column =1)

def searchAuthor():
    def searchfor():
        conn = sqlite3.connect('database.db')
        s = "%"+searchEntry.get()+"%" 
        cursor = conn.execute("""SELECT TITEL, LINK, AUTHOR, STARTDATE, ANSWERS, VISITS FROM DATABASE WHERE AUTHOR LIKE ?""", (s,))
        showResult(cursor)
        conn.close()   

    v = Toplevel()
    labelSearch = Label(v, text="Search for Author: ")
    labelSearch.grid(row=0, column =0)
    searchEntry = Entry(v)
    searchEntry.grid(row=0, column =1)
    search = Button(v, text="Search", command= searchfor)
    search.grid(row=1, column =1)

def searchDate():
    def searchfor():
        conn = sqlite3.connect('database.db')
        s = "%"+searchEntry.get()+"%" 
        cursor = conn.execute("""SELECT TITEL, LINK, AUTHOR, STARTDATE, ANSWERS, VISITS FROM DATABASE WHERE STARTDATE LIKE ?""", (s,))
        showResult(cursor)
        conn.close()   

    v = Toplevel()
    labelSearch = Label(v, text="Search for Date: ")
    labelSearch.grid(row=0, column =0)
    searchEntry = Entry(v)
    searchEntry.grid(row=0, column =1)
    search = Button(v, text="Search", command= searchfor)
    search.grid(row=1, column =1)

def showResult(cursor):
    #print(cursor[1])
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill=Y)
    lb = Listbox(v, width=200, yscrollcommand=sc.set)
    if(cursor != None):
        for row in cursor:
            lb.insert(END, "\n")
            lb.insert(END, row[0])
            lb.insert(END, row[2])
            lb.insert(END, row[3])
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command = lb.yview)
    
    else:
        messagebox.showinfo("Nothing", "There is no entry")
   
def famousAnswers():
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill=Y)
    lb = Listbox(v, width=200, yscrollcommand=sc.set)
    conn = sqlite3.connect('database.db')
    curser = conn.execute('''SELECT TITEL, AUTHOR, STARTDATE, ANSWERS FROM DATABASE ORDER BY ANSWERS DESC LIMIT 5''')
    
    for row in curser:
        lb.insert(END, "\n")
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, row[3])
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command = lb.yview)  
    
    conn.close()
    
def famoustVisits():
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side = RIGHT, fill=Y)
    lb = Listbox(v, width=200, yscrollcommand=sc.set)
    conn = sqlite3.connect('database.db')
    curser = conn.execute('''SELECT TITEL, AUTHOR, STARTDATE, VISITS FROM DATABASE ORDER BY VISITS DESC LIMIT 5''')
    
    for row in curser:
        lb.insert(END, "\n")
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, row[3])
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command = lb.yview)  
    
    conn.close()
    
def create():
    root = Tk()
    menubar = Menu(root)
    
    #Erstellt ersten Menubutton mit Unterbutton: Open, Exit
    filemenu = Menu(menubar, tearoff = 0)
    filemenu.add_command(label="Cargar", command=cargar)
    filemenu.add_command(label = "Mostrar", command=showData)
    filemenu.add_command(label = "Salir", command=root.destroy)
    #Fuegt Button zum Menu hinzu
    menubar.add_cascade(label = "Data", menu = filemenu)
    
    #Erstellt ersten Menubutton mit Unterbutton: New, Modify, Delete
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label = "Tema", command = searchTitle)
    editmenu.add_command(label = "Autor", command = searchAuthor)
    editmenu.add_command(label = "Fecha", command = searchDate)
    #Fuegt Button zum Menu hinzu
    menubar.add_cascade(label = "Buscar", menu = editmenu)
    
    #Erstellt ersten Menubutton
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label = "Temas mas populares", command = famoustVisits)
    helpmenu.add_command(label = "Temas mas activos", command = famousAnswers)
    #Fuegt Button zum Menu hinzu
    menubar.add_cascade(label = "Estadisticas", menu = helpmenu)
    
    #Konfiguriert Menubar
    root.config(menu = menubar)
    root.mainloop()


if __name__ == "__main__":
    create()
