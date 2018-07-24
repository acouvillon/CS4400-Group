from __future__ import print_function
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import mysql.connector
from mysql.connector import errorcode
import datetime


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
        self.wm_title("BMTRS")

        #fill fills space allotted
        #expand beyond space allotted
        main_window.pack(side="top", fill="both", expand=True)
        #0 - minimum,
        main_window.grid_rowconfigure(0, weight=1)
        main_window.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in {LoginPage, RegistrationPage, SearchForMuseumPage,
                  ViewMuseumsPage, TicketHistoryPage, ReviewHistoryPage,
                  ViewSpecificMuseumPage, ManageAccountPage, MuseumReviewPage,
                  ViewAllMuseumReviewsPage, CuratorRequestPage, CuratorSearchForMuseumPage,
                  CuratorViewSpecificMuseumPage, MyMuseumsPage, NewExhibitPage,
                  AdminHomePage, AdminCuratorRequestsPage, DeleteMuseumFormPage, NewMuseumPage}:
            frame = F(main_window, self)
            self.frames[F] = frame
            #sticky alignment + stretch - so it aligns everything to all sides of window
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


#PAGE 1 - LOGIN PAGE
class LoginPage(tk.Frame):

    user = ''
    textboxes = None
    isCurator = False
    def __init__(self, parent, controller):
        self.controller = controller
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
        self.textboxes = (email_entry, pwd_entry)
        login_button = tk.Button(self, text="Login", fg='blue',
                                 command=lambda: self.login(email_text, pwd_text, controller))
        register_button = tk.Button(self, borderwidth=0, text="New User? Click here to register",
                                    font="Verdana 10 underline", fg='blue',
                                    command=lambda: controller.show_frame(RegistrationPage))
        login_button.pack(anchor='n', expand=True)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n')

        register_button.pack(pady=10, anchor='n')


    # Checks database, validates credentials and allows access to specific museum page
    def login(self, username, pwd, controller):

        if len(username.get()) == 0 or len(pwd.get())==0:
            messagebox.showerror("Error","Cannot leave either field blank")
            return

        cursor = cnx.cursor()
        q = ("SELECT COUNT(*) FROM visitor "
             "WHERE email = %s;")

        cursor.execute(q, (username.get(),))
        c = cursor.fetchone()[0]
        qu = ("SELECT COUNT(*) FROM admin_user "
              "WHERE email = %s;")
        cursor.execute(qu, (username.get(),))
        admin_count = cursor.fetchone()[0]
        if c == 0 and admin_count == 0:
            messagebox.showerror("Error", "User with that email does not exist.")
            return

        query = ("SELECT COUNT(*) FROM visitor "
                 "WHERE email = %s AND password = %s;")
        values = (username.get(), pwd.get())
        cursor.execute(query, values)
        count = cursor.fetchone()[0]
        if count == 0:
            query = ("SELECT COUNT(*) FROM admin_user "
                     "WHERE email = %s AND password = %s;")
            cursor.execute(query, values)
            admin_count = cursor.fetchone()[0]
            if admin_count == 0:
                messagebox.showerror("Error","Either username or password is incorrect")
            else:
                controller.show_frame(AdminHomePage)
                print("admin logged in")
        else:
            user = username.get()
            self.user = user
            query = ("SELECT COUNT(*) FROM museum "
                     "WHERE curator_email = %s;")
            cursor.execute(query, (user, ))
            curator_count = cursor.fetchone()[0]

            if curator_count != 0:
                next_page = self.controller.get_page(CuratorSearchForMuseumPage)
                next_page.update_museum_list()
                self.isCurator = True
                view = CuratorSearchForMuseumPage
            else:
                next_page = self.controller.get_page(SearchForMuseumPage)
                # next_page.update_museum_list()
                self.isCurator = False
                view = SearchForMuseumPage
            next_page.title['text'] = "Welcome, " + user
            next_page.user = user
            controller.show_frame(view)
            print(user + "user logged in")


class CuratorSearchForMuseumPage(tk.Frame):

    user = ''
    chosen_museum = ''
    museums = None
    popupMenu = None
    museum_select_frame = None
    museum_list = []
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.title = tk.Label(self, text="Welcome, ", font=LARGE_FONT)
        self.title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        self.museum_select_frame = tk.Frame(self, borderwidth=5, relief='groove')
        self.museum_select_frame.pack(anchor='center', pady=20, padx=20, ipadx=20)

        self.update_museum_list()

        pickAMuseum = tk.Label(self.museum_select_frame, text="Pick a Museum: ")
        pickAMuseum.grid(row=0, column=0, sticky='e', pady=5, padx=5)

        view_all_museums_button = tk.Button(self, text="View All Museums", fg='blue', command=lambda: show_museums_page())

        my_tickets_button = tk.Button(self, text="My Tickets", fg='blue', command=lambda: show_ticket_page())

        my_reviews_button = tk.Button(self, text="My Reviews", fg='blue', command=lambda: show_reviews_page())

        my_museums_button = tk.Button(self, text="My Museums", fg='blue',
                                      command=lambda: show_my_museums_page())
        manage_account_button = tk.Button(self, text="Manage Account", fg='blue', command=lambda: controller.show_frame(ManageAccountPage))

        view_all_museums_button.pack(pady=20, anchor='n')
        my_tickets_button.pack(pady=5, anchor='n')
        my_reviews_button.pack(pady=5, anchor='n')
        my_museums_button.pack(pady=5, anchor='n')
        manage_account_button.pack(pady=5, anchor='n')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

        def show_ticket_page():
            self.controller.get_page(TicketHistoryPage).populateTable(self.user)
            self.controller.show_frame(TicketHistoryPage)

        def show_reviews_page():
            self.controller.get_page(ReviewHistoryPage).populateTable(self.user)
            self.controller.show_frame(ReviewHistoryPage)

        def show_museums_page():
            self.controller.get_page(ViewMuseumsPage).sql_query()
            self.controller.show_frame(ViewMuseumsPage)

        def show_my_museums_page():
            self.controller.get_page(MyMuseumsPage).populateTable(self.user)
            self.controller.show_frame(MyMuseumsPage)

    def update_museum_list(self):

        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        self.museum_list = cursor.fetchall()
        museum_names = []
        for i in range(0, len(self.museum_list)):
            museum_names.append(self.museum_list[i][0])
            i += 1
        self.museums = StringVar()
        self.museums.set(museum_names[0]) # set the default option

        if self.popupMenu != None:
            self.popupMenu.destroy()
        self.popupMenu = tk.OptionMenu(self.museum_select_frame, self.museums, *museum_names)
        self.popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        cursor.close()

        # on change dropdown value
        def change_dropdown(*args):
            if self.controller.get_page(LoginPage).isCurator:
                museum_page = self.controller.get_page(CuratorViewSpecificMuseumPage)
                museum_page.populateTable(self.museums.get())
                self.controller.show_frame(CuratorViewSpecificMuseumPage)
            else:
                museum_page = self.controller.get_page(ViewSpecificMuseumPage)
                museum_page.populateTable(self.museums.get())
                self.controller.show_frame(ViewSpecificMuseumPage)

        # link function to change dropdown
        self.museums.trace('w', change_dropdown)

class RegistrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="New User Registration", font=LARGE_FONT)
        title.pack(anchor='center')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)

        information_entry_frame = tk.Frame(self, height=200, width=500, borderwidth=5, relief='groove')
        information_entry_frame.pack(anchor='center', pady=20, padx=5)

        email_label = tk.Label(information_entry_frame, text="Email:", font=SMALL_FONT)
        email_label.grid(row=0, column=0, sticky='e', pady=10, padx=10)
        email_text=StringVar()
        email_entry = tk.Entry(information_entry_frame, textvariable=email_text)
        email_entry.grid(row=0, column=1, sticky='w', pady=10, padx=10)


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


        credit_card = tk.Label(information_entry_frame, text="Credit Card Number:", font=SMALL_FONT)
        credit_card.grid(row=3, column=0, sticky='e', pady=5, padx=5)
        credit_card_text = StringVar()
        credit_card_entry = tk.Entry(information_entry_frame, textvariable=credit_card_text)
        credit_card_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)

        exp_date = tk.Label(information_entry_frame, text="Credit Card Exp. Date (mm/yy):", font=SMALL_FONT)
        exp_date.grid(row=4, column=0, sticky='e', pady=5, padx=5)
        exp_date_text= StringVar()

        exp_date_entry = tk.Entry(information_entry_frame, textvariable=exp_date_text)
        exp_date_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)

        security_code = tk.Label(information_entry_frame, text="Credit Card Security Code:", font=SMALL_FONT)
        security_code.grid(row=5, column=0, sticky='e', pady=5, padx=5)
        sec_code_text = StringVar()

        security_code_entry = tk.Entry(information_entry_frame, textvariable=sec_code_text)
        security_code_entry.grid(row=5, column=1, sticky='w', pady=5, padx=5)

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)
        create_account_button = tk.Button(self, text="Create Account", fg='blue',
                                          command=lambda: create_account(email_text, pwd_text, confirm_text, credit_card_text, exp_date_text, sec_code_text, controller))
        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: controller.show_frame(LoginPage))
        create_account_button.pack(pady=5, anchor='n')
        back_button.pack(pady=5, anchor='n')


def create_account(email, pwd, conf_pwd, credit_card_num, exp_date, security_code, controller):
    cursor = cnx.cursor()

    date = exp_date.get()
    month = date[:2]
    year = date[3:]

    if len(email.get())==0 or len(pwd.get())==0 or len(conf_pwd.get()) == 0 or len(credit_card_num.get())==0 or len(exp_date.get())==0 or len(security_code.get())==0:
        messagebox.showerror("Error","All fields required")
        return

    if pwd.get() != conf_pwd.get():
        messagebox.showerror("Error", "Passwords don't match")
        return

    if len(date) != 5 or date[2]!='/':
        messagebox.showerror("Error","Invalid expiration date format")
        return

    if not year.isdigit() or not month.isdigit() or not credit_card_num.get().isdigit() or not security_code.get().isdigit():
        messagebox.showerror("Error", "Date, credit card and Security number must be numbers")
        return

    year = int(year)
    month = int(month)

    if month > 12 or month < 1:
        messagebox.showerror("Error", "Month is invalid")
        return

    if year < 18 and month < 7:
        messagebox.showerror("Error", "Card expired. Please use a different card")
        return

    if len(credit_card_num.get()) != 16 or not credit_card_num.get().isdigit():
        messagebox.showerror("Error", "Credit card invalid")
        return

    query = ("""INSERT INTO visitor (email, password, credit_card_num,
            expiration_month, expiration_year, credit_card_security_num)
            VALUES (%s, %s, %s, %s, %s, %s)""")
    values = (email.get(), pwd.get(), credit_card_num.get(), month, year, security_code.get())

    # cursor.execute(query, values)
    # cnx.commit()
    # controller.show_frame(LoginPage)

    try:
        cursor.execute(query, values)
        cnx.commit()
        controller.show_frame(LoginPage)
    except:
        messagebox.showerror("Error","Account already exists.")
    cursor.close()


class ViewMuseumsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="All Museums", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('rating')
        self.tree.column('rating', width=100, anchor='ne')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('rating', text='Average Rating')
        self.tree.pack()
        select_button = tk.Button(self, text="Select", fg='blue', command=lambda: self.select_press(self.tree, controller))
        select_button.pack(pady=5, anchor='n')

        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: self.choose_view())
        back_button.pack(padx=50, pady=10, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    def sql_query(self):

        self.tree.delete(*self.tree.get_children())

        cursor = cnx.cursor()

        query = ("SELECT museum_name, AVG(rating) FROM museum "
                 " NATURAL LEFT OUTER JOIN review GROUP BY museum_name")

        cursor.execute(query)

        museum_list = []
        review_list = []

        for (museum_name, review) in cursor:
            museum_list.append(museum_name)
            review_list.append(review)

        cursor.close()

        num = 0

        for museum in museum_list:
            if (review_list[num] != None):
                self.tree.insert('', 'end', text=museum, values=(str(review_list[num])[0:3] + '/5'))
            else:
                self.tree.insert('', 'end', text=museum, values=('-'))
            num+=1


    def select_press(self, tree, controller):
        curItem = tree.focus()
        museum = tree.item(curItem)['text']
        #Use this for the sql for the next page
        if museum != '':
            if self.controller.get_page(LoginPage).isCurator:
                museum_page = controller.get_page(CuratorViewSpecificMuseumPage)
                museum_page.populateTable(museum)
                controller.show_frame(CuratorViewSpecificMuseumPage)
            else:
                museum_page = controller.get_page(ViewSpecificMuseumPage)
                museum_page.populateTable(museum)
                controller.show_frame(ViewSpecificMuseumPage)


class TicketHistoryPage(tk.Frame):

    museum_list = []
    time_list = []
    price_list = []

    tree = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="My Tickets", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('date', 'price')
        self.tree.column('date', width=100, anchor='center')
        self.tree.column('price', width=100, anchor='e')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('date', text='Purchase Date')
        self.tree.heading('price', text='Price')
        self.tree.pack()
        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: self.choose_view())
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)
        #self.populateTable('helen@gatech.edu')

    #must be called from user login page at login
    def populateTable(self, username):
        self.tree.delete(*self.tree.get_children())
        num = 0
        self.sqlQuery(username)
        for museum in self.museum_list:
            self.tree.insert('', 'end', text=museum, values=(self.time_list[num].strftime('%m/%d/%Y'), '$'+self.price_list[num]))
            num+=1

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    def sqlQuery(self, username):

        self.museum_list = []
        self.time_list = []
        self.price_list = []

        cursor = cnx.cursor()

        query = ("""SELECT museum_name, purchase_timestamp, price
                    FROM ticket 
                    WHERE email = %s""")

        cursor.execute(query, (username, ))


        for (museum_name, time, price) in cursor:
            self.museum_list.append(museum_name)
            self.time_list.append(time)
            self.price_list.append(price)


        cursor.close()

