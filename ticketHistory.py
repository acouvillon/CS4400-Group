from __future__ import print_function
import tkinter as tk
from tkinter import *
from tkinter import ttk

import mysql.connector
from mysql.connector import errorcode
import datetime


museum_list = []
time_list = []
price_list = []


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

    query = ("""SELECT museum_name, purchase_timestamp, price
                FROM ticket 
                WHERE email = '{0}'""".format(username))

    cursor.execute(query)
    

    for (museum_name, time, price) in cursor:
        print(museum_name)
        museum_list.append(museum_name)
        time_list.append(time)
        price_list.append(price)
        

    cursor.close()
    cnx.close()
    
    
config = {
  'user': 'root',
  'password': 'rootuserpassword',
  'database': 'bmtrsdb',
  'raise_on_warnings': True,
}

# cnx = mysql.connector.connect(**config)
# cursor = cnx.cursor()
# DB_NAME = 'bmtrsdb'

# query = ("SELECT museum_name, AVG(rating) FROM museum "
			# " NATURAL LEFT OUTER JOIN review GROUP BY museum_name")

# cursor.execute(query)

# museum_list = []
# review_list = []

# for (museum_name, review) in cursor:
	# museum_list.append(museum_name)
	# review_list.append(review)
	

# cursor.close()
# cnx.close()

LARGE_FONT = ("Verdana", 26, "underline")
SMALL_FONT = ("Verdana", 10, "italic")
class BMTRSApp(tk.Tk):

    #self is implied -- it's the first parameter
    #args = arguments
    #keyboard arguments
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        ticket_history_screen = tk.Frame(self)
        #fill fills space allotted
        #expand beyond space allotted
        ticket_history_screen.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        ticket_history_screen.grid_rowconfigure(0, weight=1)
        ticket_history_screen.grid_columnconfigure(0, weight=1)

        self.frames ={}
        # for F in {TicketHistoryPage, RegistrationPage}:
        for F in {TicketHistoryPage}: 
            ticket_history_frame = F(ticket_history_screen, self)
            self.frames[F] = ticket_history_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            ticket_history_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(TicketHistoryPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

#PAGE 7 - VIEW ALL MUSUEMS page
class TicketHistoryPage(tk.Frame):

    tree = None
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="My Tickets", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.tree = ttk.Treeview(main_frame)
            
        self.tree['columns'] = ('date', 'price')
        self.tree.column('date', width=100, anchor='center')
        self.tree.column('price', width=100, anchor='e')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('date', text='Purchase Date')
        self.tree.heading('price', text='Price')
        self.tree.pack()
        back_button = tk.Button(self, text="Back", fg='black', command=lambda: controller.show_frame(self))
        back_button.pack(pady=5, anchor='n')
        #self.populateTable('helen@gatech.edu')
        
    #must be called from user login page at login
    def populateTable(self, username):
        num = 0
        sqlQuery(username)
        for museum in museum_list:
            self.tree.insert('', 'end', text=museum, values=(time_list[num].strftime('%m/%d/%Y'), '$'+price_list[num]))
            num+=1
        
        
app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
