from __future__ import print_function
import tkinter as tk
from tkinter import *
from tkinter import ttk

import mysql.connector
from mysql.connector import errorcode
import datetime

config = {
  'user': 'root',
  'password': '',
  'database': 'bmtrsdb',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
DB_NAME = 'bmtrsdb'

query = ("SELECT museum_name, AVG(rating) FROM museum "
			" NATURAL LEFT OUTER JOIN review GROUP BY museum_name")

cursor.execute(query)

museum_list = []
review_list = []

for (museum_name, review) in cursor:
	museum_list.append(museum_name)
	review_list.append(review)
	

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
        view_museums_screen = tk.Frame(self)
        #fill fills space allotted
        #expand beyond space allotted
        view_museums_screen.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        view_museums_screen.grid_rowconfigure(0, weight=1)
        view_museums_screen.grid_columnconfigure(0, weight=1)

        self.frames ={}
        # for F in {ViewMuseumsPage, RegistrationPage}:
        for F in {ViewMuseumsPage}: 
            view_museums_frame = F(view_museums_screen, self)
            self.frames[F] = view_museums_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            view_museums_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ViewMuseumsPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

#PAGE 7 - VIEW ALL MUSUEMS page
class ViewMuseumsPage(tk.Frame):
	def __init__(self, parent, controller):
			tk.Frame.__init__(self, parent)
			title = tk.Label(self, text="All Museums", font=LARGE_FONT)
			title.pack(pady=10, padx=10)
			main_frame = tk.Frame(self, pady=10)
			main_frame.pack(anchor='center', pady=0, padx=5)
			tree = ttk.Treeview(main_frame)
			num = 0
			for museum in museum_list:
				tree.insert('', 'end', text=museum, values=(review_list[num]))
				num+=1
				
			tree['columns'] = ('rating')
			tree.column('rating', width=100, anchor='ne')
			tree.heading('#0', text='Museum Name')
			tree.heading('rating', text='Average Rating')
			tree.pack()
			select_button = tk.Button(self, text="Select", fg='black', command=lambda: controller.show_frame(ViewMuseumsPage))
			select_button.pack(pady=5, anchor='n')
			back_button = tk.Button(self, text="Back", fg='black', command=lambda: controller.show_frame(ViewMuseumsPage))
			back_button.pack(pady=5, anchor='n')

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