#PAGE 9 - MY REVIEWS page
class ReviewHistoryPage(tk.Frame):

    museum_list = []
    review_list = []
    rating_list = []

    tree = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="My Reviews", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('review', 'rating')
        self.tree.column('#0', width=150, anchor='center')
        self.tree.column('review', width=300, anchor='center')
        self.tree.column('rating', width=50, anchor='e')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('review', text='Review')
        self.tree.heading('rating', text='Rating')
        self.tree.pack()
        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: self.choose_view())
        back_button.pack(padx=50, pady=20, anchor='w')
        # self.populateTable('helen@gatech.edu')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    #must be called from user login page at login
    def populateTable(self, username):
        self.tree.delete(*self.tree.get_children())
        num = 0
        self.sqlQuery(username)
        for museum in self.museum_list:
            self.tree.insert('', 'end', text=museum, values=(self.review_list[num], str(self.rating_list[num])+'/5'))
            num+=1

    def sqlQuery(self, username):

        self.museum_list = []
        self.review_list = []
        self.rating_list = []

        cursor = cnx.cursor()

        query = ("""SELECT museum_name, comment, rating
                    FROM review 
                    WHERE email = %s""")

        cursor.execute(query, (username, ))

        for (museum_name, review, rating) in cursor:
            self.museum_list.append(museum_name)
            self.review_list.append(review)
            self.rating_list.append(rating)

        cursor.close()


class ViewSpecificMuseumPage(tk.Frame):

    tree = None
    title = None

    exhibit_list = []
    year_list = []
    link_list = []
    museum = ''
    price = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = tk.Label(self, text="[INSERT MUSEUM NAME HERE]", font=LARGE_FONT)
        self.title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)

        self.controller = controller

        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('year','url')
        self.tree.column('#0', width=200, anchor='w')
        self.tree.column('year', width=50, anchor='center')
        self.tree.column('url', width=200, anchor='e')
        self.tree.heading('#0', text='Exhibit')
        self.tree.heading('year', text='Year')
        self.tree.heading('url', text='Link to Exhibit (Double Click)')
        self.tree.bind("<Double-Button-1>", self.link_tree)
        self.tree.pack()

        purchase_ticket_button = tk.Button(self, text="Purchase Ticket", fg='blue',
                                           command=lambda: self.purchase_ticket())
        review_museum_button = tk.Button(self, text="Review Museum", fg='blue',
                                         command=lambda: self.create_review())
        view_other_reviews_button = tk.Button(self, text="View Others' Reviews", fg='blue',
                                              command=lambda: self.show_all_reviews())
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: self.choose_view())

        purchase_ticket_button.pack(anchor='n', expand=True)
        review_museum_button.pack(pady=5, anchor='n')
        view_other_reviews_button.pack(pady=5, anchor='n')
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    #must be called from previous page
    def populateTable(self, museum):
        self.tree.delete(*self.tree.get_children())

        num = 0
        self.title['text'] = museum
        self.museum = museum
        self.sqlQuery(museum)
        for exhibit in self.exhibit_list:
            self.tree.insert('', 'end', text=exhibit, values=(self.year_list[num], self.link_list[num]))
            num+=1

    def sqlQuery(self, museum_name):
        self.tree.delete(*self.tree.get_children())
        self.exhibit_list = []
        self.year_list = []
        self.link_list = []

        cursor = cnx.cursor()

        query = ("""SELECT exhibit_name, year, url
                    FROM exhibit
                    WHERE museum_name = %s""")

        cursor.execute(query, (museum_name, ))

        for (exhibit, year, link) in cursor:
            self.exhibit_list.append(exhibit)
            self.year_list.append(year)
            self.link_list.append(link)

        query2 = ("""SELECT ticket_price
                    FROM museum
                    WHERE museum_name = %s""")

        cursor.execute(query2, (museum_name, ))

        for (price) in cursor:
            self.title['text'] += ' - $' + price[0]
            self.price = price[0]


        cursor.close()

    def purchase_ticket(self):

        user = self.controller.get_page(LoginPage).user

        cursor = cnx.cursor()

        query = ("""INSERT INTO ticket (email, museum_name, price, purchase_timestamp)
            VALUES (%s, %s, %s, %s)""")
        values = (user, self.museum, self.price, datetime.datetime.now())

        try:
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
        except:
            messagebox.showinfo("Purchase declined", "You already own a ticket for the {}.".format(self.museum))
            cursor.close()
            return


        messagebox.showinfo("Purchase accepted", "Thank you for purchasing a ticket for the {}! Please check your email for more info.".format(self.museum))

    def create_review(self):

        user = self.controller.get_page(LoginPage).user

        cursor = cnx.cursor()

        ticket_query = ("""SELECT *
                    FROM ticket
                    WHERE email = %s AND museum_name = %s""")
        values = (user, self.museum)
        cursor.execute(ticket_query, values)

        if cursor.fetchone() == None:
            messagebox.showerror("Error","You cannot leave a review without purchasing a ticket for this museum first.")
            cursor.close()
            return

        review_query = ("""SELECT comment, rating
                        FROM review
                        WHERE email = %s AND museum_name = %s""")
        values = (user, self.museum)
        cursor.execute(review_query, values)

        if cursor.fetchone() != None:
            # messagebox.showerror("Error","You have already left a review for this museum.")
            next_page = self.controller.get_page(MuseumReviewPage)
            next_page.comment.delete('1.0',END)
            cursor.execute(review_query, values)
            for (comment, rating) in cursor:
                print(comment)
                next_page.comment.insert(END, comment)
                next_page.rating.set(rating)
            cursor.close()
        else:
            cursor.close()

            next_page = self.controller.get_page(MuseumReviewPage)

            next_page.comment.delete('1.0',END)
            next_page.rating.set(None)

        self.controller.show_frame(MuseumReviewPage)

    def show_all_reviews(self):
        self.controller.get_page(ViewAllMuseumReviewsPage).populateTable(self.museum)
        self.controller.show_frame(ViewAllMuseumReviewsPage)

    def link_tree(self,event):
        cur_item = self.tree.focus()
        url = self.tree.item(cur_item)['values'][1]

        import webbrowser
        webbrowser.open('{}'.format(url))

