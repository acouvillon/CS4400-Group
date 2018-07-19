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

        self.frames ={}
        for F in {LoginPage, RegistrationPage, SearchForMuseumPage, ViewMuseumsPage, TicketHistoryPage, ReviewHistoryPage, ViewSpecificMuseumPage, ManageAccountPage, MuseumReviewPage}:
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

    user = None
    textboxes = None

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
            user = username.get()
            self.user = user
            next_page = self.controller.get_page(SearchForMuseumPage)
            next_page.title['text'] = "Welcome, " + user
            next_page.user = user

            controller.show_frame(SearchForMuseumPage)
            print("visitor logged in")
            

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

        # on change dropdown value
        def change_dropdown(*args):
            museum_page = controller.get_page(ViewSpecificMuseumPage)
            museum_page.populateTable(museums.get())
            controller.show_frame(ViewSpecificMuseumPage)

        # link function to change dropdown
        museums.trace('w', change_dropdown)

        view_all_museums_button = tk.Button(self, text="View All Museums", fg='blue', command=lambda: show_museums_page())

        my_tickets_button = tk.Button(self, text="My Tickets", fg='blue', command=lambda: show_ticket_page())

        my_reviews_button = tk.Button(self, text="My Reviews", fg='blue', command=lambda: show_reviews_page())

        manage_account_button = tk.Button(self, text="Manage Account", fg='blue', command=lambda: controller.show_frame(ManageAccountPage))

        view_all_museums_button.pack(pady=20, anchor='n')
        my_tickets_button.pack(pady=5, anchor='n')
        my_reviews_button.pack(pady=5, anchor='n')
        manage_account_button.pack(pady=5, anchor='n')
        
        def show_ticket_page():
            self.controller.get_page(TicketHistoryPage).populateTable(self.user)
            self.controller.show_frame(TicketHistoryPage)
            
        def show_reviews_page():
            self.controller.get_page(ReviewHistoryPage).populateTable(self.user)
            self.controller.show_frame(ReviewHistoryPage)
            
        def show_museums_page():
            self.controller.get_page(ViewMuseumsPage).sql_query()
            self.controller.show_frame(ViewMuseumsPage)
            

class RegistrationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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

        #todo - check if confirm text matches password text
        credit_card = tk.Label(information_entry_frame, text="Credit Card Number:", font=SMALL_FONT)
        credit_card.grid(row=3, column=0, sticky='e', pady=5, padx=5)
        credit_card_text = StringVar()
        credit_card_entry = tk.Entry(information_entry_frame, textvariable=credit_card_text)
        credit_card_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        #todo - credit card entry formatting as .... .... .... 3333
        credit_card_text.trace("w", lambda name, index, mode, credit_card_text=credit_card_text: entryFormattingForCreditCardNumber(credit_card_entry))

        exp_date = tk.Label(information_entry_frame, text="Credit Card Exp. Date (mm/yy):", font=SMALL_FONT)
        exp_date.grid(row=4, column=0, sticky='e', pady=5, padx=5)
        exp_date_text= StringVar()
        #todo - format entry as mm/yy
        exp_date_entry = tk.Entry(information_entry_frame, textvariable=exp_date_text)
        exp_date_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)

        security_code = tk.Label(information_entry_frame, text="Credit Card Security Code:", font=SMALL_FONT)
        security_code.grid(row=5, column=0, sticky='e', pady=5, padx=5)
        sec_code_text = StringVar()
        #todo - format entry as 3 digit entry only
        security_code_entry = tk.Entry(information_entry_frame, textvariable=sec_code_text)
        security_code_entry.grid(row=5, column=1, sticky='w', pady=5, padx=5)

        black_line=Frame(self, height=1, width=500, bg="black")
        black_line.pack(pady=20)
        create_account_button = tk.Button(self, text="Create Account", fg='blue',
                                          command=lambda: create_account(email_text, pwd_text, credit_card_text, exp_date_text, sec_code_text, controller))
        back_button = tk.Button(self, text="Back", fg='blue', command=lambda: controller.show_frame(LoginPage))
        create_account_button.pack(pady=5, anchor='n')
        back_button.pack(pady=5, anchor='n')

