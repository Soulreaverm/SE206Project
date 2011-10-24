from Tkinter import Frame, Button, Label, Canvas
from Tkconstants import *
from ResultsTable import ResultsTable

class ResultsFrame(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.results_list = ResultsTable(self.parent, height=160, width=250)
        buttonRetry = Button(self.parent, text="Retry", width=10,
                             command=self.restart)
        buttonNewlist = Button(self.parent, text="New List", width=10,
                               command=self.new_selection)
        buttonExit = Button(self.parent, text="Quit", width=10,
                            command=self.parent.destroy)
        self.results_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
        font = ("Helvetica", 20)
        self.results_canvas.create_text(300, 15, text="Results", fill="#004183",
                                        font=font)
        self.results_canvas.create_window(310, 35, window=self.results_list,
                                          anchor=NW)
        self.results_canvas.create_window(150, 230, window=buttonRetry)
        self.results_canvas.create_window(300, 230, window=buttonNewlist)
        self.results_canvas.create_window(450, 230, window=buttonExit)
        self.results_canvas.create_text(25, 55, font=font, text="List:",
                                        anchor=W)
        self.results_canvas.create_text(25, 85, font=font, text="Score:",
                                        anchor=W)
        self.results_canvas.create_text(25, 115, font=font, text="Time:",
                                        anchor=W)
        self.results_canvas.create_text(25, 145, font=font, text="Best Score:",
                                        anchor=W)
        self.results_canvas.create_text(25, 175, font=font, text="Best Time:",
                                        anchor=W)
        self.list_name = self.results_canvas.create_text(300, 55, font=font,
                                                         anchor=E)
        self.score_number = self.results_canvas.create_text(300, 85, font=font,
                                                            anchor=E)
        self.time_number = self.results_canvas.create_text(300, 115, font=font,
                                                           anchor=E)
        self.best_score = self.results_canvas.create_text(300, 145, font=font,
                                                          anchor=E)
        self.best_time = self.results_canvas.create_text(300, 175, font=font,
                                                         anchor=E)
        self.results_canvas.pack()
        
    def calculate(self, word_list, time_elapsed):
        score = 0
        user_id = self.parent.user.uid
        list_id = word_list.l_id
        self.results_list.add_list(word_list.words)
        for word in word_list.words:
            if word.isCorrect:
                score += 1
        previous_records = self.parent.db.sql("""SELECT best_score, best_time 
                           FROM user_list_map WHERE list_id = '%d'
                           AND user_id = '%d'"""
                           %(list_id, user_id))
        
        try:
            best_score = max(score, previous_records[0][0])
            best_time = min(time_elapsed, previous_records[0][1])
            self.parent.db.sql("""UPDATE user_list_map SET best_score='%d',
                           best_time='%d' WHERE list_id = '%d' AND
                           user_id = '%d'"""
                           %(best_score, best_time, list_id, user_id))
        except IndexError:
            best_score = score
            best_time = time_elapsed
            print "Creating"
            self.parent.db.sql("""INSERT INTO user_list_map VALUES
                               ('%d', '%d', '%d', '%d')"""
                               %(user_id, list_id, best_score, best_time))
        self.results_canvas.itemconfig(self.list_name, text=word_list.name)
        self.results_canvas.itemconfig(self.score_number, text=score)
        self.results_canvas.itemconfig(self.time_number, text=time_elapsed)
        self.results_canvas.itemconfig(self.best_score, text=best_score)
        self.results_canvas.itemconfig(self.best_time, text=best_time)
   
    def restart(self):
        self.results_list.clear()
        self.parent.start_game(self.parent.current_list)

    def new_selection(self):
        self.results_list.clear()
        self.parent.new_list()
