from Tkinter import Frame, Button, Canvas, OptionMenu, StringVar
from Tkconstants import *

class StartFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.start_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
        self.start_canvas.pack()

        self.start_canvas.create_text((10, 10), anchor=NW, text="Welcome, %s."
                                      %(self.parent.user.username),
                                      font=("Helvetica", 15))
        buttonStart = Button(self, text="Start", width=10,
                                  command=self.start)
        buttonEdit = Button(self, text="Edit Lists",
                            command=self.parent.show_editor)
        self.list_menu_var = StringVar(self)
        self.list_menu_var.set("Random List")
        list_menu = OptionMenu(self, self.list_menu_var,
                               *self.parent.list_list, command=self.update)
        list_menu.configure(width=30)
        self.start_canvas.create_window(300, 200, window=buttonStart)
        self.start_canvas.create_window(300, 150, window=list_menu)
        self.start_canvas.create_window(520, 230, window=buttonEdit)
        self.start_canvas.create_text(300, 100, font=("Helvetica", 25),
                                      text="Select a list:")
        self.update()


    def start(self):
        self.parent.start_game(self.selected_list)

    def update(self, event=None):
        list_name = self.list_menu_var.get()
        for word_list in self.parent.list_list:
            if word_list.name == list_name:
                self.selected_list = word_list
            
