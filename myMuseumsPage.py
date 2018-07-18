import tkinter as tk
from tkinter import *
from tkinter import ttk

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
        for F in {MyMuseumsPage}:
            login_frame = F(login_screen, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MyMuseumsPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class MyMuseumsPage(tk.Frame):

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="My Museums", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()
            main_frame = tk.Frame(self, pady=10)
            main_frame.pack(anchor='center', pady=0, padx=5)
            my_museums_list = getMyMuseums()

            tree = ttk.Treeview(main_frame)
            num = 0
            for museum in my_museums_list:
                tree.insert('', 'end', text=museum, values=("1", "5/5"))
                num+=1

            tree['columns'] = ('numExhibits','rating')
            tree.column('#0', width=200, anchor='w')
            tree.column('numExhibits', width=75, anchor='center')
            tree.column('rating', width=75, anchor='e')
            tree.heading('#0', text='Museum')
            tree.heading('numExhibits', text='Exhibit Count')
            tree.heading('rating', text='Rating')
            tree.pack()

            back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(ManageAccountPage))
            back_button.pack(pady=0, anchor='n')

def getMyMuseums():
    #TODO: put SQL statement here
    return ['museum 1', 'museum 2', 'museum 3']

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
