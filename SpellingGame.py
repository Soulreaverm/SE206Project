#!/usr/bin/env python
from Tkinter import Tk, Button, Entry, Label, Frame, StringVar, Canvas, NE, CENTER, END
from Festival import FestivalInterface
from SpellingDatabase import SpellingDatabase
from PIL import Image, ImageTk
import random

class SpellingGame:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user
        print "Welcome, %s"%(self.user.username)
        self.word_list = self.get_dictionary()
        self.random_list = self.get_random_list(15)
        self.festival = FestivalInterface()
        self.init_gui()
        
    def get_dictionary(self):
        db = SpellingDatabase()
        word_records = db.sql("""SELECT word FROM words WHERE
                              difficulty LIKE 'SB%'""")
        word_list = []
        for word in word_records:
            word_list.append(str(word[0]))
        return word_list
 

    def get_random_list(self, length):
        random_list = random.sample(self.word_list, length)
        self.list_length = length
        self.random_list_iter = iter(random_list)
        self.current_word = self.random_list_iter.next()
        return random_list

    def next_word(self):
        try:
            self.current_word = self.random_list_iter.next()
            self.canvas.itemconfig(self.progress_display, text="%d/%d"
                                   %(self.random_list.index(self.current_word) + 1,
                                   self.list_length))
            self.festival.speech(self.current_word)
        except StopIteration:
            self.random_list = self.get_random_list(15)
            self.next_word()

    def replay_word(self):
       self.festival.speech(self.current_word)

    def submit_word(self, event=None):
        guess = self.entry.get()
        self.entry.delete(0, END)
        if guess == self.current_word:
            self.correct()
        else:
            self.incorrect()
        self.canvas.itemconfig(self.word_display, text='%s'%(self.current_word))

    def correct(self):
        self.canvas.itemconfig(self.canvas_image, image=self.correct_img)
        self.canvas.itemconfig(self.word_display, fill="green")
        print "Correct!"

    def incorrect(self):
        self.canvas.itemconfig(self.canvas_image, image=self.wrong_img)
        self.canvas.itemconfig(self.word_display, fill="red")
        print "Incorrect"

    def init_gui(self):
        root = Tk()
        frame = Frame(root, height=500, width=500)
        frame.pack()

        correct_img = Image.open("correct.png")
        wrong_img  = Image.open("wrong.png")
        correct_img.thumbnail((64, 64), Image.ANTIALIAS)
        wrong_img.thumbnail((64, 64), Image.ANTIALIAS)
        self.correct_img = ImageTk.PhotoImage(correct_img, master=root)
        self.wrong_img = ImageTk.PhotoImage(wrong_img, master=root)

        self.entry = Entry(root, width=15, font=('Helvetica', 20, 'normal'),
                                                  justify=CENTER)
        self.entry.bind("<Return>", self.submit_word)
        buttonNext = Button(frame, width=10, text="Next Word",
                            command=self.next_word)
        buttonSubmit = Button(frame, width=10, text="Submit",
                              command=self.submit_word)
        buttonReplay = Button(frame, width=10, text="Repeat Word",
                              command=self.replay_word)
        self.canvas = Canvas(frame, width=600, height=250, bg="#004183")
        self.word_display = self.canvas.create_text((300, 125), text="?",
                           font=("Helvetica", 50, "bold"))
        self.progress_display = self.canvas.create_text((593, 5),
                                text="%d/%d"%(1, self.list_length),
                                font=("Helvetica", 25, "bold"), anchor=NE)
        self.canvas.create_window(300, 200, window=self.entry)
        self.canvas_image = self.canvas.create_image(500, 200)
        self.canvas.grid(row=0, column=0, columnspan=3)
        buttonReplay.grid(row=1, column=0)
        buttonSubmit.grid(row=1, column=1)
        buttonNext.grid(row=1, column=2)
        
        root.mainloop()        

def main():
    user = Button()
    user.username = "hello"
    game = SpellingGame(1, user)

if __name__=='__main__':
    main()

