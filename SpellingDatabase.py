#!/usr/bin/env python
import sqlite3
from datetime import date

class SpellingDatabase(object):
    def __init__(self):
        self.db = sqlite3.connect('spelling.db')
        self.cursor = self.db.cursor()
        database_check = self.sql("SELECT name FROM sqlite_master WHERE type='table'")
        #Check if there is a database that already exists.
        #Create the tables if the number of tables isnt what it should be.
        if len(database_check) < 4:
            self.sql("""CREATE TABLE lists (list_id INTEGER PRIMARY KEY,
                                            list_name varchar(20),
                                            source varchar(100),
                                            date_edited varchar(25),
                                            num_words NUMERIC)""")

            self.sql("""CREATE TABLE students (student_id INTEGER PRIMARY KEY,
                                               first_name varchar(20),
                                               last_name varchar(20),
                                               birthday varchar(20),
                                               comments varchar(200))""")

            self.sql("""CREATE TABLE word_list_map (word_id INTEGER, 
                                                    list_id INTEGER)""")

            self.sql("""CREATE TABLE words (word_id INTEGER PRIMARY KEY,
                                            word varchar(20),
                                            definition varchar(100),
                                            usage varchar(100),
                                            difficulty varchar(10))""")
    def sql(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def importList(self, listName, wordDict, source, date_edited, num_words):
        #check if list with same name already exists
        self.cursor.execute("select list_id from lists where list_name = '%s';" % (listName))
        word_check = self.cursor.fetchall()
        if len(word_check) > 0:
            #return 0 if listName is already taken
            return 0

        self.sql("""insert into lists (list_name, source, date_edited, num_words) 
                    values ('%s', '%s', '%s', '%s');""" % (self.duplicateSingleQuotes(listName),                                                        
                                                           self.duplicateSingleQuotes(source),
                                                           self.duplicateSingleQuotes(date_edited),
                                                           self.duplicateSingleQuotes(num_words)))
        
        list_id = self.cursor.lastrowid
        for word in wordDict.keys():
            #Check if word is already in database
            word_check = self.sql("SELECT word_id FROM words WHERE word = '%s' AND difficulty = '%s';" % (self.duplicateSingleQuotes(word), self.duplicateSingleQuotes(wordDict[word][2])))
            if len(word_check) == 0:
                self.sql("""INSERT INTO words ('word','definition','usage','difficulty') 
                          VALUES ('%s','%s','%s','%s');""" % (self.duplicateSingleQuotes(word),
                                                            self.duplicateSingleQuotes(wordDict[word][0]),
                                                            self.duplicateSingleQuotes(wordDict[word][1]),
                                                            self.duplicateSingleQuotes(wordDict[word][2])))
                word_id = self.cursor.lastrowid
            else:
                word_id = word_check[0][0]
            
            self.sql("""INSERT INTO word_list_map ('word_id', 'list_id') 
                      VALUES ('%s', '%s');""" % (word_id, list_id))
        
        #Indicate that insertion was successful
        return 1

    def createList(self, word_list, list_name):
        self.sql("INSERT INTO lists (list_name, source, date_edited, num_words) VALUES ('%s', '%s', '%s', '%d')"%(list_name, "User Created List", str(date.today()), len(word_list)))
        list_id = self.cursor.lastrowid
        for word in word_list:
            id_record = self.sql("SELECT word_id FROM words WHERE word = '%s'"%(word))
            word_id = id_record[0][0]
            self.sql("INSERT INTO word_list_map VALUES ('%d', '%d')"%(word_id, list_id))

    def getList(self, list_name):
        return self.sql("SELECT * FROM lists where list_name = '%s'" % (list_name))

    def __del__(self):
        self.db.commit()
        self.db.close()
    def getAllWords(self):
        return self.sql("SELECT * FROM words")

    def getWords(self, listName):
        return self.sql("""SELECT words.word FROM words, lists, word_list_map where lists.list_id = word_list_map.list_id 
                                                            and words.word_id = word_list_map.word_id
                                                            and lists.list_name = '%s'""" % (listName))
    def getWord(self, wordName):
        return self.sql("SELECT * from words where word='%s'" % (self.duplicateSingleQuotes(wordName)))

    def getLists(self):
        return self.sql("SELECT * FROM lists")
    
    def update_student(self, old_fname, old_lname, new_fname, new_lname, new_birthday, new_comments):
        self.sql("""UPDATE students SET first_name='%s', last_name='%s', birthday='%s', comments='%s'
                    WHERE first_name='%s' AND last_name='%s';""" % (self.duplicateSingleQuotes(new_fname), 
                                                               self.duplicateSingleQuotes(new_lname), 
                                                               self.duplicateSingleQuotes(new_birthday), 
                                                               self.duplicateSingleQuotes(new_comments), 
                                                               self.duplicateSingleQuotes(old_fname), 
                                                               self.duplicateSingleQuotes(old_lname)))
                
    
    def addStudent(self, fname, lname, birthday, comments):
        self.sql("""INSERT INTO students (first_name, last_name, birthday, comments) 
                    VALUES('%s','%s','%s','%s')""" % (self.duplicateSingleQuotes(fname),
                                                     self.duplicateSingleQuotes(lname), 
                                                     self.duplicateSingleQuotes(birthday),
                                                     self.duplicateSingleQuotes(comments)))
    def duplicateSingleQuotes(self, string):
        new_string = ""
        for char in str(string):
            if char == "'":
                new_string+=char
                new_string+="'"
            else:
                new_string+=char

        return new_string

    def commit(self):
        self.db.commit()