#todo - implement this function
def create_account(email, pwd, credit_card_num, exp_date, security_code, controller):
    cursor = cnx.cursor()
    
    date = exp_date.get()
    
            
    if len(email.get())==0 or len(pwd.get())==0 or len(credit_card_num.get())==0 or len(exp_date.get())==0 or len(security_code.get())==0:
        messagebox.showerror("Error","All fields required")
        return
            
    if len(date) != 5 or date[2]!='/':
        messagebox.showerror("Error","Invalid expiration date")
        return
        
    month = date[:2]
    year = date[3:]
    
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

def entryFormattingForCreditCardNumber(entry):
    text = entry.get()
    if len(text) % 4 == 0:
        entry.insert(SEPARATOR, ' ')
        entry.icursor(len(text)+1)


class ViewMuseumsPage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="All Museums", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
        main_frame = tk.Frame(self, pady=10)
        main_frame.pack(anchor='center', pady=0, padx=5)
        self.tree = ttk.Treeview(main_frame)
            
        self.tree['columns'] = ('rating')
        self.tree.column('rating', width=100, anchor='ne')
        self.tree.heading('#0', text='Museum Name')
        self.tree.heading('rating', text='Average Rating')
        self.tree.pack()
        select_button = tk.Button(self, text="Select", fg='black', command=lambda: self.select_press(self.tree, controller))
        select_button.pack(pady=5, anchor='n')
        back_button = tk.Button(self, text="Back", fg='black', command=lambda: controller.show_frame(SearchForMuseumPage))
        back_button.pack(pady=5, anchor='n')
        
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
                self.tree.insert('', 'end', text=museum, values=(review_list[num]))
            else:
                self.tree.insert('', 'end', text=museum, values=('-'))
            num+=1
    
        
    def select_press(self, tree, controller):
        curItem = tree.focus()
        museum = tree.item(curItem)['text']
        #Use this for the sql for the next page
        if museum != '':
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
        title = tk.Label(self, text="My Tickets", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
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
        back_button = tk.Button(self, text="Back", fg='black', command=lambda: controller.show_frame(SearchForMuseumPage))
        back_button.pack(pady=5, anchor='n')
        #self.populateTable('helen@gatech.edu')
        
    #must be called from user login page at login
    def populateTable(self, username):
        self.tree.delete(*self.tree.get_children())
        num = 0
        self.sqlQuery(username)
        for museum in self.museum_list:
            self.tree.insert('', 'end', text=museum, values=(self.time_list[num].strftime('%m/%d/%Y'), '$'+self.price_list[num]))
            num+=1
                    
    def sqlQuery(self, username):
        
        self.museum_list = []
        self.time_list = []
        self.price_list = []
        
        cursor = cnx.cursor()

        query = ("""SELECT museum_name, purchase_timestamp, price
                    FROM ticket 
                    WHERE email = '{0}'""".format(username))

        cursor.execute(query)
        

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
        title = tk.Label(self, text="My Reviews", font=LARGE_FONT)
        title.pack(pady=10, padx=10)
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
        back_button = tk.Button(self, text="Back", fg='black', command=lambda: controller.show_frame(SearchForMuseumPage))
        back_button.pack(pady=5, anchor='n')
        # self.populateTable('helen@gatech.edu')
        
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
                    WHERE email = '{0}'""".format(username))

        cursor.execute(query)
        
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
            review_museum_button = tk.Button(self, borderwidth=0, text="Review Museum", fg='blue',
                                        command=lambda: self.create_review())
            view_other_reviews_button = tk.Button(self, borderwidth=0, text="View Others' Reviews", fg='blue',
                                        command=lambda: controller.show_frame(MyReviewsPage))
            back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(SearchForMuseumPage))

            purchase_ticket_button.pack(anchor='n', expand=True)
            review_museum_button.pack(pady=0, anchor='n')
            view_other_reviews_button.pack(pady=0, anchor='n')
            back_button.pack(pady=0, anchor='n')
            
            
    #must be called from previous page
    def populateTable(self, museum):
        num = 0
        self.title['text'] = museum
        self.museum = museum
        self.sqlQuery(museum)
        for exhibit in self.exhibit_list:
            self.tree.insert('', 'end', text=exhibit, values=(self.year_list[num], self.link_list[num]))
            num+=1
    
    def sqlQuery(self, museum_name):
        cursor = cnx.cursor()

        query = ("""SELECT exhibit_name, year, url
                    FROM exhibit
                    WHERE museum_name = '{0}'""".format(museum_name))

        cursor.execute(query)

        for (exhibit, year, link) in cursor:
            self.exhibit_list.append(exhibit)
            self.year_list.append(year)
            self.link_list.append(link)
        
        query2 = ("""SELECT ticket_price
                    FROM museum
                    WHERE museum_name = '{0}'""".format(museum_name))
                    
        cursor.execute(query2)
        
        for (price) in cursor:
            self.title['text'] += ' - $' + price[0]
            self.price = price[0]


        cursor.close()
    
    def purchase_ticket(self):
        
        user = self.controller.get_page(LoginPage).user
    
        cursor = cnx.cursor()

        query = ("""INSERT INTO ticket (email, museum_name, price, purchase_timestamp)
            VALUES ('{}', '{}', '{}', '{}')""".format(user, self.museum, self.price, datetime.datetime.now()))
                    

        try:
            cursor.execute(query)
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
                    WHERE email = '{}' AND museum_name = '{}'""".format(user, self.museum))

        cursor.execute(ticket_query)
        
        if cursor.fetchone() == None:
            messagebox.showerror("Error","You cannot leave a review without purchasing a ticket for this museum first.")
            cursor.close()
            return
        
        review_query = ("""SELECT *
                        FROM review
                        WHERE email = '{}' AND museum_name = '{}'""".format(user, self.museum))
        cursor.execute(review_query)
        
        if cursor.fetchone() != None:
            messagebox.showerror("Error","You have already left a review for this museum.")
            cursor.close()
            return
            
        cursor.close()
        
        next_page = self.controller.get_page(MuseumReviewPage)
        
        next_page.comment.delete('1.0',END)
        next_page.rating.set(None)
        
        self.controller.show_frame(MuseumReviewPage)
    
    def link_tree(self,event):
        cur_item = self.tree.focus()
        url = self.tree.item(cur_item)['values'][1]
        
        import webbrowser
        webbrowser.open('{}'.format(url))

        
