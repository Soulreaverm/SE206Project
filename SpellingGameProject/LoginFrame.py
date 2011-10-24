#!/usr/bin/env python
from Tkinter import Tk, Entry, Button, StringVar, Label, Frame, Canvas
from Tkconstants import *
import hashlib, tkMessageBox
from SpellingDatabase import SpellingDatabase
from User import User

class LoginFrame(Frame):
    """Class which controls the Login and Register screens of the spelling aid"""
    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.db = self.parent.db
        
        #Create login screen widgets
        font = ("Helvetica", 20)
        self.userEntry = Entry(self.parent, width=15, font=font)
        self.passEntry = Entry(self.parent, width=15, show='*', font=font)
        self.passEntry.bind('<Return>', self.login)
        buttonSubmit = Button(self.parent, text="Login", command=self.login, width=10)
        buttonRegSwitch = Button(self.parent, text="New User",
                                 command=self.viewRegister, width=10)
        
        #Create register screen widgets
        self.userRegEntry = Entry(self.parent, width=15, font=font)
        self.passRegEntry = Entry(self.parent, width=15, show='*',
                                  font=font)
        self.passRegEntry.bind('<Return>', self.register)
        buttonRegister = Button(self.parent, text="Register",
                                command=self.register, width=10)
        buttonBack = Button(self.parent, text="Back",
                            command=self.viewLogin, width=10)
        
        #Create a canvas for each screen and populate
        self.login_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
        self.register_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
       
        self.login_canvas.create_text(300, 40, text="Login", font=font, fill="#004183")
        self.login_canvas.create_text(170, 80, text="Username:", font=font,
                                      anchor=N)
        self.login_canvas.create_text(170, 150, text="Password:", font=font,
                                      anchor=N)
        self.login_canvas.create_window(300, 80, anchor=NW,
                                        window=self.userEntry)
        self.login_canvas.create_window(300, 150, anchor=NW,
                                        window=self.passEntry)
        self.login_canvas.create_window(200, 220, window=buttonRegSwitch)
        self.login_canvas.create_window(400, 220, window=buttonSubmit)
        self.login_canvas.pack()

        self.register_canvas.create_text(300, 40, text="Register", font=font, fill="#004183")
        self.register_canvas.create_text(170, 80, text="Username:", font=font,
                                         anchor=N)
        self.register_canvas.create_text(170, 150, text="Password:", font=font,
                                         anchor=N)
        self.register_canvas.create_window(300, 80, anchor=NW, 
                                           window=self.userRegEntry)
        self.register_canvas.create_window(300, 150, anchor=NW,
                                           window=self.passRegEntry)
        self.register_canvas.create_window(200, 220, window=buttonRegister)
        self.register_canvas.create_window(400, 220, window=buttonBack)


    def login(self, event=None):
        "Check the user's input and allow access if it is correct"""
        usernameGiven = self.userEntry.get()
        passwordGiven = self.passEntry.get()
        userDetails = self.db.sql("""SELECT * FROM
                                  users WHERE username='%s'"""
                                  %(usernameGiven.lower().strip()))
        #Check that the username exists
        if len(userDetails)==1:
            passHash = userDetails[0][2]
            #Check that the password is correct
            if (hashlib.sha1(passwordGiven).hexdigest() == passHash):
                #Details are correct, unlock application
                self.parent.login(User(userDetails[0]))
                loginFailed = False
            else:
                loginFailed = True
        else:
            loginFailed = True
        if loginFailed:
            #If details are incorrect show an error message
            tkMessageBox.showerror("Login Failed",
                                   "Invalid username or password")
            self.userEntry.delete(0, END)
            self.passEntry.delete(0, END)

    def register(self):
        """Register a new user with provided input"""
        username = self.userRegEntry.get()
        passwd = self.passRegEntry.get()
        if username != '' and passwd != '':
            username = username.lower().strip()
            passHash = hashlib.sha1(passwd).hexdigest()
            self.db.sql("""INSERT INTO users (username, passwd) VALUES 
                        ('%s', '%s')"""%(username, passHash))
            self.viewLogin()

    def viewRegister(self):
        """Switch to the register screen"""
        self.login_canvas.pack_forget()
        self.register_canvas.pack()

    def viewLogin(self):
        """Switch to the login screen"""
        self.register_canvas.pack_forget()
        self.login_canvas.pack()
        

def main():
    login = Login()

if __name__=='__main__':
    main()
