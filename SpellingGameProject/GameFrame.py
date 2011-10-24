from Tkinter import Frame, Button, Canvas, Entry, PhotoImage
from Tkconstants import *
from ProgressBar import ProgressBar
class GameFrame(Frame):
    """A class which controls the Game screen of the spelling aid."""
    
    def __init__(self, parent):
        Frame.__init__(self, parent, width=600, height=250)
        self.parent = parent    
       
    def init_gui(self):
        #Tick and cross images hard-coded
        correct = """R0lGODlhQABAAOeqAAAAAAABAAACAAADAAAEAAAFAAAFAQAGAQAHAQEHAQEIAQEJAQEKAQEKAgEL
AgEMAgENAgEPAgIPAgIQAgIRAwITAwIUAwIVBAMVBAIWAwIWBAIXBAMXBAMYAwIZBAMZBAMaBQMb
BAMdBQMeBQMfBQMgBQQgBQQiBgQkBgQlBgQmBwQnBwUnBgUoBwUqBwUrBwUsBwUsCAUtCAUuCAUv
CAYvCAUxCAYyCQYzCAY0CQY1CgY2CQY3CQc3CgY5Cgc5Cgc7Cgc+Cwg/CwdACwhACwhBCwhCCwhG
DAhHDAhIDQlLDQlMDglNDglPDglQDglRDglSDgpUDwpWDwtWDwpXDwpZDwtaEAtfEQtgEQthEQxk
EQxkEgxlEgxnEgxoEw1oEgxpEgxqEw1qEg1rEwxsEw1sEg1tEw1vEw1wFA1yFA5yFA1zFA50FA50
FQ51FA52FQ95Fg56FQ57Fg97FQ99Fg9+Fg9/Fg+AFhCAFg+BFhCCFhCEFxCGFxCHGBCIGBCKGBGK
GBCLGBGMGRGNGRGOGRGQGRGRGRGRGhGSGRGTGhKTGRKTGhGUGhKVGhKXGhKXGxKYGhKaGxKbGxKc
GxKdGxKdHBOdGxOdHBKeHBOeGxOeHBOfHBOgHBOhHBOiHBOiHROjHBOjHROkHRSkHROlHRSlHRSm
HRSnHRSoHRSrHv//////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////yH+EUNyZWF0ZWQgd2l0aCBH
SU1QACH5BAEKAP8ALAAAAABAAEAAAAj+AP8JHEiwoMGDCBMqPAhgocOHEB0CaBixosWFEyde3MhR
YEaKHUNC/CiyJMYHCTSaXGkQgAcVKVnKHAhgBZIIIGeanAiki4acOkVOlJInBNCgHQEIELOIxFGk
GwFASLNJxVOoFgFUiFOKx1WsEQFY0GOqiQCwIQF0ECSqi4KvaDGKWNRJjgW4cRMCOEGI06AWePMy
ROGnU6QggQUXBIBij6dPUBIrptk4lKkuAiRPBpCCT6hQdipoVgxgBB9PnAzBGC0YQAY7mzRJWsI6
L4AIazTpVkNg8kgFXDhpwqTorm+JA6aE0kRpk47acQEkMUVJU6cs0NEC8FGKEiVOfQb+ZMcKgMWk
TM0joRgPFQCIQMw1bXpy9rjC22+Ea+IUZwJ7pAZcIVx1jdjwX1AAKFHJJt5lgsWBOgGwAyScUHKJ
JoJIAKFMpRlSIXOj3LAhSwAkgMeHlIDixYgkauGdJpds4ggFLO5EhCOaWMKcKUMEEGFaJfzBoG6d
vAEBgipl9cAZoFRXXSQ41OgRAAHUJgATp1Sn2yZjJNBeARi8FZYMoGByoW6IrEbeD04Y9RAAFBwy
JHOYdCFlS1T8UQROCwVgxocwapIIB3cuBsAWppgxQ5KLGfGibpSI4kShLTnQRiqEWPHBUQCYAJ9u
zHHCxwGUtiQCH6RwYscRBOS0QBjKsYGqCSk1lMpQDoxs0okjaVjVEABCVBIfc6CwccBxADwxCaiF
VEHqBosAqhsnMdiaUABoDCsJIDq40YmZkIJCBgP2/VMiIAxWd4kkTsr6SA7W3ndBJMPJai8naSBQ
Lk0zxKalvZo00kO8DgXAxID2UmLJHARLtAAYsdorCQ0NS/TBHcMytwkdFb8JgyHDYuKJCx2/OcQm
mFhCSScM73tfFNRhMsoLJY+UwBeneAKHly7fZ0EdqOxQc0UAvFBGBT0/JEAD9SWN0XEBAQA7
"""
        wrong = """R0lGODlhQABAAOexAAAAAAEAAAIAAAMAAAQAAAUAAAYAAAgAAAkAAAoAAAwAAA0AAA4AAA8AABAA
ABEAABIAABMAABQAABUAABYAABcAABgAABkAABoAABsAABwAAB0AAB4AAB8AACAAACEAACIAACMA
ACQAACUAACYAACgAACkAACoAACsAACwAAC0AAC4AADEAADMAADQAADUAADYAADgAADkAADoAADsA
ADwAAD0AAD4AAD8AAEEAAEIAAEQAAEUAAEkAAEoAAEsAAFQAAFUAAFgAAFkAAF0AAF8AAGEAAGIA
AGQAAGcAAGgAAGoAAGsAAG0AAG4AAG8AAHAAAHMAAHgAAHsAAHwAAIEAAIYAAIoAAI4AAJMAAJQA
AJUAAJYAAJcAAJgAAJkAAJoAAJsAAJwAAJ0AAJ4AAKAAAKEAAKQAAKcAAKgAAKkAAKoAAK0AAK4A
AK8AALAAALEAALMAALUAALcAALgAALkAALoAALsAAL4AAL8AAMAAAMEAAMQAAMUAAMYAAMgAAMkA
AMoAAMwAAM0AAM4AAM8AANAAANEAANIAANMAANQAANUAANYAANcAANgAANkAANoAANsAAN0AAN4A
AOAAAOEAAOIAAOMAAOQAAOYAAOgAAOkAAOoAAOwAAO0AAO4AAO8AAPAAAPEAAPIAAPMAAPQAAPUA
APYAAPcAAPgAAPkAAPoAAPsAAPwAAP0AAP4AAP8AAP//////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////yH+EUNyZWF0ZWQgd2l0aCBH
SU1QACH5BAEKAP8ALAAAAABAAEAAAAj+AP8JHEhwIAAABRMqXLjwIMOHCQFAgIAQosWGFjRUvNhQ
A5sxDTZyvAggwhpAK0SOFAigwxxXo7aEXGmxZBlSqwbFUMmx5Z1To0qN4oKAJ02DCsiQEmqKUA2j
DwFsoFOKFKlRpE55CQB1JQABZE5dtVqqEIyuES28STXW6ihWXxweNQhAzCqsVq+eMpQCrUEKamCN
wpt3VKsvBPwyBEDASyvChVcdKuEXQIU0giEXVtVFgWKFCbKo0lyY1SEVXQFcaJM5r+u8pbY4+ExQ
AZbXuK+uQjTDKAAMckaTdh00pueRCK6IEpqb+ClEOVSqliN0+OugpbgkrinASinmzYn+l0KEYyMA
Cm3EWseNVZUXuQ0BVFnVNvxrU4peIATQ4AzM9c0ZtlVqVAhmX4CpKBLCQR8UYkp9BxLHShdFKUTA
FDBFyB4ppugBwn4m8CGWhuydIpNKBkxhCoD2mXLHhwad8MeKJLKnBQMbFSAFKODVeJUpe4ggHQiH
0OjjVUJtcQBCAkTBI4u5jXLKIBz4VsEjQB05FipdHLTEKdUdKWUjE6QmQSMPQskeK1sQ4QqEGmJl
SiMSVKbBIOppOYoqj6lJXFaFbPAZACT0kaeYcEaI1SmBnEDbPwCgYKiWlOZ1iiAsPMoSCYMYWSmJ
QTGS0lwAaNBIlp8qWoolJGhaEAD+EjziaapRlpIJjHMZVEGRiaYqJyWU5foqCH8cSuuWjrTgalQn
iHisa6csYsOyEAFgAiCzVhqUJOUJG5UHiWSL6Ca9eVstBYw8mKonZ5lbUxOspJoKGvC5q1AASbDi
Z4CrgFGhvQkN0ESatI6CChgPUAvRAFB40uOxYkSg8EIBONGJuNpWZcYCE7+qxFKDPesWh2psZy4A
R7TS67F7viFAxwAg8UrIIrO3ShwJKCwAE6nQXDN7qLxBwbIDPBHKyj9bZUobGq0kwBOdPJz0dUvB
cQFtADARSpg+yrlvYRzaMVtNSLDlM6ikdJLu1yOfwse/DR0xM9tYlcLJCxIgQrD+mKgAMtO9SvSJ
6CmUTAsAB37s3TUqfmTA0wBOjKwlKpDsUBGheIyo5yl6tEoQw1Gz/eMkPIgEwAh5oKrlKXl4/s8B
DWN8IFaadPtqBn2gIrqcf6BwUAaCCIdoKDs1xMAfPW+uiQv7vaCIumiX8ol+USHg7NelYPKDeTgg
InWAWWFSbrUN1KG4fVhVIoR0OSCiOvioRKID1mpVxWJQlhDhmwyI3HXgKZEonVcywAboBegUmghC
alRwCH0FKHvzOwoAJuAG3R3QEz2oTAkM4T+qfWJ8EkwAHDronE9EsCYpKMT7sBIK6gkLAAFow2jE
wwkfPAoAMCBEVcZiCk0U72RWBEiD4jAxBFcBgAaEoBEqJmE7dwFgATcRSikuYQRqASAGg1DFKSAh
QIBBCgJh4NAmijAxAKxAEJiwnBcN4gAwdAIIHYNUB24Qx8U8QFn2guEaI/KZgAAAOw=="""
        #Create actual image objects
        self.correct_img = PhotoImage(data=correct)
        self.wrong_img = PhotoImage(data=wrong)
        #Create the UI elements
        self.entry = Entry(self.parent, width=15, 
                           font=('Helvetica', 20, 'normal'), justify=CENTER)
        self.entry.bind("<Return>", lambda x:self.buttonSubmit.invoke())
        self.buttonNext = Button(self.parent, width=10, text="Next Word",
                            command=self.next_word, state=DISABLED)
        self.buttonSubmit = Button(self.parent, width=10, text="Submit",
                              command=self.submit_word)
        buttonReplay = Button(self.parent, width=10, text="Repeat Word",
                              command=self.replay_word)
        self.game_canvas = Canvas(self, width=600, height=250, bg="#FFFFFF")
        self.word_display = self.game_canvas.create_text((300, 105), text="?",
                           font=("Helvetica", 50, "bold"), fill="#004183")
        self.progress_display = self.game_canvas.create_text((593, 5),
                                text="%d/%d"%(1, self.parent.list_length),
                                font=("Helvetica", 25, "bold"), anchor=NE)
        self.timer_display = self.game_canvas.create_text(10, 5, anchor=NW,
                                                        font=("Helvetica", 25))
        self.progress_bar = ProgressBar(self, width=300,
                                       increments=len(self.parent.current_list.words))
        self.game_canvas.create_window(500, 10, anchor=NE, window=self.progress_bar)
        self.game_canvas.create_window(300, 180, window=self.entry)
        self.game_canvas_image = self.game_canvas.create_image(500, 170)
        self.game_canvas.create_window(150, 230, window=buttonReplay)
        self.game_canvas.create_window(300, 230, window=self.buttonSubmit)
        self.game_canvas.create_window(450, 230, window=self.buttonNext)
        self.game_canvas.pack()
        
    def start(self):
        """Method to be invoked when the game is starting. Begins timer and sets up game"""
        self.current_list_iter = iter(self.parent.current_list.words)
        self.current_word = self.current_list_iter.next()
        self.parent.festival.speech(self.current_word)
        self.time_elapsed = 0
        self.init_gui()
        self.tick()

    def next_word(self):
        """Speak the next word in the list, update UI elements"""
        try:
            self.current_word = self.current_list_iter.next()
            index = self.parent.current_list.words.index(self.current_word) + 1
            self.game_canvas.itemconfig(self.progress_display, text="%d/%d"
                                   %(index, self.parent.list_length))
            if index == self.parent.list_length:
                self.buttonNext.configure(text="Finish")
            self.game_canvas.itemconfig(self.word_display, text="?", fill="#004183")
            self.game_canvas.itemconfig(self.game_canvas_image, state=HIDDEN)
            self.buttonSubmit.configure(state=NORMAL)
            self.buttonNext.configure(state=DISABLED)
            self.parent.festival.speech(self.current_word)
        except StopIteration:
            #If there are no more words in the list, the game is over.
            self.list_complete()

    def list_complete(self):
        """The game is finished; stop the timer and show the results page"""
        self.parent.after_cancel(self.timer)
        self.parent.show_results(self.time_elapsed)
        

    def replay_word(self):
       """Have the current word spoken again"""
       self.parent.festival.speech(self.current_word)

    def submit_word(self, event=None):
        """Process user input on the current word"""
        guess = self.entry.get()
        self.entry.delete(0, END)
        if guess == self.current_word.word:
            #The guess was right
            self.correct(guess)
        else:
            #The guess was wrong
            self.incorrect(guess)
        self.game_canvas.itemconfig(self.word_display, text='%s'%(self.current_word))
        self.buttonNext.configure(state=NORMAL)
        self.buttonSubmit.configure(state=DISABLED)
        self.game_canvas.itemconfig(self.game_canvas_image, state=NORMAL)
        

    def correct(self, guess):
        """The user made a correct guess, update UI elements to reflect this"""
        self.current_word.setAnswer(guess, True)
        self.game_canvas.itemconfig(self.game_canvas_image, image=self.correct_img)
        self.game_canvas.itemconfig(self.word_display, fill="#139E1C")
        self.progress_bar.increment(True)

    def incorrect(self, guess):
        """The user made an incorrect guess, update UI elements to reflect this"""
        self.current_word.setAnswer(guess, False)
        self.game_canvas.itemconfig(self.game_canvas_image, image=self.wrong_img)
        self.game_canvas.itemconfig(self.word_display, fill="#F30000")
        self.progress_bar.increment(False)

    def tick(self):
        """A second has passed, update the timer and reschedule this call for next second"""
        seconds = (self.time_elapsed)%60
        minutes = self.time_elapsed/60
        separator = ":" if seconds > 9 else ":0"
        formatted_time = "%d%s%d"%(minutes, separator, seconds)
        self.game_canvas.itemconfig(self.timer_display, text=formatted_time)
        self.time_elapsed +=1
        self.timer = self.parent.after(1000, self.tick)

