from Tkinter import Tk, Button, Entry, Label, Frame, StringVar, Canvas
from Festival import FestivalInterface
from SpellingDatabase import SpellingDatabase
import random

class SpellingGame:

    def __init__(self):

        self.word_list = self.get_dictionary()
        self.random_list = self.get_random_list()
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
 

    def get_random_list(self):        
       return random.sample(self.word_list, 15)
    
    def next_word(self):
        if len(self.random_list) > 0:
            self.current_word = self.random_list[0]
            self.canvas.itemconfig(self.canvas_text, text=self.current_word)
            self.festival.speech(self.current_word)
            self.random_list.pop(0)
        else:
            self.random_list = self.get_random_list()
            self.next_word()

    def init_gui(self):
        root = Tk()
        frame = Frame(root, height=500, width=500)
        frame.pack()

        self.entry_text = StringVar()
        entry = Entry(frame, width=15, textvariable=self.entry_text)
        button = Button(frame, width=10, text="Submit", command=self.next_word)
        self.canvas = Canvas(frame, width=250, height=50, bg="#FFFFFF")
        self.canvas_text = self.canvas.create_text((125, 25), text="?", font=("Helvetica", 20, "bold"))
        self.canvas.grid(row=0, column=0, columnspan=2)
        entry.grid(row=1, column=0)
        button.grid(row=1, column=1)
        
        root.mainloop()        

def main():
    game = SpellingGame()

if __name__=='__main__':
    main()

