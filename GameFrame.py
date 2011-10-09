from Tkinter import Frame, Button, Canvas, Entry
from Tkconstants import *
from PIL import Image, ImageTk
from ProgressBar import ProgressBar
class GameFrame(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent    
        
        correct_img = Image.open("correct.png")
        wrong_img  = Image.open("wrong.png")
        correct_img.thumbnail((64, 64), Image.ANTIALIAS)
        wrong_img.thumbnail((64, 64), Image.ANTIALIAS)
        self.correct_img = ImageTk.PhotoImage(correct_img, master=self)
        self.wrong_img = ImageTk.PhotoImage(wrong_img, master=self)

        self.entry = Entry(self.parent, width=15, font=('Helvetica', 20, 'normal'),
                                                  justify=CENTER)
        self.entry.bind("<Return>", lambda x:self.buttonSubmit.invoke())
        self.buttonNext = Button(self, width=10, text="Next Word",
                            command=self.next_word, state=DISABLED)
        self.buttonSubmit = Button(self, width=10, text="Submit",
                              command=self.submit_word)
        buttonReplay = Button(self, width=10, text="Repeat Word",
                              command=self.replay_word)
        self.game_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
        self.word_display = self.game_canvas.create_text((300, 125), text="?",
                           font=("Helvetica", 50, "bold"), fill="#004183")
        self.progress_display = self.game_canvas.create_text((593, 5),
                                text="%d/%d"%(1, self.parent.list_length),
                                font=("Helvetica", 25, "bold"), anchor=NE)
        self.timer_display = self.game_canvas.create_text(10, 5, anchor=NW,
                                                        font=("Helvetica", 25))
        self.progress_bar = ProgressBar(self, width=300,
                                       increments=len(self.parent.current_list))
        self.game_canvas.create_window(500, 10, anchor=NE, window=self.progress_bar)
        self.game_canvas.create_window(300, 200, window=self.entry)
        self.game_canvas_image = self.game_canvas.create_image(500, 200)
        self.game_canvas.grid(row=0, column=0, columnspan=3)
        buttonReplay.grid(row=1, column=0)
        self.buttonSubmit.grid(row=1, column=1)
        self.buttonNext.grid(row=1, column=2)

    def start(self):
        self.current_list_iter = iter(self.parent.current_list)
        self.current_word = self.current_list_iter.next()
        self.parent.festival.speech(self.current_word)
        self.time_elapsed = 0
        self.tick()

    def next_word(self):
        try:
            self.current_word = self.current_list_iter.next()
            index = self.parent.current_list.index(self.current_word) + 1
            self.game_canvas.itemconfig(self.progress_display, text="%d/%d"
                                   %(index, self.parent.list_length))
            if index == self.parent.list_length:
                self.buttonNext.configure(text="Finish")
            self.game_canvas.itemconfig(self.word_display, text="?", fill="#004183")
            self.game_canvas.itemconfig(self.game_canvas_image, state=HIDDEN)
            self.buttonSubmit.configure(state=NORMAL)
            self.buttonNext.configure(state=DISABLED)
            self.parent.festival.speech(self.current_word)
        except StopIteration:
            self.list_complete()

    def list_complete(self):
        self.parent.after_cancel(self.timer)
        self.parent.show_results()
        

    def replay_word(self):
       self.parent.festival.speech(self.current_word)

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

    def tick(self):
        seconds = (self.time_elapsed)%60
        minutes = self.time_elapsed/60
        separator = ":" if seconds > 9 else ":0"
        formatted_time = "%d%s%d"%(minutes, separator, seconds)
        self.game_canvas.itemconfig(self.timer_display, text=formatted_time)
        self.time_elapsed +=1
        self.timer = self.parent.after(1000, self.tick)

