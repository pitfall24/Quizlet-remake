from random import randint
from time import sleep

path = 'file'

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
        
    def start_flashcards(self, lang = None):
        if not lang:
            self.lang = None
        else:
            self.lang = lang
        print('Starting flashcards.')
        while self.lang not in self.language:
            self.lang = input('Enter which language you would like to start with ' + str(self.language))
        print('Using', self.lang + '. Press "enter" to flip flashcard and go to the next term. Type "stop" to exit flashcards.')
        self.response = ''
        sleep(2)
        self.loc = 1
        while self.response != 'stop':
            print(self.vocab[self.loc][self.language.index(self.lang)])
            self.response = input()
            if self.response == '':
                print(self.vocab[self.loc][(self.language.index(self.lang) + 1) % 2], end = '\n\n')
            if self.response == 'stop':
                return
            self.loc = self.loc % len(self.vocab) + 1
    
    def start_learn(self):
        pass
    
    def start_test(self):
        pass

vocab = Vocabulary(path)
vocab.start_flashcards()
