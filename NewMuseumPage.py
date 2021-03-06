import tkinter as tk
from tkinter import *
from tkinter import messagebox
#import mysql.connector

LARGE_FONT = ("Verdana", 26, "underline")
SMALL_FONT = ("Verdana", 10, "italic")
config = {
    'user': 'root',
    'password': 'rootuserpassword',
    'database': 'bmtrsdb',
    'raise_on_warnings': True,
}
#cnx = mysql.connector.connect(**config)



class BMTRSApp(tk.Tk):

    #self is implied -- it's the first parameter
    #args = arguments
    #keyboard arguments
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        main_window = tk.Frame(self)
        self.wm_title("")

        #fill fills space allotted
        #expand beyond space allotted
        main_window.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        main_window.grid_rowconfigure(0, weight=1)
        main_window.grid_columnconfigure(0, weight=1)

        self.frames ={}
        frame = NewMuseumPage(main_window, self)
        self.frames[NewMuseumPage] = frame
        #sticky alignment + stretch - so it aligns everything to all sides of window
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(NewMuseumPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]
def submitNewMuseum():
    print("New Museum Added")

#PAGE 1 - New Museum PAGE
class NewMuseumPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="New Museum Form", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        information_entry_frame = tk.Frame(self, borderwidth=5, relief='groove', pady=10)
        information_entry_frame.pack(anchor='center', pady=20, padx=5)
        museum_name_label = tk.Label(information_entry_frame, text="Name*:", font=SMALL_FONT)
        museum_name_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        museum_name_text = StringVar()
        museum_name_entry = tk.Entry(information_entry_frame, textvariable=museum_name_text)
        museum_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        submit_museum_button = tk.Button(self, text="Submit Museum", fg='blue',
                                 command=lambda: submitNewMuseum())
        back_button = tk.Button(self, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(AdminHomePage))
    
        submit_museum_button.pack(anchor='n', expand=True)
        back_button.pack(pady=0, anchor='n')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n')

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
