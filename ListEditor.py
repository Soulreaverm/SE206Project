#!/usr/bin/env python
from Tkinter import Tk, Frame, Label, SUNKEN, W, LEFT, Button
from ListView import ListView
from CreateView import CreateView
from StudentView import StudentView
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

    
        nav_frame.grid(column=0, row=0)
        content_frame.grid(column=1, row=0)
        nav_frame.grid_propagate(0)
        content_frame.pack_propagate(0)

        #Create fonts for navLabels
        fontMouseOver = tkFont.Font(family="Helvetica", size=14, underline=True)
        fontMouseOut = tkFont.Font(family="Helvetica", size=14, underline=False)

        #Creating Navigation Labels
        lNavStudentRecords = Label(nav_frame, 
                               text="Student Records", 
                               bg="white", 
                               font=fontMouseOut, 
                               bd=border_width, 
                               relief=border_style, 
                               width=20)
        lNavViewLists = Label(nav_frame, 
                          text="View Word Lists", 
                          bg="white", 
                          font=fontMouseOut, 
                          bd=border_width, 
                          relief=border_style, 
                          width=20)

        lNavCreateLists = Label(nav_frame, 
                            text="Create Word Lists", 
                            bg="white",
                            font=fontMouseOut, 
                            bd=border_width, 
                            relief=border_style, 
                            width=20)

        buttonBack=Button(nav_frame, text="Back", command=self.parent.new_list)
    
        #Binding Mouse events to the Labels
        #Mouse Clicks
        lNavViewLists.bind("<Button-1>", partial(self.switch_frame, 2))
        lNavCreateLists.bind("<Button-1>", partial(self.switch_frame, 1))
        lNavStudentRecords.bind("<Button-1>", partial(self.switch_frame, 3))
        #Mouse Movements
        lNavViewLists.bind("<Enter>", lambda(event):
            lNavViewLists.configure(font=fontMouseOver))
        lNavCreateLists.bind("<Enter>", lambda(event):
            lNavCreateLists.configure(font=fontMouseOver))
        lNavViewLists.bind("<Leave>", lambda(event):
            lNavViewLists.configure(font=fontMouseOut))
        lNavCreateLists.bind("<Leave>", lambda(event):
            lNavCreateLists.configure(font=fontMouseOut))
        lNavStudentRecords.bind("<Enter>", lambda(event):
            lNavStudentRecords.configure(font=fontMouseOver))
        lNavStudentRecords.bind("<Leave>", lambda(event):
            lNavStudentRecords.configure(font=fontMouseOut))
        #Gridding the labels
        #lNavStudentRecords.grid(column=0, row=0)
        lNavViewLists.grid(column=0,row=1)
        lNavCreateLists.grid(column=0, row=2)
        buttonBack.grid(column=0, row=3)
    
        #Creating the two views we have so far 
        self.viewcreate = CreateView(content_frame, default_height, 800,
                                border_style, border_width, background_colour)

        self.viewlists = ListView(content_frame, default_height, 800,
                                border_style, border_width, background_colour)
        self.viewlists.pack()

        self.viewstudents = StudentView(content_frame, 800, default_height)

    def switch_frame(frameNumber, event):
        if frameNumber == 1:
            self.viewlists.pack_forget()
            self.viewcreate.pack()
            self.viewstudents.pack_forget()
            lNavViewLists.configure(bg="white", fg="black")
            lNavCreateLists.configure(bg="#DDDDDD", fg="#8800AA")
            lNavStudentRecords.configure(bg="white", fg="black")
            self.viewcreate.update_category()
        elif frameNumber == 2:
            self.viewcreate.pack_forget()
            self.viewlists.pack()
            self.viewstudents.pack_forget()
            lNavCreateLists.configure(bg="white", fg="black")
            lNavViewLists.configure(bg="#DDDDDD", fg="#8800AA")
            lNavStudentRecords.configure(bg="white", fg="black")
            self.viewlists.update()
        else:
            self.viewcreate.pack_forget()
            self.viewlists.pack_forget()
            self.viewstudents.pack()
            lNavCreateLists.configure(bg="white", fg="black")
            lNavViewLists.configure(bg="white", fg="black")
            lNavStudentRecords.configure(bg="#DDDDDD", fg="#8800AA")



if __name__=='__main__':
    main()
