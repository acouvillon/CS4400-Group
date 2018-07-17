import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector

LARGE_FONT = ("Verdana", 26, "underline")
SMALL_FONT = ("Verdana", 10, "italic")
config = {
    'user': 'root',
    'password': 'rootuserpassword',
    'database': 'bmtrsdb',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)



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
        for F in {LoginPage, RegistrationPage, SearchForMuseumPage}:
            login_frame = F(main_window, self)
            self.frames[F] = login_frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            login_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()



#PAGE 1 - LOGIN PAGE
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="BMTRS", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        information_entry_frame = tk.Frame(self, borderwidth=5, relief='groove', pady=10)
        information_entry_frame.pack(anchor='center', pady=20, padx=5)
        email_label = tk.Label(information_entry_frame, text="Email:", font=SMALL_FONT)
        email_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        email_text = StringVar()
        email_entry = tk.Entry(information_entry_frame, textvariable=email_text)
        email_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        pwd_label = tk.Label(information_entry_frame, text="Password:", font=SMALL_FONT)
        pwd_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
        # u022 is code for dot so that, the user's password is not visible
        pwd_text = StringVar()
        pwd_entry = tk.Entry(information_entry_frame, show='\u2022', textvariable=pwd_text)
        pwd_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        login_button = tk.Button(self, text="Login", fg='blue',
                                 command=lambda: self.login(email_text, pwd_text, controller))
        register_button = tk.Button(self, borderwidth=0, text="New User? Click here to register",
                                    font="Verdana 10 underline", fg='blue',
                                    command=lambda: controller.show_frame(RegistrationPage))
        login_button.pack(anchor='n', expand=True)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n')
        register_button.pack(pady=0, anchor='n')


    # Checks database, validates credentials and allows access to specific museum page
    def login(self, username, pwd, controller):

        if len(username.get()) == 0 or len(pwd.get())==0:
            messagebox.showerror("Error","Cannot leave either field blank")
            return

        cursor = cnx.cursor()
        query = ("SELECT COUNT(*) FROM visitor "
                 "WHERE email = '{username}' AND password = '{password}';").format(username=username.get(), password=pwd.get())
        cursor.execute(query)
        count = cursor.fetchone()[0]
        if count == 0:
            query = ("SELECT COUNT(*) FROM admin_user "
                     "WHERE email = '{username}' AND password = '{password}';").format(username=username.get(), password=pwd.get())
            cursor.execute(query)
            admin_count = cursor.fetchone()[0]
            if admin_count == 0:
                messagebox.showerror("Error","Either username or password is incorrect")
            else:
                # todo - display admin home screen
                print("admin logged in")
        else:
            # todo - display choose museums page
            controller.show_frame(SearchForMuseumPage)
            print("visitor logged in")

class SearchForMuseumPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Welcome ", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        museum_select_frame = tk.Frame(self, borderwidth=5, relief='groove')
        museum_select_frame.pack(anchor='center', pady=20, padx=5)

        museums = StringVar()
        museums.set('Picasso Museum') # set the default option

        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        museum_list = []
        for (museum_name) in cursor:
            museum_list.append(museum_name)
        cursor.close()

        pickAMuseum = tk.Label(museum_select_frame, text="Pick a Museum: ")
        popupMenu = tk.OptionMenu(museum_select_frame, museums, *museum_list)
        pickAMuseum.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)

        # on change dropdown value
        def change_dropdown(*args):
            print(museums.get())

        # link function to change dropdown
        museums.trace('w', change_dropdown)

        view_all_museums_button = tk.Button(self, text="View All Museums", fg='blue')
        # todo - command=lambda: controller.show_frame(ViewAllMuseumsPage)

        my_tickets_button = tk.Button(self, borderwidth=0, text="My Tickets", fg='blue')
        # todo - command=lambda: controller.show_frame(MyTicketsPage)

        my_reviews_button = tk.Button(self, borderwidth=0, text="My Reviews", fg='blue')
        # todo - command=lambda: controller.show_frame(MyReviewsPage)

        manage_account_button = tk.Button(self, borderwidth=0, text="Manage Account", fg='blue')
        # todo - command=lambda: controller.show_frame(ManageAccountPage)

        view_all_museums_button.pack(anchor='n', expand=True)
        my_tickets_button.pack(pady=0, anchor='n')
        my_reviews_button.pack(pady=0, anchor='n')
        manage_account_button.pack(pady=0, anchor='n')

class RegistrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="New User Registration", font=LARGE_FONT)
        title.pack(anchor='center')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)

        information_entry_frame = tk.Frame(self, borderwidth=5, relief='groove')
        information_entry_frame.pack(anchor='center', pady=20, padx=5)

        email_label = tk.Label(information_entry_frame, text="Email:", font=SMALL_FONT)
        email_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        email_text=StringVar()
        email_entry = tk.Entry(information_entry_frame, textvariable=email_text)
        email_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)


        pwd_label = tk.Label(information_entry_frame, text="Password:", font=SMALL_FONT)
        pwd_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
        pwd_text = StringVar()
        pwd_entry = tk.Entry(information_entry_frame, show="\u2022", textvariable=pwd_text)
        pwd_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        confirm_label = tk.Label(information_entry_frame, text="Confirm Password:", font=SMALL_FONT)
        confirm_label.grid(row=2, column=0, sticky='e', pady=5, padx=5)
        confirm_text=StringVar()
        confirm_entry = tk.Entry(information_entry_frame, show="\u2022", textvariable=confirm_text)
        confirm_entry.grid(row=2, column=1, sticky='w', pady=5, padx=5)

        #todo - check if confirm text matches password text
        credit_card = tk.Label(information_entry_frame, text="Credit Card Number:", font=SMALL_FONT)
        credit_card.grid(row=3, column=0, sticky='e', pady=5, padx=5)
        credit_card_text = StringVar()
        credit_card_entry = tk.Entry(information_entry_frame, textvariable=credit_card_text)
        credit_card_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        #todo - credit card entry formatting as .... .... .... 3333
        credit_card_text.trace("w", lambda name, index, mode, credit_card_text=credit_card_text: entryFormattingForCreditCardNumber(credit_card_entry))

        exp_date = tk.Label(information_entry_frame, text="Credit Card Exp. Date:", font=SMALL_FONT)
        exp_date.grid(row=4, column=0, sticky='e', pady=5, padx=5)
        exp_date_text= StringVar()
        #todo - format entry as mm/yy
        exp_date_entry = tk.Entry(information_entry_frame, textvariable=exp_date_text)
        exp_date_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)

        security_code = tk.Label(information_entry_frame, text="Credit Card Security Code:", font=SMALL_FONT)
        security_code.grid(row=4, column=0, sticky='e', pady=5, padx=5)
        sec_code_text = StringVar()
        #todo - format entry as 3 digit entry only
        security_code_entry = tk.Entry(information_entry_frame, textvariable=sec_code_text)
        security_code_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)
        create_account_button = tk.Button(self, text="Create Account", fg='blue',
                                          command=lambda: create_account(email_text, pwd_text, credit_card_text, exp_date_text, sec_code_text))
        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: controller.show_frame(LoginPage))
        create_account_button.pack(pady=5, anchor='n')
        back_button.pack(pady=5, anchor='n')

#todo - implement this function
def create_account(email, pwd, credit_card_num, exp_date, security_code):
    print('account created')

def entryFormattingForCreditCardNumber(entry):
    text = entry.get()
    if len(text) % 4 == 0:
        entry.insert(SEPARATOR, ' ')
        entry.icursor(len(text)+1)



app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