class CuratorViewSpecificMuseumPage(tk.Frame):

    tree = None
    title = None

    exhibit_list = []
    year_list = []
    link_list = []
    museum = ''
    price = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = tk.Label(self, text="[INSERT MUSEUM NAME HERE]", font=LARGE_FONT)
        self.title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)

        self.controller = controller

        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('year','url')
        self.tree.column('#0', width=200, anchor='w')
        self.tree.column('year', width=50, anchor='center')
        self.tree.column('url', width=200, anchor='e')
        self.tree.heading('#0', text='Exhibit')
        self.tree.heading('year', text='Year')
        self.tree.heading('url', text='Link to Exhibit (Double Click)')
        self.tree.bind("<Double-Button-1>", self.link_tree)
        self.tree.pack()

        purchase_ticket_button = tk.Button(self, text="Purchase Ticket", fg='blue',
                                           command=lambda: self.purchase_ticket())
        review_museum_button = tk.Button(self, text="Review Museum", fg='blue',
                                         command=lambda: self.create_review())
        view_other_reviews_button = tk.Button(self, text="View Others' Reviews", fg='blue',
                                              command=lambda: self.show_all_reviews())

        add_exhibit_button = tk.Button(self, text="Add Exhibit", fg='blue',
                                       command=lambda: self.add_exhibit())
        remove_exhibit_button = tk.Button(self, text="Remove Exhibit", fg='blue',
                                          command=lambda: self.remove_exhibit(self.tree))
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: self.choose_view())

        purchase_ticket_button.pack(anchor='n', expand=True)
        review_museum_button.pack(pady=5, anchor='n')
        view_other_reviews_button.pack(pady=5, anchor='n')
        add_exhibit_button.pack(pady=5, anchor='n', expand=True)
        remove_exhibit_button.pack(pady=5, anchor='n', expand=True)
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    #must be called from previous page
    def populateTable(self, museum):
        self.tree.delete(*self.tree.get_children())

        num = 0
        self.title['text'] = museum
        self.museum = museum
        self.sqlQuery(museum)
        for exhibit in self.exhibit_list:
            self.tree.insert('', 'end', text=exhibit, values=(self.year_list[num], self.link_list[num]))
            num+=1

    def sqlQuery(self, museum_name):
        self.tree.delete(*self.tree.get_children())

        cursor = cnx.cursor()

        query = ("""SELECT exhibit_name, year, url
                    FROM exhibit
                    WHERE museum_name = %s""")

        cursor.execute(query, (museum_name, ))
        self.exhibit_list = []
        self.year_list = []
        self.link_list = []

        for (exhibit, year, link) in cursor:
            self.exhibit_list.append(exhibit)
            self.year_list.append(year)
            self.link_list.append(link)

        query2 = ("""SELECT ticket_price
                    FROM museum
                    WHERE museum_name = %s""")

        cursor.execute(query2, (museum_name, ))

        for (price) in cursor:
            self.title['text'] += ' - $' + price[0]
            self.price = price[0]


        cursor.close()

    def purchase_ticket(self):

        user = self.controller.get_page(LoginPage).user

        cursor = cnx.cursor()

        query = ("""INSERT INTO ticket (email, museum_name, price, purchase_timestamp)
            VALUES (%s, %s, %s, %s)""")
        values = (user, self.museum, self.price, datetime.datetime.now())

        try:
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
        except:
            messagebox.showinfo("Purchase declined", "You already own a ticket for the {}.".format(self.museum))
            cursor.close()
            return


        messagebox.showinfo("Purchase accepted", "Thank you for purchasing a ticket for the {}! Please check your email for more info.".format(self.museum))

    def create_review(self):

        user = self.controller.get_page(LoginPage).user

        cursor = cnx.cursor()

        ticket_query = ("""SELECT *
                    FROM ticket
                    WHERE email = %s AND museum_name = %s""")
        values = (user, self.museum)
        cursor.execute(ticket_query, values)

        if cursor.fetchone() == None:
            messagebox.showerror("Error","You cannot leave a review without purchasing a ticket for this museum first.")
            cursor.close()
            return

        review_query = ("""SELECT comment, rating
                        FROM review
                        WHERE email = '{}' AND museum_name = '{}'""".format(user, self.museum))
        cursor.execute(review_query)

        if cursor.fetchone() != None:
            # messagebox.showerror("Error","You have already left a review for this museum.")
            next_page = self.controller.get_page(MuseumReviewPage)
            next_page.comment.delete('1.0',END)
            cursor.execute(review_query)
            for (comment, rating) in cursor:
                print(comment)
                next_page.comment.insert(END, comment)
                next_page.rating.set(rating)
            cursor.close()

        else:
            cursor.close()

            next_page = self.controller.get_page(MuseumReviewPage)

            next_page.comment.delete('1.0',END)
            next_page.rating.set(None)

        self.controller.show_frame(MuseumReviewPage)

    def show_all_reviews(self):
        self.controller.get_page(ViewAllMuseumReviewsPage).populateTable(self.museum)
        self.controller.show_frame(ViewAllMuseumReviewsPage)

    def link_tree(self,event):
        cur_item = self.tree.focus()
        url = self.tree.item(cur_item)['values'][1]

        import webbrowser
        webbrowser.open('{}'.format(url))

    def add_exhibit(self):
        cursor = cnx.cursor()
        user = self.controller.get_page(LoginPage).user
        #TODO - START FIXING FROM HERE
        q = ("SELECT COUNT(*) FROM museum "
             "WHERE curator_email = '{email}' AND museum_name = '{mus}';").format(email=user, mus=self.museum)
        cursor.execute(q)
        count = cursor.fetchone()[0]

        if count == 0:
            messagebox.showinfo("Exhibit Cannot be Added", "You are not a curator for the {museum}. "
                                                           "You can only add an exhibit to a museum you are a curator for.".format(museum=self.museum))
            return
        self.controller.get_page(NewExhibitPage).get_info(self.museum, user)
        self.controller.show_frame(NewExhibitPage)

    def remove_exhibit(self, tree):
        curItem = tree.focus()
        exhibit = tree.item(curItem)['text']
        print(exhibit)
        if exhibit == '':
            return
        cursor = cnx.cursor()
        user = self.controller.get_page(LoginPage).user
        q = ("SELECT COUNT(*) FROM museum "
             "WHERE curator_email = '{email}' AND museum_name = '{mus}';").format(email=user, mus=self.museum)
        cursor.execute(q)
        count = cursor.fetchone()[0]

        if count == 0:
            messagebox.showinfo("Exhibit Cannot be Added", "You are not a curator for the {museum}. "
                                                           "You can only remove an exhibit to a museum you are a curator for.".format(museum=self.museum))
            return

        delete_q = ("""DELETE FROM exhibit
                      WHERE exhibit_name = %s""")

        values = (exhibit,)

        cursor.execute(delete_q, values)
        cnx.commit()
        cursor.close()
        self.populateTable(self.museum)

class ManageAccountPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Manage Account", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()

        log_out_button = tk.Button(self, text="Log Out", fg='blue',
                                   command=lambda: self.logout(controller))
        curator_request_button = tk.Button(self, text="Curator Request", fg='blue',
                                           command=lambda: self.show_curator_request())
        delete_account_button = tk.Button(self, text="Delete Account", fg='blue',
                                          command=lambda: self.delete_account(controller))
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: self.choose_view())

        log_out_button.pack(pady=20, anchor='n')
        curator_request_button.pack(pady=5, anchor='n')
        delete_account_button.pack(pady=5, anchor='n')
        back_button.pack(padx=50, pady=20, anchor='w')

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    def logout(self, controller):
        login_page = controller.get_page(LoginPage)
        textboxes = login_page.textboxes

        textboxes[0].focus_set()

        for textbox in textboxes:
            textbox.delete(0,END)

        controller.show_frame(LoginPage)

    def show_curator_request(self):
        page = self.controller.get_page(CuratorRequestPage)
        page.sql_request()
        self.controller.show_frame(CuratorRequestPage)


    def delete_account(self, controller):
        user = controller.get_page(LoginPage).user
        result = messagebox.askquestion("Delete Account", "Deleting your account will get rid of all of your reviews,"
                                                          "ticket history, and credit card information. Do you still wish to proceed?", icon='warning')
        if result == 'yes':

            cursor = cnx.cursor()

            query = ("""DELETE from visitor
                        WHERE email = '{0}'""".format(user))

            cursor.execute(query)
            cnx.commit()
            cursor.close()

            self.logout(controller)
            messagebox.showinfo("Account Deleted", "Account deleted.")

class MuseumReviewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Create A Review", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        information_entry_frame = tk.Frame(self, pady=10)
        information_entry_frame.pack(anchor='center', pady=20, padx=5)
        rating_label = tk.Label(information_entry_frame, text="Rating:", font=SMALL_FONT)
        rating_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        var = tk.IntVar()
        self.rating = var
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

        comment_label = tk.Label(information_entry_frame, text="Comment:", font=SMALL_FONT)
        comment_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
        comment = tk.Text(information_entry_frame, height = 5, width = 45)
        self.comment = comment
        comment.grid(row = 1, column = 1, columnspan = 5, sticky = 'w', pady = 5, padx = 5)
        create_review_button = tk.Button(self, text="Create Review", fg='blue',
                                         command=lambda: self.create_review(var, comment.get("1.0",'end-1c')))
        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: self.choose_view_museum())
        create_review_button.pack(pady=5, anchor='n')
        back_button.pack(pady=5, anchor='n')

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def create_review(self, rating, comment):
        user = self.controller.get_page(LoginPage).user
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            museum = self.controller.get_page(CuratorViewSpecificMuseumPage).museum
        else:
            museum = self.controller.get_page(ViewSpecificMuseumPage).museum

        cursor = cnx.cursor()

        query = ("""INSERT INTO review (email, museum_name, comment, rating)
                    VALUES (%s, %s, %s, %s)""")

        values = (user, museum, comment, rating.get())

        try:
            cursor.execute(query, values)
        except:
            print('excepted')
            update_query = ("""UPDATE review
                            SET comment = %s, rating = %s
                            WHERE email = %s AND museum_name = %s""")
            values = (comment, rating.get(), user, museum)
            cursor.execute(update_query, values)
        cnx.commit()
        cursor.close()
        self.controller.show_frame(self.choose_view())

    def choose_view(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorSearchForMuseumPage
        else:
            view = SearchForMuseumPage
        self.controller.show_frame(view)

    def choose_view_museum(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorViewSpecificMuseumPage
        else:
            view = ViewSpecificMuseumPage
        self.controller.show_frame(view)

class ViewAllMuseumReviewsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="All Reviews", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        # review_list = getReviews()

        tree = ttk.Treeview(main_frame)
        self.tree = tree
        # num = 0
        # for review in review_list:
        # tree.insert('', 'end', text=review, values=('rating'))
        # num+=1

        tree['columns'] = ('rating')
        tree.column('#0', width=300, anchor='w')
        tree.column('rating', width=100, anchor='center')
        tree.heading('#0', text='Review')
        tree.heading('rating', text='Rating')
        tree.pack()

        back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                command=lambda: self.choose_view_museum())
        back_button.pack(padx=50, pady=20, anchor='w')

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def choose_view_museum(self):
        isCurator = self.controller.get_page(LoginPage).isCurator
        if isCurator:
            view = CuratorViewSpecificMuseumPage
        else:
            view = ViewSpecificMuseumPage
        self.controller.show_frame(view)

    def populateTable(self, museum):
        self.tree.delete(*self.tree.get_children())
        cursor = cnx.cursor()

        query = ("""SELECT comment, rating
                    FROM review
                    WHERE museum_name = '{}'""".format(museum))

        cursor.execute(query)

        comment_list = []
        rating_list = []

        for (comment, rating) in cursor:
            comment_list.append(comment)
            rating_list.append(rating)

        cursor.close()

        num = 0

        for comment in comment_list:
            if (rating_list[num] != None):
                self.tree.insert('', 'end', text=comment, values=(rating_list[num]))
            else:
                self.tree.insert('', 'end', text=comment, values=('-'))
            num+=1

class SearchForMuseumPage(tk.Frame):

    user = ''

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.title = tk.Label(self, text="Welcome, ", font=LARGE_FONT)
        self.title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        museum_select_frame = tk.Frame(self, borderwidth=5, relief='groove')
        museum_select_frame.pack(anchor='center', pady=20, padx=20, ipadx=20)
        self.museum_select_frame = museum_select_frame


        museums = StringVar()
        museums.set('Picasso Museum') # set the default option

        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        museum_list = cursor.fetchall()
        museum_names = []
        for i in range(0, len(museum_list)):
            museum_names.append(museum_list[i][0])
            i += 1


        cursor.close()

        pickAMuseum = tk.Label(museum_select_frame, text="Pick a Museum: ")
        popupMenu = tk.OptionMenu(museum_select_frame, museums, *museum_names)
        pickAMuseum.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)

        self.popupMenu = popupMenu
        self.update_museum_list()


        view_all_museums_button = tk.Button(self, text="View All Museums", fg='blue', command=lambda: show_museums_page())

        my_tickets_button = tk.Button(self, text="My Tickets", fg='blue', command=lambda: show_ticket_page())

        my_reviews_button = tk.Button(self, text="My Reviews", fg='blue', command=lambda: show_reviews_page())

        manage_account_button = tk.Button(self, text="Manage Account", fg='blue', command=lambda: controller.show_frame(ManageAccountPage))

        view_all_museums_button.pack(pady=20, anchor='n')
        my_tickets_button.pack(pady=5, anchor='n')
        my_reviews_button.pack(pady=5, anchor='n')
        manage_account_button.pack(pady=5, anchor='n')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20, anchor='n')

        def show_ticket_page():
            self.controller.get_page(TicketHistoryPage).populateTable(self.user)
            self.controller.show_frame(TicketHistoryPage)

        def show_reviews_page():
            self.controller.get_page(ReviewHistoryPage).populateTable(self.user)
            self.controller.show_frame(ReviewHistoryPage)

        def show_museums_page():
            self.controller.get_page(ViewMuseumsPage).sql_query()
            self.controller.show_frame(ViewMuseumsPage)
    def update_museum_list(self):

        print("Called")

        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        self.museum_list = cursor.fetchall()
        museum_names = []
        for i in range(0, len(self.museum_list)):
            museum_names.append(self.museum_list[i][0])
            i += 1
        self.museums = StringVar()
        self.museums.set(museum_names[0]) # set the default option

        if self.popupMenu != None:
            self.popupMenu.destroy()
        self.popupMenu = tk.OptionMenu(self.museum_select_frame, self.museums, *museum_names)
        self.popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        cursor.close()

        # on change dropdown value
        def change_dropdown(*args):
            controller = self.controller
            isCurator = controller.get_page(LoginPage).isCurator
            if isCurator:
                museum_page = controller.get_page(CuratorViewSpecificMuseumPage)
                museum_page.populateTable(self.museums.get())
                controller.show_frame(CuratorViewSpecificMuseumPage)
            else:
                museum_page = controller.get_page(ViewSpecificMuseumPage)
                museum_page.populateTable(self.museums.get())
                controller.show_frame(ViewSpecificMuseumPage)

        # link function to change dropdown
        self.museums.trace('w', change_dropdown)

