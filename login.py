from Tkinter import Tk, Entry, Button, StringVar, Label, Frame, END
import hashlib
from SpellingGame import SpellingGame

class Login():
    
    def __init__(self):
        root = Tk()
    
        frame = Frame(root)
        frame.pack()
        self.userEntry = Entry(frame, width=15)
        self.passEntry = Entry(frame, width=15, show='*')
        userLabel = Label(frame, text="Username:")
        passLabel = Label(frame, text="Password:")
        buttonSubmit = Button(frame, text="Submit", command=self.login)

        userLabel.grid(row=0, column=0)
        self.userEntry.grid(row=0, column=1)
        passLabel.grid(row=1, column=0)
        self.passEntry.grid(row=1, column=1)
        buttonSubmit.grid(row=2, column=1)

        root.mainloop()


    def login(self):
        username = self.userEntry.get()
        password = self.passEntry.get()
        if (username == 'Michael' and password == 'hello'):
            game = SpellingGame()
        else:
            print 'Invalid Login'
            self.userEntry.delete(0, END)
            self.passEntry.delete(0, END)

        

def main():
    login = Login()

if __name__=='__main__':
    main()
