'''
Created on 05.11.2018

@author: Lisa
'''

from tkinter import *
from tkinter import messagebox
import urllib.request
import sqlite3
from bs4 import BeautifulSoup


def safeDatabase():
    conn = sqlite3.connect('news.db')
    conn.text_factory = str 
    conn.execute("DROP TABLE IF EXISTS NEWS")
    conn.execute('''CREATE TABLE IF NOT EXISTS NEWS (
    TITEL    TEXT    NOT NULL,
    LINK    TEXT     NOT NULL,
    AUTHOR    TEXT    NOT NULL,
    DATE    TEXT    NOT NULL, 
    CONTENT     TEXT    NOT NULL);''')
    
    xml = extractXML()
    print(xml)
    for i in xml:
        titel = i.find('h2').find('a').string.strip()
        #print(titel)
        link = i.find('h2').find('a')['href']
        #print(link)
        author = i.find("div", class_="news-submitted").find("a").find_next_sibling("a").string.strip()
        print(author)
        dates = i.find("span", class_="ts visible").string.strip()
        date=0
        print(dates)
        content = i.find("div", class_="news-content").text.strip()
        #print(content)
        conn.execute('''INSERT INTO NEWS VALUES(?,?,?,?,?)''', (titel, link, author, date, content))
    conn.commit()
   
    cursor = conn.execute('''SELECT COUNT(*) FROM NEWS''')
    messagebox.showinfo("Number", "The Database has " + str(cursor.fetchone()[0]) +" entrys")
    conn.close()
    
def extractXML():
    urls = ["https://www.meneame.net/","https://www.meneame.net/?page=2", "https://www.meneame.net/?page=3"]
    l=[]
    
    for url in urls:
        print(url)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, "lxml")
        l =l + ( s.find_all("div", class_=["news-summary"]))
    print(l)
   
    return l

def showDB():
    conn = sqlite3.connect('news.db')
    cursor = conn.execute('''SELECT TITEL, AUTHOR, DATE FROM NEWS''')
    
    v = Toplevel()
    sc= Scrollbar(v)
    sc.pack(side=LEFT, fill=Y)
    lb = Listbox(v, width='200', yscrollcommand=sc.set )
    for item in cursor:
        lb.insert(END,'\n')
        lb.insert(END,item[0])
        lb.insert(END, item[1])
        lb.insert(END, item[2])
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command = lb.yview)
    conn.close()
  
def searchInContent():
    def search():
      conn = sqlite3.connect('news.db')
      s = "%"+entry.get()+"%"
      print(s)
      cursor = conn.execute('''SELECT TITEL, AUTHOR, DATE FROM NEWS WHERE CONTENT LIKE ?''',(s,))
      showResult(cursor)
      conn.close()
        
        
    v = Toplevel()
    label = Label(v, text="Search in Content for: ")
    entry = Entry(v)
    button = Button(v, text="Search!", command=search)
    label.grid(row=0, column=0)
    entry.grid(row=0, column =1 )
    button.grid(row=1, column=1)
 
#search Author through Spinbox and show every entry of the author 
def searchAutor():
    def list():
        author=conn.execute('''SELECT TITEL, AUTHOR, DATE FROM NEWS WHERE AUTHOR LIKE ?''', (w.get(),))
        showResult(author)
    conn = sqlite3.connect('news.db')
    authors = conn.execute('''SELECT AUTHOR FROM NEWS''')
    
    v = Toplevel()
    label = Label(v, text="Search in Content for: ")
    values=[]
    for i in authors:
        values.append(i)
    w = Spinbox(v, values=(values))

    button = Button(v, text="Search!", command=list)
    label.grid(row=0, column=0)
    w.grid(row=0, column =1 )
    button.grid(row=1, column=1)
      
    
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
            lb.insert(END, row[1])
            lb.insert(END, row[2])
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command = lb.yview)
    else:
        messagebox.showinfo("Nothing", "There is no entry")
           
def create():
    top = Tk()
    menubar = Menu(top)
    
    firstmenu = Menu(menubar, tearoff=0)
    firstmenu.add_command(label="Load", command=safeDatabase)
    firstmenu.add_command(label="Show", command=showDB)
    firstmenu.add_command(label="Exit", command=top.destroy)
    menubar.add_cascade(label="Data", menu =firstmenu)
    
    seccondmenu = Menu(menubar, tearoff=0)
    seccondmenu.add_command(label="Notice", command=searchInContent)
    seccondmenu.add_command(label="Author", command=searchAutor)
    seccondmenu.add_command(label="Date", command=None)
    menubar.add_cascade(label="Search", menu=seccondmenu)
    
    top.config(menu = menubar)
    top.mainloop()


if __name__ == "__main__":
    create()