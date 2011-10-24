#!/usr/bin/env python
from Tkinter import Tk, Button, Entry, Frame, LEFT, END
import tkFileDialog

class ButtonEntry(Frame):
    """A widget for opening a file dialog for tldr files"""
    def __init__(self, parent, width=20):
        Frame.__init__(self, parent)

        self.browseButton = Button(self, text="Browse", command=self.browse)
        self.fileEntry = Entry(self, width=width)

        self.browseButton.pack(side=LEFT)
        self.fileEntry.pack(side=LEFT)

    def browse(self):
        filename = tkFileDialog.askopenfilename(filetypes = (("Tldr Files", "*.tldr"),))
        if filename:
            self.filename = filename
            self.fileEntry.delete(0, END)
            width = int(self.fileEntry['width'])
            if len(filename) > width:
                filename = "...%s" % (filename[-width:])
            self.fileEntry.insert(0, filename)

    def get(self):
        return self.filename

def main():
    root = Tk()
    be = ButtonEntry(root, width=30)
    be.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
