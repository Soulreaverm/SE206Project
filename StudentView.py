#!/usr/bin/env python
from Tkinter import Tk, Frame, Label, Button, N,E,W, OptionMenu, StringVar, LEFT, Entry, Text, END
from ListPane import ListPane
from SpellingDatabase import SpellingDatabase
class StudentView(Frame):
    def __init__(self, parent, width, height):
        #Call the initializer of the class we're inheriting from
        Frame.__init__(self, parent)

        self.db = SpellingDatabase()

        student_list_frame = Frame(self)
        
        self.student_listpane = ListPane(student_list_frame, height=30, width = 35)
        self.student_listpane.singleClickFunc=self.display_details
        sort_options_list = ['First Name', 'Last Name']
        self.sort_v = StringVar()
        self.sort_v.set(sort_options_list[1])
        self.sort_option = OptionMenu(student_list_frame, self.sort_v, *sort_options_list, command=self.update_sort) 
        sort_label = Label(student_list_frame, text="Sort by:")
        title_label = Label(student_list_frame, text="Student Details")

        title_label.grid(row=0, column=0, sticky=W,pady=5)
        self.student_listpane.grid(row=1, column=0, columnspan=2)
        sort_label.grid(row=2, column=0, sticky=W, padx = 2)
        self.sort_option.grid(row=2, column=0, padx=50, sticky=W)
        
        student_details_frame=Frame(self) 
        
        fname_label = Label(student_details_frame, text="First Name:")
        lname_label = Label(student_details_frame, text="Last Name:")
        age_label = Label(student_details_frame, text="Birthday:")
        comments_label = Label(student_details_frame, text="Comments")

        self.fname_entry = Entry(student_details_frame, width=30)
        self.lname_entry = Entry(student_details_frame, width=30)
        self.age_entry = Entry(student_details_frame, width=30)
        self.comments_text = Text(student_details_frame, width=65, height=10)
        enable_edit_button = Button(student_details_frame, text="Edit Details", command=self.update_student)
        add_student_button = Button(student_details_frame, text="Add Student", command=self.insert_student)
        remove_student_button = Button(student_details_frame, text="Remove Student", command=self.remove_student)

        fname_label.grid(row=0, column=0, sticky=W, padx=3)
        lname_label.grid(row=1, column=0, sticky=W, padx=3)
        age_label.grid(row=2, column=0, sticky=W, padx=3)
        comments_label.grid(row=3, column=0, sticky=W, padx=3)
        self.fname_entry.grid(row=0, column=1, sticky=W)
        self.lname_entry.grid(row=1, column=1, sticky=W)
        self.age_entry.grid(row=2, column=1, sticky=W)
        self.comments_text.grid(row=4, column=0, columnspan=2, sticky=W, padx=10)
        enable_edit_button.grid(row=5, column=0, padx=7)
        add_student_button.grid(row=5, column=1, sticky=W)
        remove_student_button.grid(row=5, column=1, sticky=W, padx=110)
        
        student_list_frame.pack(side=LEFT)
        student_details_frame.pack(side=LEFT)

        #Load student table from database
        student_records = self.db.sql("SELECT last_name, first_name From students ORDER By last_name")
        names_list = []
        for record in student_records:
            names_list.append("%s, %s" % (record[0], record[1]))
        
        self.student_listpane.display(names_list)
    
    def update_sort(self, option):
        order_by=""
        if option == "First Name": order_by = 'first_name'
        else: order_by = 'last_name'
        
        student_records = self.db.sql("SELECT last_name, first_name From students ORDER By %s" % order_by)
        names_list = []
        for record in student_records:
            if option == "First Name": names_list.append("%s %s" % (record[1], record[0]))
            else: names_list.append("%s, %s" % (record[0], record[1]))
        self.student_listpane.display(names_list)
    
    def display_details(self, item_index):
        if len(self.student_listpane.getDisplayed()) == 0: return
        if self.fname_entry.get() == "" and self.lname_entry.get() == "": return
        self.selected_student = item_index
        first_name = ""
        last_name = ""
        if self.sort_v.get() == "First Name":
            first_name, last_name = self.student_listpane.get(item_index).split(' ')
        else:
            last_name, first_name = self.student_listpane.get(item_index).split(', ')
        student_record = self.db.sql("SELECT * from students where first_name = '%s' and last_name = '%s'" % (first_name, last_name))[0]
        self.fname_entry.delete(0, END)
        self.fname_entry.insert(0, first_name)
        self.lname_entry.delete(0, END)
        self.lname_entry.insert(0, last_name)
        self.age_entry.delete(0, END)
        self.age_entry.insert(0, student_record[3])
        self.comments_text.delete(1.0, END)
        self.comments_text.insert(1.0, student_record[4])

    def remove_student(self):
        if self.fname_entry.get() == "" and self.lname_entry.get() == "":
            return
        first_name = ""
        last_name = ""
        if len(self.student_listpane.get(self.selected_student))==0: return
        if self.sort_v.get() == "First Name":
            first_name, last_name = self.student_listpane.get(self.selected_student).split(' ')
        else:
            last_name, first_name = self.student_listpane.get(self.selected_student).split(', ')
        self.db.sql("DELETE FROM students where first_name = '%s' and last_name = '%s'" % (first_name, last_name))
        self.db.commit()
        self.update_sort(self.sort_v.get())
    
    def update_student(self):
        if len(self.student_listpane.getDisplayed()) == 0: return
        if self.fname_entry.get() == "" and self.lname_entry.get() == "": return

        old_first_name = ""
        old_last_name = ""
        if self.sort_v.get() == "First Name":
            old_first_name, old_last_name = self.student_listpane.get(self.selected_student).split(' ')
        else:
            old_last_name, old_first_name = self.student_listpane.get(self.selected_student).split(', ')
        
        self.db.update_student(old_first_name, old_last_name, self.fname_entry.get(), self.lname_entry.get(), self.age_entry.get(), self.comments_text.get(1.0,END))
        self.db.commit()
        self.update_sort(self.sort_v.get())
            
    def insert_student(self):
        current_students = self.student_listpane.getDisplayed()
        if self.fname_entry.get() == "" and self.lname_entry.get() == "":
            return
        for student in current_students:
            first_name = ""
            last_name = ""
            if self.sort_v.get() == "First Name":
                first_name, last_name = student.split(' ')
            else:
                last_name, first_name = student.split(', ')
           
            if first_name == self.fname_entry.get() and last_name == self.lname_entry.get():
                return

        self.db.addStudent(self.fname_entry.get(), self.lname_entry.get(), self.age_entry.get(), self.comments_text.get(1.0, END))
        self.db.commit()
        self.update_sort(self.sort_v.get())

def main():
    root = Tk()
    sv = StudentView(root, 800, 600)
    sv.pack()
    root.mainloop()
if __name__ == "__main__":
    main()
