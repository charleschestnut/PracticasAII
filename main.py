from bs4 import BeautifulSoup
from tkinter import *
from sqlite3 import *
from urllib import request


def main_window():
    root = Tk()
    
    store_view = Button(root, text="Store", command=None)
    store_view.pack(side=LEFT)
    sorted_view = Button(root, text="List", command=None)
    sorted_view.pack(side=LEFT)
    search_brand_view = Button(root, text="Search by title", command=lambda: None)
    search_brand_view.pack(side=LEFT)
    find_discaunt_view = Button(root, text="Search by author", command=lambda: None)
    find_discaunt_view.pack(side=LEFT)
   
    root.mainloop()
    return #TODO: Show the main window


def store_data():
    return  # TODO: Store the data from retieve_data in the database


def retrieve_data(d: str):
    return  # TODO: retrieve the necessary data from the URL in parameter d as an array


def retrieve_page(d: str):
    return  # TODO: auxiliary method for retrieving the website as a websoup object


def list_data():
    return  # TODO: Retrieve the data from the database and show them in the interface

def search_data(search_type: str):
    return  # TODO: Search the database applying some filter

def order_data(order_type:str):
    return  # TODO: Sort the data from the database using some criteria


if __name__ == "__main__": main_window()
