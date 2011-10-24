#!/usr/bin/env python

from Tkinter import Tk, Frame, Listbox, Scrollbar, LEFT, BOTH, RIGHT, Y, END, TclError

class ListPane(Frame):
    """A ListPane is a widget for holding a list of words, incorporating a scrollbar"""
    
    def __init__(self, parent, height=35, width=40):
        Frame.__init__(self, parent)
        
        #Create a scrollbar so that list can be of arbitrary length
        scrollbar = Scrollbar(self)
        #Create a listbox to hold/display the word list
        self.listbox  = Listbox(self, height = height, width = width, 
        yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview)
        self.listbox.pack(side=LEFT, fill = BOTH)
        scrollbar.pack(side=RIGHT, fill = Y)
        
        #Allow the widget to react to single or double clicks
        self.listbox.bind("<Double-Button-1>", self.doubleclicked)
        self.listbox.bind("<Button-1>", self.singleclicked)

    def remove(self, itemindex):
        """Removes the word at the given index of the list"""
        self.listbox.delete(itemindex, itemindex)

    def get(self, index=None):
        """Get the currently selected word"""
        try:
            if index!=None:
                return self.listbox.get(index)
            else: return self.get(self.listbox.curselection())
        except TclError:
            return None

    def getDisplayed(self):
        """Get a list of all words currently contained in the ListPane"""
        return self.listbox.get(0,END)

    def insert(self, item):
        """Insert a word into the list"""
        self.listbox.insert(END, item) 

    def display(self, itemlist):
        """Pass a list to this method and the contents will be displayed in the ListPane"""
        self.listbox.delete(0, END)
        for item in itemlist:
            self.listbox.insert(END, item)

    def doubleclicked(self, event):
        """Called when widget is double-clicked. Template method that calls doubleClickFunc"""
        try:
            itemindex = self.listbox.curselection()
            self.doubleClickFunc(itemindex)
        except TclError:
            pass
    
    def doubleClickFunc(self, itemindex):
        """This method should be replaced on specific instances of ListPane. 
           Defines the behaviour of widget when double-clicked"""
        pass
    
    def singleclicked(self, event):
        """Called when widget is single-clicked. Template method that calls singleClickFunc"""
        self.singleClickFunc(self.listbox.index("@%d,%d" % (event.x, event.y)))

    def singleClickFunc(self, itemindex):
        """This method should be replaced on specific instances of ListPane
           Defines the behaviour of widget when single-clicked"""
        pass
