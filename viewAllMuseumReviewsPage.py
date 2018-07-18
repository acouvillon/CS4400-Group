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
        for F in {ViewAllMuseumReviewsPage}:
            login_frame = F(login_screen, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ViewAllMuseumReviewsPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class ViewAllMuseumReviewsPage(tk.Frame):

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="All Reviews", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()
            main_frame = tk.Frame(self, pady=10)
            main_frame.pack(anchor='center', pady=0, padx=5)
            review_list = getReviews()

            tree = ttk.Treeview(main_frame)
            num = 0
            for review in review_list:
                tree.insert('', 'end', text=review, values=('rating'))
                num+=1

            tree['columns'] = ('rating')
            tree.column('#0', width=300, anchor='w')
            tree.column('rating', width=100, anchor='center')
            tree.heading('#0', text='Review')
            tree.heading('rating', text='Rating')
            tree.pack()

            back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(ViewSpecificMuseumPage))
            back_button.pack(pady=0, anchor='n')

def getReviews():
    #TODO: put SQL statement here
    return ['review 1', 'review 2', 'review 3']

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
