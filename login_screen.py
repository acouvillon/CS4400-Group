from tkinter import *
from tkinter import ttk

# Define a class to set up our GUI


class App(object):
    def __init__(self, login_screen):
        # Set the window title

        self.parent = login_screen

        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame')
        self.f1 = ttk.Frame(self.parent, style='My.TFrame', padding=(3, 3, 12, 12))  # added padding
        self.f1.grid(column=1, row=2, sticky=(N, S, E, W))  # added sticky
        title = Label(login_screen, text="BMTRS", font=("Verdana", 20)).grid(row=0, columnspan=5)
        self.email_label = ttk.Label(self.f1, text="Email:")
        self.email = ttk.Entry(self.f1)
        self.pwd_label = ttk.Label(self.f1, text="Password:")
        self.pwd = ttk.Entry(self.f1)

        login_screen.wm_title("")

        login_button = Button(self.f1, text="Login", fg='blue', width=20)
        registration_button = Button(self.f1, text="New User? Click here to register", font=("Verdana 8 underline"), fg='blue', borderwidth=0, relief='flat')


        self.f1.grid(column=1, row=2, sticky=(N, S, E, W))  # added sticky
        self.email_label.grid(column=5, row=2, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
        self.email.grid(column=6, row=2, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
        self.pwd_label.grid(column=5, row=3, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
        self.pwd.grid(column=6, row=3, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
        login_button.grid(column=6, row=5, pady=5)
        registration_button.grid(column=6, row=6, pady=5)

        # added resizing configs
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.f1.columnconfigure(0, weight=1)
        self.f1.columnconfigure(1, weight=1)
        self.f1.columnconfigure(2, weight=1)
        self.f1.columnconfigure(3, weight=1)
        self.f1.columnconfigure(4, weight=1)
        self.f1.rowconfigure(1, weight=1)






# In our main function, create the GUI and pass it to our App class d


def main():
    window= Tk()
    start= App(window)
    window.mainloop()

#  Run the main function


if __name__ == "__main__":
    main()
