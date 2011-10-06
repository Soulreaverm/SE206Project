#!/usr/bin/env python
from Tkinter import Tk, Button, Entry, Label, Frame, StringVar, Canvas, OptionMenu
from Tkconstants import *
from Festival import FestivalInterface
from SpellingDatabase import SpellingDatabase
from PIL import Image, ImageTk
from Word import Word
from List import WordList
import random
from threading import Timer

class SpellingGame:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user
        print "Welcome, %s"%(self.user.username)
        self.db = SpellingDatabase()
        self.word_list = self.get_dictionary()
        self.list_list = self.get_lists()
        self.current_list = self.get_random_list(15)
        self.festival = FestivalInterface()
        self.init_gui()

    def get_lists(self):
        list_records = self.db.sql("""SELECT * FROM lists""")
        list_list = []
        for wordlist in list_records:
            list_list.append(WordList(wordlist))
        return list_list
            
        
    def get_dictionary(self):
        word_records = self.db.sql("""SELECT * FROM words WHERE
                              difficulty LIKE 'SB%'""")
        word_list = []
        for word in word_records:
            word_list.append(Word(word))
        print word_list[0].word
        return word_list
 

    def get_random_list(self, length):
        random_list = random.sample(self.word_list, length)
        self.list_length = length
        self.current_list_iter = iter(random_list)
        return random_list

    def next_word(self):
        try:
            self.current_word = self.current_list_iter.next()
            self.game_canvas.itemconfig(self.progress_display, text="%d/%d"
                                   %(self.current_list.index(self.current_word) + 1,
                                   self.list_length))
            self.game_canvas.itemconfig(self.word_display, text="?", fill="#004183")
            self.game_canvas.itemconfig(self.game_canvas_image, state=HIDDEN)
            self.buttonSubmit.configure(state=NORMAL)
            self.buttonNext.configure(state=DISABLED)
            self.festival.speech(self.current_word)
        except StopIteration:
            self.list_complete()

    def list_complete(self):
        for word in self.current_list:
            print word.answer

    def replay_word(self):
       self.festival.speech(self.current_word)

    def submit_word(self, event=None):
        guess = self.entry.get()
        self.entry.delete(0, END)
        if guess == self.current_word.word:
            self.correct(guess)
        else:
            self.incorrect(guess)
        self.game_canvas.itemconfig(self.word_display, text='%s'%(self.current_word))
        self.buttonNext.configure(state=NORMAL)
        self.buttonSubmit.configure(state=DISABLED)
        self.game_canvas.itemconfig(self.game_canvas_image, state=NORMAL)
        

    def correct(self, guess):
        self.current_word.setAnswer(guess, True)
        self.game_canvas.itemconfig(self.game_canvas_image, image=self.correct_img)
        self.game_canvas.itemconfig(self.word_display, fill="#139E1C")
        self.progress_bar.increment(True)

    def incorrect(self, guess):
        self.current_word.setAnswer(guess, False)
        self.game_canvas.itemconfig(self.game_canvas_image, image=self.wrong_img)
        self.game_canvas.itemconfig(self.word_display, fill="#F30000")
        self.progress_bar.increment(False)

    def start_game(self):
        self.start_frame.pack_forget()
        self.game_frame.pack()
        self.current_word = self.current_list_iter.next()
        self.festival.speech(self.current_word)
        self.time_elapsed = 0
        self.tick()

    def tick(self):
        seconds = (self.time_elapsed)%60
        minutes = self.time_elapsed/60
        separator = ":" if seconds > 9 else ":0"
        formatted_time = "%d%s%d"%(minutes, separator, seconds)
        self.game_canvas.itemconfig(self.timer_display, text=formatted_time)
        self.time_elapsed +=1
        self.root.after(1000, self.tick)

        


    def init_gui(self):
        self.root = Tk()

        self.game_frame = Frame(self.root, height=500, width=500)

        correct_img = Image.open("correct.png")
        wrong_img  = Image.open("wrong.png")
        correct_img.thumbnail((64, 64), Image.ANTIALIAS)
        wrong_img.thumbnail((64, 64), Image.ANTIALIAS)
        self.correct_img = ImageTk.PhotoImage(correct_img, master=self.root)
        self.wrong_img = ImageTk.PhotoImage(wrong_img, master=self.root)

        self.entry = Entry(self.root, width=15, font=('Helvetica', 20, 'normal'),
                                                  justify=CENTER)
        self.entry.bind("<Return>", lambda x:self.buttonSubmit.invoke())
        self.buttonNext = Button(self.game_frame, width=10, text="Next Word",
                            command=self.next_word, state=DISABLED)
        self.buttonSubmit = Button(self.game_frame, width=10, text="Submit",
                              command=self.submit_word)
        buttonReplay = Button(self.game_frame, width=10, text="Repeat Word",
                              command=self.replay_word)
        self.game_canvas = Canvas(self.game_frame, width=600, height=250, bg="#FFFFFF")
        self.word_display = self.game_canvas.create_text((300, 125), text="?",
                           font=("Helvetica", 50, "bold"), fill="#004183")
        self.progress_display = self.game_canvas.create_text((593, 5),
                                text="%d/%d"%(1, self.list_length),
                                font=("Helvetica", 25, "bold"), anchor=NE)
        self.timer_display = self.game_canvas.create_text(10, 5, anchor=NW, font=("Helvetica", 25))
        self.progress_bar = ProgressBar(self.root, width=300, increments=len(self.current_list))
        self.game_canvas.create_window(500, 10, anchor=NE, window=self.progress_bar)
        self.game_canvas.create_window(300, 200, window=self.entry)
        self.game_canvas_image = self.game_canvas.create_image(500, 200)
        self.game_canvas.grid(row=0, column=0, columnspan=3)
        buttonReplay.grid(row=1, column=0)
        self.buttonSubmit.grid(row=1, column=1)
        self.buttonNext.grid(row=1, column=2)

        self.start_frame = Frame(self.root, height=300, width=600)
        self.start_frame.pack()
        self.start_canvas = Canvas(self.start_frame, width=600, height=250, bg="#004183")
        self.start_canvas.pack()

        self.start_canvas.create_text((10, 10), anchor=NW, text="Welcome, %s."
                                      %(self.user.username), font=("Helvetica", 15))
        buttonStart = Button(self.root, text="Start", width=10,
                                  command=self.start_game)
        self.list_menu_var = StringVar(self.root)
        self.list_menu_var.set("Random List")
        list_menu = OptionMenu(self.root, self.list_menu_var, "Random List", *self.list_list)
        list_menu.configure(width=30)
        self.start_canvas.create_window(300, 200, window=buttonStart)
        self.start_canvas.create_window(300, 150, window=list_menu)
        

        self.root.mainloop()

class ProgressBar(Canvas):
    
    def __init__(self, parent, height=30, width=150, increments=15):
        self.increments = increments
        self.height = height
        self.increment_width = width/increments-2
        print self.increment_width
        self.current_increment = 0
        Canvas.__init__(self, parent, height=height, width=width, bd=0)
        self.create_rectangle(1, 1, width-1, height-1, fill="")
        self.xview_moveto(0)
        self.yview_moveto(0)

    def increment(self, isCorrect):
        left_side = self.current_increment*(self.increment_width+2)
        right_side = left_side + self.increment_width
        fill = "#139E1C" if isCorrect else "#F30000"
        self.create_rectangle(left_side, 2, right_side, self.height-2,
                              fill=fill)
        self.current_increment += 1

def main():
    user = Button()
    user.username = "Michael"
    game = SpellingGame(1, user)

if __name__=='__main__':
    main()

