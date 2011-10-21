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

    def __init__(self):

        Tk.__init__(self)
        self.title('Spelling Game')
        self.db = SpellingDatabase()
        self.word_list = self.get_dictionary()
        self.list_list = self.get_lists()
        self.festival = FestivalInterface()
        self.init_gui()

    def get_lists(self):
        list_records = self.db.sql("""SELECT * FROM lists""")
        list_list = []
        for wordlist in list_records:
            list_list.append(WordList(wordlist))
        return list_list

    def update_lists(self):
        self.list_list = self.get_lists()
            
        
    def get_dictionary(self):
        word_records = self.db.sql("""SELECT * FROM words WHERE
                              difficulty LIKE 'SB%'""")
        word_list = []
        for word in word_records:
            word_list.append(Word(word))
        return word_list
 

    def get_random_list(self, length):
        words = random.sample(self.word_list, length)
        return words

    def login(self, user):
        self.user = user
        self.login_frame.pack_forget()
        self.start_frame.welcomeMessage()
        self.start_frame.pack()

    def start_game(self, word_list):
        self.current_list = word_list
        if word_list.name != "Random List":
            word_records = self.db.getWords(word_list.name)
            self.current_list.words = [Word(word) for word in word_records]
        else:
            self.current_list.words = self.get_random_list(15)
        self.list_length = len(self.current_list.words)
        self.start_frame.pack_forget()
        self.results_frame.pack_forget()
        self.game_frame.pack()
        self.game_frame.start()

    def show_results(self, time_elapsed):
        self.game_frame.pack_forget()
        self.results_frame.calculate(self.current_list, time_elapsed)
        self.results_frame.pack()

    def new_list(self):
        self.results_frame.pack_forget()
        self.list_editor.pack_forget()
        self.start_frame.update_list()
        self.start_frame.pack()

    def show_editor(self):
        self.start_frame.pack_forget()
        self.list_editor.pack()

    def init_gui(self):

        self.login_frame = LoginFrame(self)
        self.login_frame.pack()

        self.game_frame = GameFrame(self)

        self.start_frame = StartFrame(self)

        self.results_frame = ResultsFrame(self)

        self.list_editor = ListEditor(self)


        self.mainloop()

def main():
    game = SpellingGame()

if __name__=='__main__':
    main()

