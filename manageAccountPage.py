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
        for F in {ManageAccountPage}:
            login_frame = F(login_screen, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ManageAccountPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class ManageAccountPage(tk.Frame):

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="Manage Account", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()

            log_out_button = tk.Button(self, text="Log Out", fg='blue',
                                     command=lambda: controller.show_frame(ViewAllMuseumsPage))
            curator_request_button = tk.Button(self, borderwidth=0, text="Curator Request", fg='blue',
                                        command=lambda: controller.show_frame(MyTicketsPage))
            delete_account_button = tk.Button(self, borderwidth=0, text="Delete Account", fg='blue',
                                        command=lambda: controller.show_frame(MyReviewsPage))
            back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(ManageAccountPage))

            log_out_button.pack(anchor='n', expand=True)
            curator_request_button.pack(pady=0, anchor='n')
            delete_account_button.pack(pady=0, anchor='n')
            back_button.pack(pady=0, anchor='n')

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
