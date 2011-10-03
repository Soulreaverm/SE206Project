#!/usr/bin/python
from functools import partial
from Tkinter import Tk, Button, Entry
import subprocess, os, signal, tkMessageBox
class FestivalInterface:
    #The FetivalObject contructor creating the popen object
    #and setting the audio mode on festival so that it doesn't close after one (Say Text) command. 
    #A problem on Natty Narwhal
    def __init__(self):
        try:
            self.p = subprocess.Popen(["festival", "--pipe"], stdin=subprocess.PIPE, preexec_fn=os.setsid)
        except OSError:
            tkMessageBox.showerror("Festival Error", "You either don't have festival installed or it is not in your path.")
            exit()
        
        self.p.stdin.write("(audio_mode 'async)\n")
        self.p.stdin.write("(voice_rab_diphone)\n")
    #The main function of the class, the one that causes text to be sent to festival along the pipe
    def speech(self, text):
        #Make sure the input isn't empty
        if (text == ""):
            text = "You didn't enter anything"
        #Print to the command line what is being spoken
        print "Speaking: " + str(text)
        #Create the text to send through the pipe to festival
        text = "(SayText \"" + str(text) + "\")\n"
        #send data along the pipe
        self.p.stdin.write(text)
    
    #The function that kills the current fetival process and its children processes.
    #It also recreates the pipe on a new festival session
    def resetSpeech(self):
        #Indicate on the command line that the 'stop' button has been pressed
        print "Killing"
        #Send SIGKILL to the process group of the current instance of festival
	os.killpg(os.getpgid(self.p.pid), signal.SIGKILL)
        #Reopen festival
        self.__init__()
