#!/usr/bin/env python

from Tkinter import Frame, Label, OptionMenu, Button, Entry, SUNKEN, LEFT, RIGHT, StringVar, N, W, E, END
from ListPane import ListPane
from SpellingDatabase import SpellingDatabase
import random

class CreateView(Frame):
    """A class describing the list creation page of the UI"""

    def __init__(self, parent, height, width, border_style, border_width,
                 background_colour):

        Frame.__init__(self, parent, height=height, width=width)

        #Connect to the word/list database 
        self.db = SpellingDatabase()
		
        #Create a frame containing a menu for choosing word category
        categorymenu_frame = Frame(self, width=340, height=30, relief=SUNKEN, bd=1)
        categorymenu_frame.pack_propagate(0)
        categorymenu_label = Label(categorymenu_frame, text="Category:")
        wordlist_title = Label(categorymenu_frame, text="Select Words")
        #Menu options: one for each category of word
        optionList = ("Child", "ESOL", "Spelling Bee", "Custom")
        self.category_v = StringVar()
        self.category_v.set(optionList[0])
        #Command causes word browser to be populated with words from chosen category
        self.category_menu = OptionMenu(categorymenu_frame, self.category_v, *optionList, command=self.update_category)
        self.category_menu.config(width=10)
        self.category_menu.pack(side=RIGHT)
        categorymenu_label.pack(side=RIGHT)
        wordlist_title.pack(side=LEFT)
        
        #Create frame for the title of the user list panel
        userlist_title_frame = Frame(self, width=340, height=30)
        userlist_title_frame.pack_propagate(0)
        userlist_title = Label(userlist_title_frame, text="Your New List")
        userlist_title_frame.grid(column=2, row=0)
        userlist_title.pack(side=LEFT)

        #Create frame for middle bar containing transfer buttons
	middlebar_frame = Frame(self, width = 70, height=400)
        middlebar_frame.grid_propagate(0)
        #Buttons transfer words from one list to the other
        transfer_right_button = Button(middlebar_frame, text="->", command=self.transfer_right)
        transfer_left_button = Button(middlebar_frame, text="<-", command=self.transfer_left)
        #Press this button to generate a random list from the current category
        random_list_button = Button(middlebar_frame, text="Create", command=self.random_list)
        random_list_label = Label(middlebar_frame, text="Random\nList")
        self.random_list_entry = Entry(middlebar_frame, width=3, justify=RIGHT)
        self.random_list_entry.insert(0, 15) 
	transfer_left_button.grid(column=0, row=1, padx=15, pady=50)
        transfer_right_button.grid(column=0, row=0, padx=15, pady=50)
        random_list_label.grid(column=0, row=2, pady=3)
        self.random_list_entry.grid(column=0, row=3, pady=3)
        random_list_button.grid(column=0, row=4, pady=3)
        middlebar_frame.grid(column=1, row=1)
        #random_list_button.grid(column=0, row=2)

        #Create frame for "Add New Word" menu
        addword_frame = Frame(self, width=340, height=150, bd=2, relief=SUNKEN)
        addword_frame.grid_propagate(0)
        addword_label = Label(addword_frame, text = "Add a new word:")
        word_label = Label(addword_frame, text="Word:")
        def_label = Label(addword_frame, text="Definition:")
        use_label = Label(addword_frame, text="Example of Use:")
        difficulty_label = Label(addword_frame, text="Difficulty:")
        #Entry boxes and an option menu allowing the user to enter attributes of the new word
        self.addword_entry = Entry(addword_frame, width = 28)
        self.adddefinition_entry = Entry(addword_frame, width=28)
        self.adduse_entry = Entry(addword_frame, width=28)
        self.difficulty_v = StringVar()
        self.difficulty_v.set("1")
        difficulty_list = range(1,9)
        self.difficulty_menu = OptionMenu(addword_frame, self.difficulty_v, *difficulty_list)
        #Pressing this button adds the new word to the database
        addword_button = Button(addword_frame, text = "Add", command = self.add_word)
        addword_label.grid(row=0, column=0, sticky=W)
        addword_button.grid(row=0, column=1, pady=2, sticky=E)
        word_label.grid(row=1, column=0, sticky=W)
        def_label.grid(row=2, column=0, sticky=W)
        use_label.grid(row=3, column=0, sticky=W)
        difficulty_label.grid(row=4, column=0, sticky=W)
        self.addword_entry.grid(row=1, column=1, pady=2, sticky=E)
        self.adddefinition_entry.grid(row=2, column=1, pady=2, sticky=E)
        self.adduse_entry.grid(row=3, column=1, pady=2, sticky=E)
        self.difficulty_menu.grid(row=4, column=1, pady=2, sticky=E)
        addword_frame.grid(column=0, row=2)
        
        #Frame for menu allowing users to save their new lists
        savelist_frame = Frame(self, width=340, height=30, bd=2, relief=SUNKEN)
        savelist_frame.pack_propagate(0)
        savelist_label = Label(savelist_frame, text="List Name:")
        #User enters the name of the new list here
        self.savelist_entry = Entry(savelist_frame, width=25)
        #Pressing this button adds the new list to the database
        savelist_button = Button(savelist_frame, text="Save", command = self.save_list)
        savelist_label.pack(side=LEFT)
        savelist_button.pack(side=RIGHT)
        self.savelist_entry.pack(side=RIGHT, padx=5)
        savelist_frame.grid(column=2, row=2, sticky=N, pady=5)

        #Create list panel for browsing the words stored in database
        self.wordbrowse_frame = ListPane(self, height=25) 
        categorymenu_frame.grid(column=0, row=0)
        self.wordbrowse_frame.grid(column=0, row=1, sticky=N)
        #Populate the list with words from database
        self.update_category()
        #Double-clicking a word has same effect as transfer button
        self.wordbrowse_frame.doubleClickFunc = self.transfer_right

        #Create list panel for holding/displaying the list being built
        self.userlist_frame = ListPane(self, height=25)
        self.userlist_frame.grid(column=2, row=1, sticky=N)
        #Double-clicking a word has same effect as transfer button
        self.userlist_frame.doubleClickFunc = self.transfer_left

    def transfer_right(self, index=None):
        """Moves a word from word browser to user list"""
        if index == None:
            index = self.wordbrowse_frame.listbox.curselection()
        if self.wordbrowse_frame.get()!=None:
            #Add selection to user list
            self.userlist_frame.insert(self.wordbrowse_frame.get())
            #Remove selection from word browser
            word_list = list(self.wordbrowse_frame.getDisplayed())
            word_list.remove(self.wordbrowse_frame.get())
            self.wordbrowse_frame.display(word_list)
            #Ensure current list contents stay visible and select the next word
            self.wordbrowse_frame.listbox.see(index)
            self.wordbrowse_frame.listbox.selection_set(index)

    def transfer_left(self, index=None):
        """Moves a word from user list back to word browser"""
        if index == None:
            index = self.userlist_frame.listbox.curselection()
        if self.userlist_frame.get()!=None:
            word_list = list(self.wordbrowse_frame.getDisplayed())
            word_list.append(self.userlist_frame.get())
            word_list.sort(key=str.lower)
            self.wordbrowse_frame.display(word_list)
            word_list = list(self.userlist_frame.getDisplayed())
            word_list.remove(self.userlist_frame.get())
            self.userlist_frame.display(word_list)
            self.userlist_frame.listbox.see(index)
            self.userlist_frame.listbox.select_set(index)

    def random_list(self):
        source_list = self.wordbrowse_frame.getDisplayed()
        list_size = int(self.random_list_entry.get())
        if list_size > len(source_list):
            list_size = len(source_list)
            self.random_list_entry.delete(0, END)
            self.random_list_entry.insert(0, list_size)
        generated_list = random.sample(source_list, list_size)
        self.userlist_frame.display(generated_list)

    def update_category(self, event=None):
        """Populates the word browser with words from the selected category"""
        category = self.category_v.get()
        if category == "Child":
            category = "CL"
        elif category == "ESOL":
            category = "AL"
        elif category == "Spelling Bee":
            category = "SB"
        else: category = "UL"
        word_records = self.db.sql("SELECT word FROM words WHERE difficulty LIKE '%s%s'"%(category, "%"))
        word_list = []
        for word in word_records:
            word_list.append(str(word[0]))
        word_list.sort(key=str.lower)
        self.wordbrowse_frame.display(word_list)

    def add_word(self):
        """Adds a new word to the database with the attributes entered by the user"""
        if self.addword_entry.get() == "":
            return
        self.db.sql("INSERT INTO words (word, definition, usage, difficulty) VALUES ('%s', '%s', '%s', 'UL%s')"%(self.addword_entry.get(), self.adddefinition_entry.get(), self.adduse_entry.get(), self.difficulty_v.get()))
        self.addword_entry.delete(0, END)
        self.adddefinition_entry.delete(0, END)
        self.adduse_entry.delete(0, END)
        #User words are added to a 'Custom' category
        self.category_v.set("Custom")
        self.update_category(None)
        self.db.commit()

    def save_list(self):
        """Adds the list contained in the user list panel to the database"""
        word_list = self.userlist_frame.getDisplayed()
        self.db.createList(word_list, self.savelist_entry.get())
        self.savelist_entry.delete(0, END)
        self.db.commit()
        
        

