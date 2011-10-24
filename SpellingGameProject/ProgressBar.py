from Tkinter import Canvas

class ProgressBar(Canvas):
    """A custom progress bar widget. Displays rectangles of appropriate colour 
       as words are completed""" 
    def __init__(self, parent, height=30, width=150, increments=15):
        self.increments = increments
        self.height = height
        self.increment_width = width/increments-2
        self.current_increment = 0
        Canvas.__init__(self, parent, height=height, width=width, bd=0)
        self.create_rectangle(1, 1, width-1, height-1, fill="")
        self.xview_moveto(0)
        self.yview_moveto(0)

    def increment(self, isCorrect):
        """Draw a rectangle of appropriate shape and colour to fill the next 
           segment of the bar"""
        left_side = self.current_increment*(self.increment_width+2)
        right_side = left_side + self.increment_width
        fill = "#139E1C" if isCorrect else "#F30000"
        self.create_rectangle(left_side, 2, right_side, self.height-2,
                              fill=fill)
        self.current_increment += 1

