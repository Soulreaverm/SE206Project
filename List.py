class WordList():

    def __init__(self, (list_id, name, source, date_edited, num_words)):
        self.l_id = list_id
        self.name = name
        self.source = source
        self.date_edited = date_edited
        self.num_words = num_words

    def __str__(self):
        return self.name
