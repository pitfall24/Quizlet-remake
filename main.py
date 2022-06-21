from random import randint, choice, choices
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
        for i, word in enumerate(self.words):
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
        while self.lang not in [0, 1]:
            try:
                self.lang = int(input('Enter which language you would like to start with ' + str(self.language) + ' (0 or 1)'))
            except ValueError:
                continue
        print('Using', self.language[self.lang] + '. Press "enter" to flip flashcard and go to the next term. Type "stop" to exit flashcards. Type "switch" to switch languages.')
        self.response = ''
        self.loc = 0
        while True:
            sleep(1)
            print(self.vocab[self.loc][self.lang])
            self.response = input()
            if self.response == '':
                print(self.vocab[self.loc][(self.lang + 1) % 2], end = '\n-------------------------------------------------\n')
            if self.response == 'stop':
                return
            if self.response == 'switch':
                self.lang = (self.lang + 1) % 2
            self.loc = (self.loc + 1) % len(self.vocab)

    def start_learn(self, mc, openr, tf, flashcards, lang = None):
        self.input = {'mc':mc, 'openr':openr, 'tf':tf, 'flashcards':flashcards}
        self.options = [name for name, value in self.input.items() if value]
        self.response = ''

        if not lang:
            self.lang = None
        else:
            self.lang = lang
        print('Starting learn.')
        while self.lang not in [0, 1]:
            try:
                self.lang = int(input('Enter which language you would like to start with ' + str(self.language) + ' (0 or 1)'))
            except ValueError:
                continue
        print('Using ' + str(self.language[self.lang]) + '. Quizzing with ' + str(self.options) + '. Type "skip" to skip a question. Type "stop" to exit learn. Type "switch" to switch languages.')

        while True:
            sleep(1)
            self.method = choice(self.options)
            if self.method == 'mc':
                self.available = choices(self.vocab, k = 4)
                self.totest = choice(self.available)
                self.answers = {letter:word for letter, word in zip(['A', 'B', 'C', 'D'], self.available)}
                print('Multiple choice question: ' + str(self.totest[self.lang]))
                print('\n'.join(str(letter) + '. ' + str(word[(self.lang + 1) % 2]) for letter, word in self.answers.items()))

                self.response = input()
                if self.response == 'stop':
                    return
                if self.response.upper() not in self.answers.keys() and self.response not in ['skip', 'stop', 'switch']:
                    print('???')
                    continue
                if self.response == 'skip':
                    print(f'Skipped. Answer was "{self.totest[self.lang]}"')
                    continue
                if self.response == 'switch':
                    self.lang = (self.lang + 1) % 2
                    continue
                if self.answers[self.response.upper()] == self.totest:
                    print('Correct')
                    continue
                else:
                    print(f'Incorrect. Correct answer was "{self.totest[self.lang]}"')

    def start_test(self):
        pass

vocab = Vocabulary(path)
vocab.start_learn(True, False, False, False)
