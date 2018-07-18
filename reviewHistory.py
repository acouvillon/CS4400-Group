from __future__ import print_function
import tkinter as tk
from tkinter import *
from tkinter import ttk

import mysql.connector
from mysql.connector import errorcode
import datetime


museum_list = []
review_list = []
rating_list = []


def sqlQuery(username):
    config = {
      'user': 'root',
      'password': 'rootuserpassword',
      'database': 'bmtrsdb',
      'raise_on_warnings': True,
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    DB_NAME = 'bmtrsdb'

    query = ("""SELECT museum_name, comment, rating
                FROM review 
                WHERE email = '{0}'""".format(username))

    cursor.execute(query)
    

    for (museum_name, review, rating) in cursor:
        museum_list.append(museum_name)
        review_list.append(review)
        rating_list.append(rating)
        

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
        review_history_screen = tk.Frame(self)
        #fill fills space allotted
        #expand beyond space allotted
        review_history_screen.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        review_history_screen.grid_rowconfigure(0, weight=1)
        review_history_screen.grid_columnconfigure(0, weight=1)

        self.frames ={}
        # for F in {ReviewHistoryPage, RegistrationPage}:
        for F in {ReviewHistoryPage}: 
            review_history_frame = F(review_history_screen, self)
            self.frames[F] = review_history_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            review_history_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ReviewHistoryPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

#PAGE 9 - MY REVIEWS page
class ReviewHistoryPage(tk.Frame):

    tree = None
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="My Reviews", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.tree = ttk.Treeview(main_frame)
            
        self.tree['columns'] = ('review', 'rating')
        self.tree.column('#0', width=150, anchor='center')
        self.tree.column('review', width=300, anchor='center')
        self.tree.column('rating', width=50, anchor='e')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('review', text='Review')
        self.tree.heading('rating', text='Rating')
        self.tree.pack()
        back_button = tk.Button(self, text="Back", fg='black', command=lambda: controller.show_frame(self))
        back_button.pack(pady=5, anchor='n')
        self.populateTable('helen@gatech.edu')
        
    #must be called from user login page at login
    def populateTable(self, username):
        num = 0
        sqlQuery(username)
        for museum in museum_list:
            self.tree.insert('', 'end', text=museum, values=(review_list[num], str(rating_list[num])+'/5'))
            num+=1
        
        
app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
