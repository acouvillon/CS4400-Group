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
        museum_review_screen = tk.Frame(self)
        #fill fills space allotted
        #expand beyond space allotted
        museum_review_screen.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        museum_review_screen.grid_rowconfigure(0, weight=1)
        museum_review_screen.grid_columnconfigure(0, weight=1)

        self.frames ={}
        # for F in {MuseumReviewPage, RegistrationPage}:
        for F in {MuseumReviewPage}: 
            museum_review_frame = F(museum_review_screen, self)
            self.frames[F] = museum_review_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            museum_review_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MuseumReviewPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

#todo
#Checks database, validates credentials and allows access to specific museum page
def createreview(username, pwd):
    print("login successful")


#PAGE 5 - MUSEUM REVIEW PAGE
class MuseumReviewPage(tk.Frame):

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="Create A Review", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()
            information_entry_frame = tk.Frame(self, pady=10)
            information_entry_frame.pack(anchor='center', pady=20, padx=5)
            rating_label = tk.Label(information_entry_frame, text="Rating:", font=SMALL_FONT)
            rating_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
            #rating_entry = tk.Entry(information_entry_frame)
            #rating_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
            var = tk.IntVar()
            rating_star1 = tk.Radiobutton(information_entry_frame, variable = var, value = 1, text='1', highlightbackground='white')
            rating_star1.grid(row=0, column=1, sticky='w', pady=5)
            rating_star2 = tk.Radiobutton(information_entry_frame, variable = var, value = 2, text='2', highlightbackground='white')
            rating_star2.grid(row=0, column=2, sticky='w', pady=5)
            rating_star3 = tk.Radiobutton(information_entry_frame, variable = var, value = 3, text='3', highlightbackground='white')
            rating_star3.grid(row=0, column=3, sticky='w', pady=5)
            rating_star4 = tk.Radiobutton(information_entry_frame, variable = var, value = 4, text='4', highlightbackground='white')
            rating_star4.grid(row=0, column=4, sticky='w', pady=5)
            rating_star5 = tk.Radiobutton(information_entry_frame, variable = var, value = 5, text='5', highlightbackground='white')
            rating_star5.grid(row=0, column=5, sticky='w', pady=5)
            rating_text=StringVar()
            comment_label = tk.Label(information_entry_frame, text="Comment:", font=SMALL_FONT)
            comment_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
            # u022 is code for dot so that, the user's password is not visible
            comment_text = tk.Text(information_entry_frame, height = 5)
            comment_text.grid(row = 1, column = 1, columnspan = 5, sticky = 'w', pady = 5, padx = 5)
            #comment_entry = tk.Entry(information_entry_frame, show='\u2022')
            #comment_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
            create_review_button = tk.Button(self, text="Create Review", fg='blue',
                                     command=lambda: createreview(username_text, pwd_text))
            #register_button = tk.Button(self, borderwidth=0, text="New User? Click here to register",
            #                            font="Verdana 10 underline", fg='blue',
            #                            command=lambda: controller.show_frame(RegistrationPage))
            back_button = tk.Button(self, text="Back", fg='blue', command=lambda: controller.show_frame(MuseumReviewPage))
            create_review_button.pack(pady=5, anchor='n')
            back_button.pack(pady=5, anchor='n')
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack(anchor='n')
            #register_button.pack(pady=0, anchor='n')

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