class CuratorRequestPage(tk.Frame):

    chosen_museum = None
    controller = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Curator Request", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()

        self.controller = controller
        self.museum_select_frame = tk.Frame(self, borderwidth=5, relief='groove')
        self.museum_select_frame.pack(anchor='center', pady=20, padx=20, ipadx=20)

        self.museums = StringVar()
        museums = self.museums
        museums.set('Picasso Museum')# set the default option
        self.chosen_museum = 'Picasso Museum'

        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        museum_list = cursor.fetchall()
        museum_names = []
        for i in range(0, len(museum_list)):
            museum_names.append(museum_list[i][0])
            i += 1


        cursor.close()

        pickAMuseum = tk.Label(self.museum_select_frame, text="Pick a Museum: ")
        self.popupMenu = tk.OptionMenu(self.museum_select_frame, museums, *museum_names)
        pickAMuseum.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        self.popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)

        # on change dropdown value
        def change_dropdown(*args):
            print(museums.get())
            self.set_museum_name(museums.get())


        # link function to change dropdown
        museums.trace('w', change_dropdown)

        create_request_button = tk.Button(self, text="Create Curator Request", fg='blue',
                                          command=lambda: self.request_to_be_curator())
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: controller.show_frame(ManageAccountPage))


        create_request_button.pack(pady=20, anchor='n')
        back_button.pack(padx=50, pady=20, anchor='w')

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n', pady=20)

    def sql_request(self):
        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        museum_list = cursor.fetchall()
        museum_names = []
        for i in range(0, len(museum_list)):
            museum_names.append(museum_list[i][0])
            i += 1


        cursor.close()
        if self.popupMenu != None:
            self.popupMenu.destroy()
        self.popupMenu = tk.OptionMenu(self.museum_select_frame, self.museums, *museum_names)
        self.popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        print ('success')


    def set_museum_name(self, museum_name):
        self.chosen_museum = museum_name

    def request_to_be_curator(self):
        user = self.controller.get_page(LoginPage).user
        cursor = cnx.cursor()

        q = ("SELECT COUNT(*) FROM museum "
             "WHERE curator_email = '{username}' AND museum_name = '{museum}';").format(username=user, museum=self.chosen_museum)
        cursor.execute(q)
        c = cursor.fetchone()[0]
        if c != 0:
            messagebox.showinfo("Request declined", "You are already a curator of this museum.")
            return

        query = ("""INSERT INTO curator_request (email, museum_name)
                VALUES ('{}', '{}')""".format(user, self.chosen_museum))
        try:
            cursor.execute(query)
            cnx.commit()
            cursor.close()
        except:
            messagebox.showinfo("Request declined", "You already requested to be a curator for {}.".format(self.chosen_museum))
            cursor.close()
            return
        messagebox.showinfo("Request sent", "Your request to be curator of {} will be considered by the Museum Administrator. Thank you for your patience!".format(self.chosen_museum))

class MyMuseumsPage(tk.Frame):

    museum_list = []
    exhibit_count_list = []
    rating_list = []
    tree = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="My Museums", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)

        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('numExhibits','rating')
        self.tree.column('#0', width=200, anchor='w')
        self.tree.column('numExhibits', width=100, anchor='center')
        self.tree.column('rating', width=100, anchor='e')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('numExhibits', text='Exhibit Count')
        self.tree.heading('rating', text='Rating')
        self.tree.pack()

        select_button = tk.Button(self, text="Select", fg='blue', command=lambda: self.select_press(self.tree, controller))
        select_button.pack(pady=5, anchor='n')
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: controller.show_frame(CuratorSearchForMuseumPage))
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20, anchor='n')

    def sql_query(self, username):

        self.museum_list = []
        self.exhibit_count_list = []
        self.rating_list = []

        cursor = cnx.cursor()

        query = ("SELECT museum_name, COUNT(*), AVG(rating) FROM museum "
                 "NATURAL LEFT OUTER JOIN review "
                 "NATURAL LEFT OUTER JOIN exhibit "
                 "WHERE curator_email = '{email}'"
                 "GROUP BY museum_name;").format(email=username)

        cursor.execute(query)

        for (museum_name, exhibit_count, rating) in cursor:
            self.museum_list.append(museum_name)
            self.exhibit_count_list.append(exhibit_count)
            self.rating_list.append(rating)


        cursor.close()

    def populateTable(self, username):
        self.tree.delete(*self.tree.get_children())
        num = 0
        self.sql_query(username)
        for museum in self.museum_list:
            if (self.rating_list[num] != None):
                self.tree.insert('', 'end', text=museum, values=(self.exhibit_count_list[num], str(self.rating_list[num])+'/5'))
            else:
                self.tree.insert('', 'end', text=museum, values=(self.exhibit_count_list[num], '-'))
            num+=1

    def select_press(self, tree, controller):
        curItem = tree.focus()
        museum = tree.item(curItem)['text']
        #Use this for the sql for the next page
        if museum != '':
            if self.controller.get_page(LoginPage).isCurator:
                museum_page = controller.get_page(CuratorViewSpecificMuseumPage)
                museum_page.populateTable(museum)
                controller.show_frame(CuratorViewSpecificMuseumPage)
            else:
                museum_page = controller.get_page(ViewSpecificMuseumPage)
                museum_page.populateTable(museum)
                controller.show_frame(ViewSpecificMuseumPage)

