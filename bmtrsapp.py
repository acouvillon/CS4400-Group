from tkinter import *
from tkinter import ttk
from tkinter import font


class BmtrsApp(object):
    def __init__ (self, home_screen):
        self.parent = home_screen
        create_login_page()
        home_screen.withdraw()

def create_login_page():
    login_page = Tk()
    f1 = ttk.Frame(login_page, style='My.TFrame', padding=(3, 3, 12, 12))  # added padding
    f1.grid(column=1, row=2, sticky=(N, S, E, W))  # added sticky
    title = Label(login_page, text="BMTRS", font=("Verdana", 20)).grid(row=0, columnspan=5)
    email_label = ttk.Label(f1, text="Email:")
    email = ttk.Entry(f1)
    email_text = StringVar()
    pwd_label = ttk.Label(f1, text="Password:")
    pwd = ttk.Entry(f1)
    pwd_text = StringVar()



    login_button = Button(f1, text="Login", fg='blue', width=20)
    create_new_user_button = Button(f1, text="New User? Click here to register",
                                    font="Verdana 8 underline", fg='blue', borderwidth=0, command=create_registration_page)

    f1.grid(column=1, row=2, sticky=(N, S, E, W))  # added sticky
    email_label.grid(column=5, row=2, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    email.grid(column=6, row=2, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    pwd_label.grid(column=5, row=3, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    pwd.grid(column=6, row=3, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    login_button.grid(column=6, row=9, pady=5)
    create_new_user_button.grid(column=6, row=10, pady=5)

    # added resizing configs
    login_page.columnconfigure(0, weight=1)
    login_page.rowconfigure(0, weight=1)
    f1.columnconfigure(0, weight=1)
    f1.columnconfigure(1, weight=1)
    f1.columnconfigure(2, weight=1)
    f1.columnconfigure(3, weight=1)
    f1.columnconfigure(4, weight=1)
    f1.columnconfigure(5, weight=1)
    f1.columnconfigure(6, weight=1)
    f1.columnconfigure(7, weight=1)
    f1.rowconfigure(1, weight=1)


    login_page.wm_title("")


def create_registration_page():
    registration_page = Tk()
    f1_style = ttk.Style()
    f1_style.configure('My.TFrame')
    f1 = ttk.Frame(registration_page, style='My.TFrame', padding=(3, 3, 12, 12))  # added padding
    f1.grid(column=1, row=2, sticky=(N, S, E, W))  # added sticky
    title = Label(registration_page, text="New User Registration", font=("Verdana", 20)).grid(row=0, columnspan=5)
    email_label = ttk.Label(f1, text="Email:")
    email = ttk.Entry(f1)
    email_text = StringVar()
    pwd_label = ttk.Label(f1, text="Password:")
    pwd = ttk.Entry(f1)
    pwd_text = StringVar()
    confirm_pwd_label = ttk.Label(f1, text="Confirm Password:")
    confirm_pwd = ttk.Entry(f1)
    confirm_pwd_text = StringVar()
    credit_card_num_label = ttk.Label(f1, text="Credit Card Number:")
    credit_card_num = ttk.Entry(f1)
    ccd_text = StringVar()
    exp_date_label = ttk.Label(f1, text="Credit Card Exp. Date:")
    exp_date = ttk.Entry(f1)
    exp_text = StringVar()
    security_code_label = ttk.Label(f1, text="Credit Card Security Code:")
    security_code = ttk.Entry(f1)
    sec_text = StringVar()



    create_account_button = Button(f1, text="Create Account", fg='blue', width=20)
    back_button = Button(f1, text="Back", fg='blue', width=20, command=lambda:[create_login_page,registration_page.withdraw])


    f1.grid(column=1, row=2, sticky=(N, S, E, W))  # added sticky
    email_label.grid(column=5, row=2, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    email.grid(column=6, row=2, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    pwd_label.grid(column=5, row=3, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    pwd.grid(column=6, row=3, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    confirm_pwd_label.grid(column=5, row=4, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    confirm_pwd.grid(column=6, row=4, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    credit_card_num_label.grid(column=5, row=5, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    credit_card_num.grid(column=6, row=5, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    exp_date_label.grid(column=5, row=6, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    exp_date.grid(column=6, row=6, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    security_code_label.grid(column=5, row=7, columnspan=1, sticky=(N, E), pady=5, padx=5)  # added sticky, padx
    security_code.grid(column=6, row=7, columnspan=1, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx
    create_account_button.grid(column=6, row=9, pady=5)
    back_button.grid(column=6, row=10, pady=5)

    # added resizing configs
    registration_page.columnconfigure(0, weight=1)
    registration_page.rowconfigure(0, weight=1)
    f1.columnconfigure(0, weight=1)
    f1.columnconfigure(1, weight=1)
    f1.columnconfigure(2, weight=1)
    f1.columnconfigure(3, weight=1)
    f1.columnconfigure(4, weight=1)
    f1.columnconfigure(5, weight=1)
    f1.columnconfigure(6, weight=1)
    f1.columnconfigure(7, weight=1)
    f1.rowconfigure(1, weight=1)
    registration_page.rowconfigure(2, weight=1)
    registration_page.rowconfigure(3, weight=1)
    registration_page.rowconfigure(4, weight=1)
    registration_page.rowconfigure(5, weight=1)
    registration_page.rowconfigure(6, weight=1)
    registration_page.rowconfigure(7, weight=1)
    registration_page.rowconfigure(8, weight=1)

    registration_page.wm_title("")

def main():
    home_screen= Tk()
    start= BmtrsApp(home_screen)
    home_screen.mainloop()
#  Run the main function

if __name__ == "__main__":
    main()
