from __future__ import print_function
import tkinter as tk
from tkinter import *
from tkinter import ttk

import mysql.connector
from mysql.connector import errorcode
import datetime


exhibit_list = []
year_list = []
link_list = []


def sqlQuery(museum_name):
    config = {
      'user': 'root',
      'password': 'rootuserpassword',
      'database': 'bmtrsdb',
      'raise_on_warnings': True,
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    DB_NAME = 'bmtrsdb'

    query = ("""SELECT exhibit_name, year, url
                FROM exhibit
                WHERE museum_name = '{0}'""".format(museum_name))

    cursor.execute(query)


    for (exhibit, year, link) in cursor:
        exhibit_list.append(exhibit)
        year_list.append(year)
        link_list.append(link)


    cursor.close()
    cnx.close()

LARGE_FONT = ("Verdana", 26, "underline")
SMALL_FONT = ("Verdana", 10, "italic")

class BMTRSApp(tk.Tk):

    #self is implied -- it's the first parameter
    #args = arguments
    #keyboard arguments
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        login_screen = tk.Frame(self)
        #fill fills space allotted
        #expand beyond space allotted
        login_screen.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        login_screen.grid_rowconfigure(0, weight=1)
        login_screen.grid_columnconfigure(0, weight=1)

        self.frames ={}
        for F in {ViewSpecificMuseumPage}:
            login_frame = F(login_screen, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ViewSpecificMuseumPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class ViewSpecificMuseumPage(tk.Frame):

    tree = None
    title = None

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.title = tk.Label(self, text="[INSERT MUSEUM NAME HERE]", font=LARGE_FONT)
            self.title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()
            main_frame = tk.Frame(self, pady=10)
            main_frame.pack(anchor='center', pady=0, padx=5)
            
            self.tree = ttk.Treeview(main_frame)

            self.tree['columns'] = ('year','url')
            self.tree.column('#0', width=200, anchor='w')
            self.tree.column('year', width=50, anchor='center')
            self.tree.column('url', width=200, anchor='e')
            self.tree.heading('#0', text='Exhibit')
            self.tree.heading('year', text='Year')
            self.tree.heading('url', text='Link to Exhibit')
            self.tree.pack()
            
            #self.populateTable('CCCB')

            purchase_ticket_button = tk.Button(self, text="Purchase Ticket", fg='blue',
                                     command=lambda: controller.show_frame(ViewAllMuseumsPage))
            review_museum_button = tk.Button(self, borderwidth=0, text="Review Museum", fg='blue',
                                        command=lambda: controller.show_frame(MyTicketsPage))
            view_other_reviews_button = tk.Button(self, borderwidth=0, text="View Others' Reviews", fg='blue',
                                        command=lambda: controller.show_frame(MyReviewsPage))
            back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(ManageAccountPage))

            purchase_ticket_button.pack(anchor='n', expand=True)
            review_museum_button.pack(pady=0, anchor='n')
            view_other_reviews_button.pack(pady=0, anchor='n')
            back_button.pack(pady=0, anchor='n')
            
            
    #must be called from user login page at login
    def populateTable(self, museum):
        num = 0
        self.title['text'] = museum
        sqlQuery(museum)
        for exhibit in exhibit_list:
            self.tree.insert('', 'end', text=exhibit, values=(year_list[num], link_list[num]))
            num+=1
            
def getExhibits():
    #TODO: put SQL statement here
    return ['exhibit 1', 'exhibit 2', 'exhibit 3']

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
