#!/usr/bin/env python
class TldrParser(object):
    '''Class for importing and exporting .tldr files''' 
    def __init__(self, tldrFile=None):
        '''Constructor calls readtldr if filename given
        Makes assumption that file is of right format.
        Fix needed'''
        
        self.wordlist = {}
        if tldrFile != None:
            self.readtldr(tldrFile)

    def readtldr(self, filename):
        f = open(filename)
        line_count = 0
        for line in f:
            #Get meta information from first 3 lines. Assumes correct formatting
            if line_count == 0:
                self.source = line.strip('#\n')
            elif line_count == 1:
                self.date = line.strip('#\n')
            elif line_count == 2:
                self.num_words = int(line.strip('#\n'))
            else:
                if not line.startswith('#'):
                    #comments are ignored
                    line = line.strip('\n')
                    wordline = line.split('|')
                    self.wordlist[wordline[0]] = [wordline[1], wordline[2], wordline[3]]

            line_count += 1

        f.close()
    
    def writetldr(self, filename):
        #File existence checking should be done here.
        f = open(filename, 'w')
        f.write(self.source)
        f.write(self.date)
        f.write(self.num_words)
        for word in self.wordlist.keys():
            line = "%s|%s|%s|%s\n" % (word, self.wordlist[word][0], self.wordlist[word][1], self.wordlist[word][2])
            f.write(line)
        f.close()
    
    
    '''Getters and Setters. 
    Getters should be usually only used after a readtldr() call. 
    Setters should typically used before calling writetldr().
    Setting should be enabled in constructor. Needs doing'''
    
    def getWordList(self):
        #returns a dict with a 3 item list as the value
        return self.wordlist

    def getListSize(self):
        return self.num_words

    def getDateEdited(self):
        return self.date

    def getSource(self):
        return self.source

    def setWordList(self, wordlist):
        #Takes a dict with a 3 item list as value 
        self.wordlist = wordlist

    def setListSize(self, size):
        self.num_words = "#%s\n" % (size)

    def setDateEdited(self, date_string):
        self.date = "#%s\n" % (date_string)

    def setSource(self, source):
        self.source = "#%s\n" % (source)


