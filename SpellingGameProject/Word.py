class Word():
    """Class which represents a word"""
    def __init__(self, (word_id, word, definition, example, difficulty)):

        self.w_id = word_id
        self.word = word
        self.definition = definition
        self.example = example
        self.difficulty = difficulty

    def setAnswer(self, answer, isCorrect):
        """Update the word with details about the users performance in spelling
           it"""
        self.answer = answer
        self.isCorrect = isCorrect

    def __str__(self):
        """Word as a string is the word itself"""
        return self.word
