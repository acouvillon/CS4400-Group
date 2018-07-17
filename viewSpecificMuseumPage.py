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

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="[INSERT MUSEUM NAME HERE]", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()
            main_frame = tk.Frame(self, pady=10)
            main_frame.pack(anchor='center', pady=0, padx=5)
            exhibit_list = getExhibits()

            tree = ttk.Treeview(main_frame)
            num = 0
            for exhibit in exhibit_list:
                tree.insert('', 'end', text=exhibit, values=("2000", exhibit))
                num+=1

            tree['columns'] = ('year','url')
            tree.column('#0', width=200, anchor='nw')
            tree.column('year', width=100, anchor='nw')
            tree.column('url', width=200, anchor='nw')
            tree.heading('#0', text='Exhibit')
            tree.heading('year', text='Year')
            tree.heading('url', text='Link to Exhibit')
            tree.pack()

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

def getExhibits():
    #TODO: put SQL statement here
    return ['exhibit 1', 'exhibit 2', 'exhibit 3']

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
