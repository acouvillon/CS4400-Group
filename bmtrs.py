from tkinter import *
import pymysql as mdb
import pandas as pd
import time
from tkinter import messagebox
import datetime
import re
import os

#Define a class to set up our GUI
class BmtrsApp(object):
    def __init__(self, login_screen):
    	 #Set the window title
        login_screen.wm_title("BMTRS")
        

#In our main function, create the GUI and pass it to our App class
def main():
	login_screen= Tk()
	start= App(login_screen)
	login_screen.mainloop()
	input('Press ENTER to exit')

#Run the main function
if __name__ == "__main__":
    main()
