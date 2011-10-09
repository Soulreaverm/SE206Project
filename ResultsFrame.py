from Tkinter import Frame, Button
from ResultsTable import ResultsTable

class ResultsFrame(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.results_list = ResultsTable(self)
        self.results_list.grid(row=0, column=0, columnspan=3)
        buttonRetry = Button(self, text="Retry",
                             command=self.parent.start_game)
        buttonNewlist = Button(self, text="New List",
                               command=self.parent.new_list)
        buttonExit = Button(self, text="Quit",
                            command=self.parent.destroy)
        buttonRetry.grid(row=1, column=0)
        buttonNewlist.grid(row=1, column=1)
        buttonExit.grid(row=1, column=2) 

