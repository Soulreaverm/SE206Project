#!/usr/bin/env python
from Tkinter import Tk, Frame, W, SUNKEN, Button, Listbox, Scrollbar, OptionMenu, Entry, END, RIGHT, LEFT, BOTH, Y, Label, StringVar, N, Text, DISABLED, NORMAL
from tldrParser import TldrParser
from SpellingDatabase import SpellingDatabase
from Festival import FestivalInterface
from ListPane import ListPane
from datetime import date
import tkFileDialog, tkFont
class ListView(Frame):

    def __init__(self, parent, height, width, border_style, border_width, background_colour):
        #Call Frams's __init__
        Frame.__init__(self, parent) 
        #create the frame that holds the widgets on the left
        lists_frame = Frame(self)
        #Add custom ListPane widget
        self.lists_list_pane = ListPane(lists_frame, height = 25)
        self.lists_list_pane.singleClickFunc = self.displayWords
        #Add labels and Buttons
        lists_label = Label(lists_frame, text="Word Lists")
        import_button = Button(lists_frame, text="Import", command=self.importList)
        export_button = Button(lists_frame, text="Export", command=self.exportList)
        #Grid everything
        lists_label.grid(row=0, column=0, sticky=W, pady=3, padx=2)
        self.lists_list_pane.grid(row=1, column=0, columnspan=2)
        import_button.grid(row=2, column=0, sticky=W, padx=2)
        export_button.grid(row=2, column=0) 
        
        #create the container frame that holds the widgets on the right
        words_frame = Frame(self)
        #create custom ListPane widget
        self.words_list_pane = ListPane(words_frame,height = 25)
        self.words_list_pane.singleClickFunc = self.displayWordInfo
        #create labels and buttons
        self.speak_word_button = Button(words_frame, text="Speak Word", command=self.speakWord, state=DISABLED)
        self.speak_list_button = Button(words_frame,text="Speak List", command=self.speakList, state=DISABLED)
        stop_speech_button = Button(words_frame,text="Stop Speech", command=self.stopSpeech)
        words_label = Label(words_frame, text="Words in List")
        
        #grid everything
        words_label.grid(row=0, column=0, sticky=W, pady=3, padx=2)
        self.words_list_pane.grid(row=1, column=0, columnspan=3)
        self.speak_word_button.grid(row=2, column=0)
        self.speak_list_button.grid(row=2, column=1)
        stop_speech_button.grid(row=2, column=2)
        
        #Create the infoFrame
        info_frame = Frame(self, height=140, width=width, bd=border_width, bg=background_colour, relief=border_style)

        self.info_text = Text(info_frame, state=DISABLED, font=tkFont.Font(family="Tahoma", size=9))
        self.info_text.pack(fill=BOTH)
        
        lists_frame.grid(column=0, row=0)
        words_frame.grid(column=1, row=0)
        info_frame.grid(column=0, row=1, columnspan=2)
        info_frame.pack_propagate(0)
        
        #Create databse and Festival connections
        self.db = SpellingDatabase()
        self.fest = FestivalInterface()

        list_records = self.db.getLists()
        list_names = []
        for row in list_records:
            list_names.append(row[1])
        self.lists_list_pane.display(list_names)
        self.words_list_pane.display(['...'])


    def importList(self):
        filename = tkFileDialog.askopenfilename(filetypes = (("Tldr Files", "*.tldr"),))
        if str(filename) == "":
            return
        tldr_parse = TldrParser(filename)
        list_name = filename[:-5].split('/')[-1]
        if self.db.importList(list_name, tldr_parse.getWordList(), tldr_parse.getSource(), tldr_parse.getDateEdited(), tldr_parse.getListSize()):
            self.lists_list_pane.insert(list_name)
        else:
            print "List with that name already exists!!!"
        self.db.commit()


    def exportList(self):
        filename = tkFileDialog.asksaveasfilename(filetypes = (("Tldr Files", "*.tldr"),), initialfile = self.lists_list_pane.get())
        if str(filename) == "":
            return
        export_list = self.db.getList(self.lists_list_pane.get())[0]
        word_list = self.db.getWords(self.lists_list_pane.get())
        word_dict = {}
        for word in word_list:
            word = word[0]
            word_record = self.db.getWord(word)[0]
            word_dict[word] = [word_record[2],word_record[3],word_record[4]]
        tldr_parse = TldrParser()
        tldr_parse.setWordList(word_dict)
        tldr_parse.setSource(export_list[2])
        tldr_parse.setDateEdited(str(date.today()))
        tldr_parse.setListSize(export_list[4])
        tldr_parse.writetldr(filename)


    def speakWord(self):
        word = self.words_list_pane.get()
        self.fest.speech(word)
        
    def speakList(self):
        word_list = self.words_list_pane.getDisplayed()
        long_sentence = ""
        for word in word_list:
            long_sentence += " %s," % (word)
        self.fest.speech(long_sentence)
        
    def stopSpeech(self):
        self.fest.resetSpeech()
    
    def displayWords(self, item_index):
        word_records = self.db.getWords(self.lists_list_pane.get(item_index))
        word_names = []
        for row in word_records:
            word_names.append(str(row[1]))
        word_names.sort(key=str.lower)
        self.words_list_pane.display(word_names)
        
        list_record = self.db.getList(self.lists_list_pane.get(item_index))
        if len(list_record) > 0:
            list_record = list_record[0]
            info_string = """List: %s

Source: %s
Date Edited: %s
Number of Words in List: %s""" % (list_record[1], list_record[2], list_record[3], list_record[4])
            self.info_text.configure(state=NORMAL)
            self.info_text.delete(1.0, END)
            self.info_text.insert(1.0, info_string)
            self.info_text.configure(state=DISABLED)

            self.speak_word_button.configure(state=DISABLED)
            self.speak_list_button.configure(state=NORMAL)
        else:
            self.info_text.configure(state=NORMAL)
            self.info_text.delete(1.0, END)
            self.info_text.insert(1.0, "There are no lists in the database.\nImport one or create one")
            self.info_text.configure(state=DISABLED)

    def displayWordInfo(self, item_index): 
        word_record = self.db.getWord(self.words_list_pane.get(item_index))
        if len(word_record) > 0:
            word_record = word_record[0]
            info_string = """Word: %s

Definition: %s
Usage: "%s"
Difficulty: %s""" % (word_record[1], word_record[2], word_record[3], word_record[4])
            self.info_text.configure(state=NORMAL)
            self.info_text.delete(1.0, END)
            self.info_text.insert(1.0, info_string)
            self.info_text.configure(state=DISABLED)
            
            self.speak_word_button.configure(state=NORMAL)
    
    def update(self):        
        list_records = self.db.getLists()
        list_names = []
        for row in list_records:
            list_names.append(row[1])
        self.lists_list_pane.display(list_names)
        self.words_list_pane.display(['...'])

def main():
    root = Tk()
    list_view = ListView(root, height=600, width=800, border_style=SUNKEN, border_width=1, background_colour="white")
    list_view.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
