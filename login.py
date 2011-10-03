#!/usr/bin/env python
from Tkinter import Tk, Entry, Button, StringVar, Label, Frame, END
import hashlib
from SpellingGame import SpellingGame
from SpellingDatabase import SpellingDatabase

class Login():
    
    def __init__(self):
        self.root = Tk()
        self.db = SpellingDatabase()
    
        self.loginFrame = Frame(self.root)
        self.loginFrame.pack()
        self.userEntry = Entry(self.loginFrame, width=15)
        self.passEntry = Entry(self.loginFrame, width=15, show='*')
        userLabel = Label(self.loginFrame, text="Username:")
        passLabel = Label(self.loginFrame, text="Password:")
        buttonSubmit = Button(self.loginFrame, text="Login", command=self.login)
        buttonRegSwitch = Button(self.loginFrame, text="New User",
                                 command=self.viewRegister)

        userLabel.grid(row=0, column=0)
        self.userEntry.grid(row=0, column=1)
        passLabel.grid(row=1, column=0)
        self.passEntry.grid(row=1, column=1)
        buttonSubmit.grid(row=2, column=1)
        buttonRegSwitch.grid(row=2, column=0, padx=10)

        self.registerFrame = Frame(self.root)
        self.userRegEntry = Entry(self.registerFrame, width=15)
        self.passRegEntry = Entry(self.registerFrame, width=15, show='*')
        userRegLabel = Label(self.registerFrame, text="Username:")
        passRegLabel = Label(self.registerFrame, text="Password:")
        buttonRegister = Button(self.registerFrame, text="Register",
                                command=self.register)
        buttonBack = Button(self.registerFrame, text="Back",
                            command=self.viewLogin)

        userRegLabel.grid(row=0, column=0)
        self.userRegEntry.grid(row=0, column=1)
        passRegLabel.grid(row=1, column=0)
        self.passRegEntry.grid(row=1, column=1)
        buttonBack.grid(row=2, column=1)
        buttonRegister.grid(row=2, column=0, padx=10)

        self.root.mainloop()


    def login(self):
        usernameGiven = self.userEntry.get()
        passwordGiven = self.passEntry.get()
        passHash = self.db.sql("SELECT passwd FROM users WHERE username='%s'"
                               %(usernameGiven.lower().strip()))
        if len(passHash)==1:
            passHash = passHash[0][0]
        if (hashlib.sha1(passwordGiven).hexdigest() == passHash):
            self.root.destroy()
            game = SpellingGame()
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
        self.loginFrame.pack_forget()
        self.registerFrame.pack()

    def viewLogin(self):
        self.registerFrame.pack_forget()
        self.loginFrame.pack()
        

def main():
    login = Login()

if __name__=='__main__':
    main()
