#!/usr/bin/env python
from Tkinter import Tk, Entry, Button, StringVar, Label, Frame, Canvas
from Tkconstants import *
import hashlib
from SpellingDatabase import SpellingDatabase
from User import User

class LoginFrame(Frame):
    
    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.db = self.parent.db
    
        font = ("Helvetica", 20)
        self.userEntry = Entry(self.parent, width=15, font=font)
        self.passEntry = Entry(self.parent, width=15, show='*', font=font)
        self.passEntry.bind('<Return>', self.login)
        buttonSubmit = Button(self.parent, text="Login", command=self.login)
        buttonRegSwitch = Button(self.parent, text="New User",
                                 command=self.viewRegister)

        self.userRegEntry = Entry(self.parent, width=15, font=font)
        self.passRegEntry = Entry(self.parent, width=15, show='*',
                                  font=font)
        self.passRegEntry.bind('<Return>', self.register)
        buttonRegister = Button(self.parent, text="Register",
                                command=self.register)
        buttonBack = Button(self.parent, text="Back",
                            command=self.viewLogin)
        
        self.login_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
        self.register_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
       
        self.login_canvas.create_text(300, 40, text="Login", font=font)
        self.login_canvas.create_text(200, 80, text="Username:", font=font,
                                      anchor=N)
        self.login_canvas.create_text(200, 150, text="Password:", font=font,
                                      anchor=N)
        self.login_canvas.create_window(300, 80, anchor=NW,
                                        window=self.userEntry)
        self.login_canvas.create_window(300, 150, anchor=NW,
                                        window=self.passEntry)
        self.login_canvas.create_window(200, 220, window=buttonRegSwitch)
        self.login_canvas.create_window(400, 220, window=buttonSubmit)
        self.login_canvas.pack()

        self.register_canvas.create_text(300, 40, text="Register", font=font)
        self.register_canvas.create_text(200, 80, text="Username:", font=font,
                                         anchor=N)
        self.register_canvas.create_text(200, 150, text="Password:", font=font,
                                         anchor=N)
        self.register_canvas.create_window(300, 80, anchor=NW, 
                                           window=self.userRegEntry)
        self.register_canvas.create_window(300, 150, anchor=NW,
                                           window=self.passRegEntry)
        self.register_canvas.create_window(200, 220, window=buttonRegister)
        self.register_canvas.create_window(400, 220, window=buttonBack)


    def login(self, event=None):
        usernameGiven = self.userEntry.get()
        passwordGiven = self.passEntry.get()
        userDetails = self.db.sql("""SELECT * FROM
                                  users WHERE username='%s'"""
                                  %(usernameGiven.lower().strip()))
        if len(userDetails)==1:
            passHash = userDetails[0][2]
            if (hashlib.sha1(passwordGiven).hexdigest() == passHash):
                self.parent.login(User(userDetails[0]))
        else:
            print 'Invalid Username or Password'
            self.userEntry.delete(0, END)
            self.passEntry.delete(0, END)

    def register(self):
        username = self.userRegEntry.get()
        passwd = self.passRegEntry.get()
        if username != '' and passwd != '':
            username = username.lower().strip()
            passHash = hashlib.sha1(passwd).hexdigest()
            self.db.sql("""INSERT INTO users (username, passwd) VALUES 
                        ('%s', '%s')"""%(username, passHash))
            self.viewLogin()

    def viewRegister(self):
        self.login_canvas.pack_forget()
        self.register_canvas.pack()

    def viewLogin(self):
        self.register_canvas.pack_forget()
        self.login_canvas.pack()
        

def main():
    login = Login()

if __name__=='__main__':
    main()
