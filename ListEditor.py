#!/usr/bin/env python
from Tkinter import Tk, Frame, Label, SUNKEN, W, LEFT, Button
from ListView import ListView
from CreateView import CreateView
from functools import partial
import tkFont

class ListEditor(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        border_width = 1
        border_style = SUNKEN
        background_colour = "#FFFFFF"
        default_height=600

        nav_frame = Frame(self, height=default_height,
                          width=200,
                          bd=border_width,
                          relief=border_style,
                          bg=background_colour)

        content_frame = Frame(self, height=default_height, 
                          width=804, 
                          bd=border_width,
                          relief=border_style)
        content_frame.parent = parent

    
        nav_frame.grid(column=0, row=0)
        content_frame.grid(column=1, row=0)
        nav_frame.grid_propagate(0)
        content_frame.pack_propagate(0)

        #Create fonts for navLabels
        fontMouseOver = tkFont.Font(family="Helvetica", size=14, underline=True)
        fontMouseOut = tkFont.Font(family="Helvetica", size=14, underline=False)

        #Creating Navigation Labels
        self.lNavStudentRecords = Label(nav_frame, 
                               text="Student Records", 
                               bg="white", 
                               font=fontMouseOut, 
                               bd=border_width, 
                               relief=border_style, 
                               width=20)
        self.lNavViewLists = Label(nav_frame, 
                          text="View Word Lists", 
                          bg="white", 
                          font=fontMouseOut, 
                          bd=border_width, 
                          relief=border_style, 
                          width=20)

        self.lNavCreateLists = Label(nav_frame, 
                            text="Create Word Lists", 
                            bg="white",
                            font=fontMouseOut, 
                            bd=border_width, 
                            relief=border_style, 
                            width=20)

        buttonBack=Button(nav_frame, text="Back", command=self.parent.new_list)
    
        #Binding Mouse events to the Labels
        #Mouse Clicks
        self.lNavViewLists.bind("<Button-1>", partial(self.switch_frame, 2))
        self.lNavCreateLists.bind("<Button-1>", partial(self.switch_frame, 1))
        self.lNavStudentRecords.bind("<Button-1>", partial(self.switch_frame, 3))
        #Mouse Movements
        self.lNavViewLists.bind("<Enter>", lambda(event):
            self.lNavViewLists.configure(font=fontMouseOver))
        self.lNavCreateLists.bind("<Enter>", lambda(event):
            self.lNavCreateLists.configure(font=fontMouseOver))
        self.lNavViewLists.bind("<Leave>", lambda(event):
            self.lNavViewLists.configure(font=fontMouseOut))
        self.lNavCreateLists.bind("<Leave>", lambda(event):
            self.lNavCreateLists.configure(font=fontMouseOut))
        self.lNavStudentRecords.bind("<Enter>", lambda(event):
            self.lNavStudentRecords.configure(font=fontMouseOver))
        self.lNavStudentRecords.bind("<Leave>", lambda(event):
            self.lNavStudentRecords.configure(font=fontMouseOut))
        #Gridding the labels
        #self.lNavStudentRecords.grid(column=0, row=0)
        self.lNavViewLists.grid(column=0,row=1)
        self.lNavCreateLists.grid(column=0, row=2)
        buttonBack.grid(column=0, row=3)
    
        #Creating the two views we have so far 
        self.viewcreate = CreateView(content_frame, default_height, 800,
                                border_style, border_width, background_colour)

        self.viewlists = ListView(content_frame, default_height, 800,
                                border_style, border_width, background_colour)
        self.viewlists.pack()


    def switch_frame(self, frameNumber, event):
        if frameNumber == 1:
            self.viewlists.pack_forget()
            self.viewcreate.pack()
            self.lNavViewLists.configure(bg="white", fg="black")
            self.lNavCreateLists.configure(bg="#DDDDDD", fg="#8800AA")
            self.lNavStudentRecords.configure(bg="white", fg="black")
            self.viewcreate.update_category()
        elif frameNumber == 2:
            self.viewcreate.pack_forget()
            self.viewlists.pack()
            self.lNavCreateLists.configure(bg="white", fg="black")
            self.lNavViewLists.configure(bg="#DDDDDD", fg="#8800AA")
            self.lNavStudentRecords.configure(bg="white", fg="black")
            self.viewlists.update()
        else:
            self.viewcreate.pack_forget()
            self.viewlists.pack_forget()
            self.lNavCreateLists.configure(bg="white", fg="black")
            self.lNavViewLists.configure(bg="white", fg="black")
            self.lNavStudentRecords.configure(bg="#DDDDDD", fg="#8800AA")



if __name__=='__main__':
    main()