#PAGE 1 - New Exhibit PAGE
class NewExhibitPage(tk.Frame):

    museum = ''
    user = ''

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="New Exhibit Form", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        information_entry_frame = tk.Frame(self, borderwidth=5, relief='groove', pady=10)
        information_entry_frame.pack(anchor='center', pady=20, padx=5)
        exhibit_name_label = tk.Label(information_entry_frame, text="Name*:", font=SMALL_FONT)
        exhibit_name_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        exhibit_text = StringVar()
        exhibit_name_entry = tk.Entry(information_entry_frame, textvariable=exhibit_text)
        exhibit_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        year_label = tk.Label(information_entry_frame, text="Year*:", font=SMALL_FONT)
        year_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
        year_text = StringVar()
        year_entry = tk.Entry(information_entry_frame, textvariable=year_text)
        year_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        url_label = tk.Label(information_entry_frame, text="Link to More Info:", font=SMALL_FONT)
        url_label.grid(row=2, column=0, sticky='e', pady=5, padx=5)
        # u022 is code for dot so that, the user's password is not visible
        url_text = StringVar()
        url_entry = tk.Entry(information_entry_frame, textvariable=url_text)
        url_entry.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        submit_exhibit_button = tk.Button(self, text="Submit Exhibit", fg='blue',
                                          command=lambda: self.add_exhibit(exhibit_text, year_text, url_text))
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: controller.show_frame(CuratorSearchForMuseumPage))

        submit_exhibit_button.pack(anchor='n', expand=True)
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(anchor='n')

    def get_info(self, museum, user):
        self.museum = museum
        self.user = user

    def add_exhibit(self, exhibit, year, url):
        cursor = cnx.cursor()

        query = ("INSERT INTO exhibit "
                 "VALUES (%s, %s, %s, %s);")

        values = (self.museum, exhibit.get(), year.get(), url.get())
        try:
            cursor.execute(query, values)
            cnx.commit()
            messagebox.showinfo("Exhibit created", "Exhibit was successfully added.")
        except:
            messagebox.showerror("Error", "Cannot add exhibits with the same name to the same museum.")
            return

        cursor.close()


class AdminHomePage(tk.Frame):

    user = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Welcome, Sir/Madam", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()

        accept_curator_request_button = tk.Button(self, text="Accept Curator Request", fg='blue',
                                                  command=lambda: self.show_requests_page())
        add_museum_button = tk.Button(self, text="Add Museum", fg='blue',
                                      command=lambda: controller.show_frame(NewMuseumPage))
        delete_museum_button = tk.Button(self, text="Delete Museum", fg='blue',
                                         command=lambda: self.update_delete_page())
        log_out_button = tk.Button(self, text="Log Out", fg='blue',
                                   command=lambda: self.logout(controller))

        accept_curator_request_button.pack(pady=5, anchor='center')
        add_museum_button.pack(pady=5, anchor='n')
        delete_museum_button.pack(pady=5, anchor='n')
        log_out_button.pack(pady=5, anchor='n')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20, anchor='n')

    def show_requests_page(self):
        self.controller.get_page(AdminCuratorRequestsPage).populateTable()
        self.controller.show_frame(AdminCuratorRequestsPage)

    def logout(self, controller):
        login_page = controller.get_page(LoginPage)
        textboxes = login_page.textboxes
        textboxes[0].focus_set()

        for textbox in textboxes:
            textbox.delete(0,END)

        controller.show_frame(LoginPage)

    def update_delete_page(self):
        self.controller.get_page(DeleteMuseumFormPage).update_museum_list()
        self.controller.show_frame(DeleteMuseumFormPage)


class AdminCuratorRequestsPage(tk.Frame):

    museum_list = []
    request_list = []
    curator_email = ''
    museum = ''
    controller = None
    tree = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Curator Requests", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.controller = controller
        self.tree = ttk.Treeview(main_frame)

        self.tree['columns'] = ('museum')
        self.tree.column('#0', width=200, anchor='w')
        self.tree.column('museum', width=200, anchor='e')
        self.tree.heading('#0', text='Museum')
        self.tree.heading('museum', text='Visitor')
        self.tree.pack()
        self.populateTable()
        approve_button = tk.Button(self, text="Approve", fg='blue',
                                   command=lambda: self.accept_request())
        reject_button = tk.Button(self, text="Reject", fg='blue',
                                  command=lambda: self.reject_request())
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: controller.show_frame(AdminHomePage))

        approve_button.pack(pady=5, anchor='n')
        reject_button.pack(pady=5, anchor='n')
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20, anchor='s')

    def reject_request(self):
        cursor = cnx.cursor()
        self.select_press(self.tree, self.controller)
        q = ("DELETE FROM curator_request "
             "WHERE museum_name = '{museum}' AND email = '{email}';".format(museum=self.museum, email=self.curator_email))
        cursor.execute(q)
        cnx.commit()
        cursor.close()
        self.populateTable()
        messagebox.showinfo("Deny Request", "{new}'s request has been declined.".format(new=self.curator_email))


    def accept_request(self):
        cursor = cnx.cursor()
        self.select_press(self.tree, self.controller)

        #check if museum already has a curator and display warning
        q = ("SELECT curator_email FROM museum "
             "WHERE museum_name = '{museum}'".format(museum=self.museum))
        cursor.execute(q)
        cur = cursor.fetchone()[0]
        if cur is not None:
            result = messagebox.askquestion("Accept Curator Request", "{email} is currently the curator for the {museum}. Accepting {new}\'s "
                                                                      "request will make {new} the new curator of {museum}. \n\n "
                                                                      "Do you wish to proceed?".format(email=cur, museum=self.museum, new=self.curator_email))

        if cur is None or result == 'yes':
            print("yo")
            query = ("UPDATE museum "
                     "SET curator_email = '{new}' "
                     "WHERE museum_name = '{museum}';".format(new=self.curator_email, museum=self.museum))
            cursor.execute(query)
            cnx.commit()

            q = ("DELETE FROM curator_request "
                 "WHERE museum_name = '{museum}' AND email = '{email}';".format(museum=self.museum, email=self.curator_email))
            cursor.execute(q)
            cnx.commit()
            cursor.close()
            self.populateTable()
            messagebox.showinfo("Request Accepted", "Curator request was accepted. \n{new} is now the curator of {museum}"
                                .format(new=self.curator_email, museum=self.museum))
        else:
            return


    def select_press(self, tree, controller):
        curItem = tree.focus()
        self.museum = tree.item(curItem)['text']
        self.curator_email = tree.item(curItem)['values'][0]

    def populateTable(self):
        self.tree.delete(*self.tree.get_children())

        self.sqlQuery()
        num = 0
        for museum in self.museum_list:
            self.tree.insert('', 'end', text=museum, values=(self.request_list[num]))
            num+=1

    def sqlQuery(self):

        self.museum_list = []
        self.request_list = []

        cursor = cnx.cursor()

        query = ("SELECT museum_name, email "
                 "FROM curator_request;")
        cursor.execute(query)

        for (museum_name, email) in cursor:
            self.museum_list.append(museum_name)
            self.request_list.append(email)

        cursor.close()

