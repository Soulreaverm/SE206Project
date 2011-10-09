from Tkinter import Frame, Button, Canvas, OptionMenu, StringVar
from Tkconstants import *


class StartFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.start_canvas = Canvas(self, width=600, height=250, bg="#004183")
        self.start_canvas.pack()

        self.start_canvas.create_text((10, 10), anchor=NW, text="Welcome, %s."
                                      %(self.parent.user.username),
                                      font=("Helvetica", 15))
        buttonStart = Button(self, text="Start", width=10,
                                  command=self.start)
        self.list_menu_var = StringVar(self)
        self.list_menu_var.set("Random List")
        list_menu = OptionMenu(self, self.list_menu_var, "Random List", *self.parent.list_list)
        list_menu.configure(width=30)
        self.start_canvas.create_window(300, 200, window=buttonStart)
        self.start_canvas.create_window(300, 150, window=list_menu)


    def start(self):
        self.parent.start_game(self.list_menu_var.get())
