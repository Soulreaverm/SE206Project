#!/usr/bin/env python
from Login import Login
from SpellingGame import SpellingGame

class MainApp():
    def __init__(self):
        login = Login(self)
        game = SpellingGame(self, self.user)

    def setUser(self, user):
        self.user = user

def main():
    main = MainApp()


if __name__=='__main__':
    main()