class DeleteMuseumFormPage(tk.Frame):
    museum=''
    museums = None
    museum_list = []
    popupMenu = None
    museum_select_frame = None
    controller = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Delete Museum Form", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()

        self.museum_select_frame = tk.Frame(self, borderwidth=5, relief='groove')
        self.museum_select_frame.pack(anchor='center', pady=20, padx=20, ipadx=20)
        self.controller = controller
        museum_names = []
        pickAMuseum = tk.Label(self.museum_select_frame, text="Pick a Museum: ")
        pickAMuseum.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        # self.museums = StringVar()
        # self.popupMenu = tk.OptionMenu(self.museum_select_frame, self.museums, *museum_names)
        # self.popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        # self.update_museum_list()

        delete_museum_button = tk.Button(self, text="Delete Museum", fg='blue',
                                         command=lambda: self.delete_museum())
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: controller.show_frame(AdminHomePage))


        delete_museum_button.pack(pady=20, anchor='n')
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20, anchor='n')

    def delete_museum(self):
        cursor = cnx.cursor()
        result = messagebox.askquestion("Delete Museum", "Are you sure you wish to delete {museum}? "
                                                         "This cannot be undone.".format(museum=self.museum))

        if result == 'yes':
            query = ("DELETE FROM museum "
                     "WHERE museum_name = '{mus}';".format(mus=self.museum))
            cursor.execute(query)
            cnx.commit()
            self.update_museum_list()
            self.update_all_museum_lists()
            cursor.close()
        else:
            return

    def update_museum_list(self):

        query = ("SELECT museum_name FROM museum "
                 "ORDER BY museum_name")

        cursor = cnx.cursor()
        cursor.execute(query)
        self.museum_list = cursor.fetchall()
        museum_names = []
        for i in range(0, len(self.museum_list)):
            museum_names.append(self.museum_list[i][0])
            i += 1
        self.museums = StringVar()
        self.museums.set(museum_names[0]) # set the default option
        if self.popupMenu != None:
            self.popupMenu.destroy()
        self.popupMenu = tk.OptionMenu(self.museum_select_frame, self.museums, *museum_names)
        self.popupMenu.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        # self.popupMenu['menu'].delete(0, 'end')
        cursor.close()

        # on change dropdown value
        def change_dropdown(*args):
            self.museum = self.museums.get()

        # link function to change dropdown
        self.museums.trace('w', change_dropdown)

    def update_all_museum_lists(self):
        visitor_page = self.controller.get_page(SearchForMuseumPage)
        visitor_page.update_museum_list()
        curator_page = self.controller.get_page(CuratorSearchForMuseumPage)
        curator_page.update_museum_list()


class NewMuseumPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="New Museum Form", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack()
        information_entry_frame = tk.Frame(self, borderwidth=5, relief='groove', pady=10)
        information_entry_frame.pack(anchor='center', pady=20, padx=5)
        museum_name_label = tk.Label(information_entry_frame, text="Name*:", font=SMALL_FONT)
        museum_name_label.grid(row=0, column=0, sticky='e', pady=5, padx=5)
        museum_name_text = StringVar()
        museum_name_entry = tk.Entry(information_entry_frame, textvariable=museum_name_text)
        museum_name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)

        ticket_price_label = tk.Label(information_entry_frame, text="Ticket price:", font=SMALL_FONT)
        ticket_price_label.grid(row=1, column=0, sticky='e', pady=5, padx=5)
        ticket_price_text = StringVar()
        ticket_price_entry = tk.Entry(information_entry_frame, textvariable=ticket_price_text)
        ticket_price_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        submit_museum_button = tk.Button(self, text="Submit Museum", fg='blue',
                                         command=lambda: self.create_new_museum(museum_name_text, ticket_price_text))
        back_button = tk.Button(self, text="Back", fg='blue',
                                command=lambda: controller.show_frame(AdminHomePage))

        submit_museum_button.pack(anchor='n', expand=True)
        back_button.pack(padx=50, pady=20, anchor='w')
        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20, anchor='n')





    def create_new_museum(self, museum, price):

        visitor_page = self.controller.get_page(SearchForMuseumPage)

        print('user: ' + self.controller.get_page(LoginPage).user)
        print(self.controller)

        cursor = cnx.cursor()
        if museum.get() is '':
            messagebox.showerror("Error", "You cannot create a museum without a name.")
            return
        query = ("INSERT INTO museum "
                 "VALUES('{museum}', NULL, NULL);".format(museum=museum.get()))
        try:
            cursor.execute(query)
        except:
            messagebox.showinfo("New museum", "Museum could not be added because another Museum with the same name exists.")
            return
        cnx.commit()
        if price is not None:
            q = ("UPDATE museum "
                 "SET ticket_price = '{price}' "
                 "WHERE museum_name = '{museum}';".format(price=price.get(), museum=museum.get()))
            cursor.execute(q)
            cnx.commit()
        cursor.close()
        messagebox.showinfo("Museum Created", "A new museum: {museum} has been added!".format(museum=museum.get()))
        self.update_all_museum_lists()

    def update_all_museum_lists(self):
        visitor_page = self.controller.get_page(SearchForMuseumPage)
        visitor_page.update_museum_list()
        curator_page = self.controller.get_page(CuratorSearchForMuseumPage)
        curator_page.update_museum_list()
        self.controller.get_page(DeleteMuseumFormPage).update_museum_list()

app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
