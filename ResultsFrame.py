from Tkinter import Frame, Button, Label
from ResultsTable import ResultsTable

class ResultsFrame(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.results_list = ResultsTable(self)
        self.results_list.grid(row=0, column=1, columnspan=2)
        buttonRetry = Button(self, text="Retry",
                             command=self.restart)
        buttonNewlist = Button(self, text="New List",
                               command=self.new_selection)
        buttonExit = Button(self, text="Quit",
                            command=self.parent.destroy)
        
        label_frame = Frame(self)
        listLabel = Label(label_frame, text="List:")
        scoreLabel = Label(label_frame, text="Score:")
        timeLabel = Label(label_frame, text="Time:")
        bestScoreLabel = Label(label_frame, text="Best Score:")
        bestTimeLabel = Label(label_frame, text="Best Time:")
        self.listName = Label(label_frame)
        self.scoreNumber = Label(label_frame)
        self.timeNumber = Label(label_frame)
        self.bestScoreNumber = Label(label_frame)
        self.bestTimeNumber = Label(label_frame)
        label_frame.grid(row=0, column=0)
        listLabel.grid(column=0, row=0)
        scoreLabel.grid(column=0, row=1)
        timeLabel.grid(column=0, row=2)
        bestScoreLabel.grid(column=0, row=3)
        bestTimeLabel.grid(column=0, row=4)
        self.listName.grid(column=1, row=0)
        self.scoreNumber.grid(column=1, row=1)
        self.timeNumber.grid(column=1, row=2)
        self.bestScoreNumber.grid(column=1, row=3)
        self.bestTimeNumber.grid(column=1, row=4)
        buttonRetry.grid(row=1, column=0)
        buttonNewlist.grid(row=1, column=1)
        buttonExit.grid(row=1, column=2)


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
        self.listName.config(text=word_list.name)
        self.scoreNumber.config(text=score)
        self.timeNumber.config(text=time_elapsed)
        self.bestScoreNumber.config(text=best_score)
        self.bestTimeNumber.config(text=best_time)
   
    def restart(self):
        self.results_list.clear()
        self.parent.start_game(self.parent.current_list)

    def new_selection(self):
        self.results_list.clear()
        self.parent.new_list()
