class Word():

    def __init__(self, (word_id, word, definition, example, difficulty)):

        self.w_id = word_id
        self.word = word
        self.definition = definition
        self.example = example
        self.difficulty = difficulty

    def setAnswer(self, answer, isCorrect):
        self.answer = answer
        self.isCorrect = isCorrect

    def __str__(self):
        return self.word
