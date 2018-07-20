from __future__ import print_function
import tkinter as tk
from tkinter import *

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
        for F in {DeleteMuseumFormPage}:
            login_frame = F(login_screen, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(DeleteMuseumFormPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        
def replaceThis():
        print("Museum Successfully Deleted")

class DeleteMuseumFormPage(tk.Frame):
    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="Delete Museum Form", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()

            museum_select_frame = tk.Frame(self, borderwidth=5, relief='groove')
            museum_select_frame.pack(anchor='center', pady=20, padx=20, ipadx=20)

            museums = StringVar()
            choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
            museums.set('Pizza') # set the default option

            pickAMuseum = tk.Label(museum_select_frame, text="What Museum Do You Want to Delete?")
            popupMenu = tk.OptionMenu(museum_select_frame, museums, *choices)
            pickAMuseum.grid(row=0, column=0, sticky='e', pady=5, padx=5)
            popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)

            # on change dropdown value
            def change_dropdown(*args):
                print( museums.get() )

            # link function to change dropdown
            museums.trace('w', change_dropdown)

            delete_museum_button = tk.Button(self, text="Delete Museum", fg='blue',
                                     command=lambda: replaceThis())
            back_button = tk.Button(self, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(AdminHomePage))
    

            delete_museum_button.pack(pady=20, anchor='n')
            back_button.pack(pady=5, anchor='n')

            
app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