class ManageAccountPage(tk.Frame):

    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            title = tk.Label(self, text="Manage Account", font=LARGE_FONT)
            title.pack(pady=10, padx=10)
            black_line=Frame(self, height=1, width=500, bg="black")
            black_line.pack()

            log_out_button = tk.Button(self, text="Log Out", fg='blue',
                                     command=lambda: self.logout(controller))
            curator_request_button = tk.Button(self, borderwidth=0, text="Curator Request", fg='blue',
                                        command=lambda: controller.show_frame(MyTicketsPage))
            delete_account_button = tk.Button(self, borderwidth=0, text="Delete Account", fg='blue',
                                        command=lambda: self.delete_account(controller))
            back_button = tk.Button(self, borderwidth=0, text="Back", fg='blue',
                                        command=lambda: controller.show_frame(SearchForMuseumPage))

            log_out_button.pack(pady=20, anchor='n')
            curator_request_button.pack(pady=5, anchor='n')
            delete_account_button.pack(pady=5, anchor='n')
            back_button.pack(pady=5, anchor='n')

    def logout(self, controller):
        login_page = controller.get_page(LoginPage)
        textboxes = login_page.textboxes
        
        textboxes[0].focus_set()
        
        for textbox in textboxes:
            textbox.delete(0,END)
        
        controller.show_frame(LoginPage)
        
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
            back_button = tk.Button(self, text="Back", fg='blue', command=lambda: controller.show_frame(ViewSpecificMuseumPage))
            create_review_button.pack(pady=5, anchor='n')
            back_button.pack(pady=5, anchor='n')

    def create_review(self, rating, comment):
        user = self.controller.get_page(LoginPage).user
        museum = self.controller.get_page(ViewSpecificMuseumPage).museum
        
        cursor = cnx.cursor()
        print("rating: " + str(rating.get()))
        print(comment)
        
        

        query = ("""INSERT INTO review (email, museum_name, comment, rating)
                    VALUES (%s, %s, %s, %s)""")
                    
        values = (user, museum, comment, rating.get())
                    
        cursor.execute(query, values)
        cnx.commit()
        cursor.close()
        self.controller.show_frame(SearchForMuseumPage)
        
app = BMTRSApp()
#tkinter functionality keeps app running
app.mainloop()
