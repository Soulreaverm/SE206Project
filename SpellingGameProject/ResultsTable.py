from Tkinter import Tk, Frame, Canvas, Scrollbar
from Tkconstants import *

class ResultsTable(Frame):
    """A custom table widget which displays words alongside the users guesses"""
    def __init__(self, parent, width=400, height=200):

        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=width, height=height, bg="#FFFFFF")
        self.canvas.configure(bd=2, relief=SUNKEN)
        self.canvas.pack(side=LEFT)
        self.centre_line = self.canvas.create_line(0, 0, 0, 0)
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.configure(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0,                               width, height))
        self.width=width
        self.height_in_lines = height/18
        self.item_count = 0
        self.font = ("Helvetica", 12)

    def add_word(self, word):
        """Add a word to the table"""
        top = 20*self.item_count
        if top > 200:
            #If necessary extend scroll region downwards
            self.canvas.configure(scrollregion=(0, 0, self.width, top+20))
        colour = "#139E1C" if word.isCorrect else "#F30000"
        #Draw the word in the left column
        self.canvas.create_text(2, top, anchor=NW, text=word, font=self.font)
        #Draw the guess in the right column
        self.canvas.create_text(self.width/2+2, top, anchor=NW, text=word.answer, font=self.font, fill=colour)
        #Draw a line to separate this row from those below
        self.canvas.create_line(0, top+19, self.width, top+19)
        #Extend centre line of tablr
        self.canvas.coords(self.centre_line, self.width/2, 0, self.width/2,
                           top+19)
        self.item_count += 1

    def add_list(self, word_list):
        """Add a list to the table"""
        for word in word_list:
            self.add_word(word)

    def clear(self):
        """Clear the table of all words"""
        self.item_count = 0
        self.canvas.delete(ALL)


def main():
    root = Tk()
    test = ResultsTable(root)
    root.word = "collated"
    root.answer = "collted"
    root.isCorrect = True
    for i in range(15):
        test.add_word(root)
    test.pack()

    root.mainloop()

if __name__=='__main__':
    main()
