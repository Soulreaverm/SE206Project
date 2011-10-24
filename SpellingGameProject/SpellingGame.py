#!/usr/bin/env python
from Tkinter import Tk, Button
from Tkconstants import *
from Festival import FestivalInterface
from SpellingDatabase import SpellingDatabase
from StartFrame import StartFrame
from GameFrame import GameFrame
from ResultsFrame import ResultsFrame
from Word import Word
from List import WordList
from ListEditor import ListEditor
from LoginFrame import LoginFrame
import random

class SpellingGame(Tk):
    """Main class for spelling aid. Manages the other screens and holds festival       and database connections"""
    def __init__(self):

        Tk.__init__(self)
        self.title('Spelling Game')
        #Estabilish database connection
        self.db = SpellingDatabase()
        #Get words from database
        self.word_list = self.get_dictionary()
        #Retrieve list of lists from db
        self.list_list = self.get_lists()
        #Start festival process
        self.festival = FestivalInterface()
        #Create screens
        self.init_gui()

    def get_lists(self):
        """Retrieve list of lists from database"""
        list_records = self.db.sql("""SELECT * FROM lists""")
        list_list = []
        for wordlist in list_records:
            list_list.append(WordList(wordlist))
        return list_list

    def update_lists(self):
        """Refresh the list-list"""
        self.list_list = self.get_lists()
            
        
    def get_dictionary(self):
        """Get dictionary words from database"""
        word_records = self.db.sql("""SELECT * FROM words WHERE
                              difficulty LIKE 'SB%'""")
        word_list = []
        for word in word_records:
            word_list.append(Word(word))
        return word_list
 

    def get_random_list(self, length):
        """Return a random list of words"""
        words = random.sample(self.word_list, length)
        return words

    def login(self, user):
        """Show the start screen as user logs in"""
        self.user = user
        self.login_frame.pack_forget()
        self.start_frame.welcomeMessage()
        self.start_frame.pack()

    def start_game(self, word_list):
        """Hide start screen and show game screen. Retrieve words for selected 
           list"""
        self.current_list = word_list
        if word_list.name != "Random List":
            word_records = self.db.getWords(word_list.name)
            self.current_list.words = [Word(word) for word in word_records]
        else:
            self.current_list.words = self.get_random_list(15)
        self.list_length = len(self.current_list.words)
        self.start_frame.pack_forget()
        self.results_frame.pack_forget()
        self.game_frame = GameFrame(self)
        self.game_frame.start()
        self.game_frame.pack()

    def show_results(self, time_elapsed):
        """Hide game frame and show results frame"""
        self.game_frame.pack_forget()
        self.results_frame.calculate(self.current_list, time_elapsed)
        self.results_frame.pack()

    def new_list(self):
        """Show start screen, hiding either results or list editor"""
        self.results_frame.pack_forget()
        self.list_editor.pack_forget()
        self.start_frame.update_list()
        self.start_frame.pack()

    def show_editor(self):
        """Hide start frame and show list editor"""
        self.start_frame.pack_forget()
        self.list_editor.pack()

    def init_gui(self):
        """Create the screens"""
        self.login_frame = LoginFrame(self)
        self.login_frame.pack()

        self.start_frame = StartFrame(self)

        self.results_frame = ResultsFrame(self)

        self.list_editor = ListEditor(self)


        self.mainloop()

def main():
    game = SpellingGame()

if __name__=='__main__':
    main()

