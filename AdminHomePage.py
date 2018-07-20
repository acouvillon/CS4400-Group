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
        for F in {AdminHomePage}:
            login_frame = F(login_screen, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(AdminHomePage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

class AdminHomePage(tk.Frame):

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="Welcome, Sir/Madam", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()

            accept_curator_request_button = tk.Button(self, text="Accept Curator Request", fg='blue',
                                     command=lambda: controller.show_frame(adminCuratorRequestsPage))
            add_museum_button = tk.Button(self, text="Add Museum", fg='blue',
                                        command=lambda: controller.show_frame(NewMuseumPage))
            delete_museum_button = tk.Button(self, text="Delete Museum", fg='blue',
                                        command=lambda: controller.show_frame(DeleteMuseumFormPage))
            log_out_button = tk.Button(self, text="Log Out", fg='blue',
                                        command=lambda: controller.show_frame(LoginPage))

            accept_curator_request_button.pack(pady=5, anchor='n', expand=True)
            add_museum_button.pack(pady=5, anchor='n', expand=True)
            delete_museum_button.pack(pady=5, anchor='n', expand=True)
            log_out_button.pack(pady=5, anchor='n', expand=True)

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
