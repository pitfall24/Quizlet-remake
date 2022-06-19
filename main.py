path = 'Quizlet remake test file'

class Vocabulary:
    def __init__(self, path):
        self.path = path
        self.words = []
        self.lines = []
        self.language = [None, None]
        self.vocab = {}

        self.read_file()
        self.get_words()
        self.get_vocab()

    def read_file(self):
        with open(self.path + '.txt', 'r') as file:
            self.lines = file.readlines()

    def get_words(self):
        self.startend = [0, 0]
        self.langstartend = [-1, -1]
        for i in range(len(self.lines)):
            if 'Vocabulary{' in self.lines[i]:
                self.startend[0] = i
            if '}Vocabulary' in self.lines[i]:
                self.startend[1] = i
            if 'Language{' in self.lines[i]:
                self.langstartend[0] = i
            if '}Language' in self.lines[i]:
                self.langstartend[1] = i

        for i in range(self.startend[0] + 1, self.startend[1]):
            self.words.append(self.lines[i].strip().replace(';', ''))
        self.language = self.lines[self.langstartend[0] + 1:self.langstartend[1]][0].strip().split(':')

    def get_vocab(self):
        for i, word in enumerate(self.words, 1):
            self.vocab[i] = word.split(':')


    def print_words(self):
        for i in self.words:
            print(i)

    def print_vocab(self):
        for i, (word, definition) in self.vocab.items():
            print(i, '\t- ', word, '->', definition)

    def print_language(self):
        print('Word:', self.language[0], end = '\t')
        print('Definition:', self.language[1])

vocab = Vocabulary(path)

vocab.print_vocab()
vocab.print_language()