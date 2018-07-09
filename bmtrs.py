from tkinter import *

# Define a class to set up our GUI


class App(object):
    def __init__(self, login_screen):
        # Set the window title
        login_screen.wm_title("BMTRS Application")
        email_label = Label(login_screen, text ="Email: ")
        pwd_label = Label(login_screen, text ="Password: ")
        email_entry = Entry(login_screen)
        pwd_entry = Entry(login_screen)
        # sticky = E makes sure it sticks to right end of the cell in the grid
        email_label.grid(row=0, sticky=E)
        email_entry.grid(row=0, column=1)
        pwd_label.grid(row=1, sticky=E)
        pwd_entry.grid(row=1, column=1)
        login_button = Button(login_screen, text='Login', fg='blue')
        # event = left mouse click
        # function = open home screen
        login_button.bind("<Button-1>", login_screen)
        login_button.grid(columnspan=2)

# In our main function, create the GUI and pass it to our App class d


def main():
    window= Tk()
    start= App(window)
    window.mainloop()

#  Run the main function


if __name__ == "__main__":
    main()
