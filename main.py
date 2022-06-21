from random import randint, choice, choices
from time import sleep

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
        print('Using ' + str(self.language[self.lang]) + '. Learning with ' + str(self.options) + '. Type "skip" to skip a question. Type "stop" to exit learn. Type "switch" to switch languages.')

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
                    print(f'Skipped. Answer was "{self.totest[self.lang]}"\n')
                    continue
                if self.response == 'switch':
                    self.lang = (self.lang + 1) % 2
                    print('\n')
                    continue
                if self.answers[self.response.upper()] == self.totest:
                    print('Correct.\n')
                    continue
                else:
                    print(f'Incorrect. Correct answer was "{self.totest[self.lang]}"')
                    
            if self.method == 'openr':
                self.totest = choice(self.vocab)
                print(f'Open response question. Type the definition of "{self.totest[self.lang]}"')
                
                self.response = input()
                if self.response == 'stop':
                    return
                if self.response == 'skip':
                    print(f'Skipped. Answer was "{self.totest[(self.lang + 1) % 2]}"\n')
                    continue
                if self.response == 'switch':
                    self.lang = (self.lang + 1) % 2
                    print('\n')
                    continue
                if self.response == self.totest[(self.lang + 1) % 2]:
                    print('Correct.\n')
                    continue
                else:
                    print(f'Incorrect. Correct answer was "{self.totest[(self.lang + 1) % 2]}"\n')
                    
            if self.method == 'tf':
                self.answer = randint(0, 1)
                if self.answer:
                    self.totest = choice(self.vocab)
                    print(f'True or False question. Is "{self.totest[1]}" the definition of "{self.totest[0]}"? Answer 0 (False) or 1 (True).')
                    
                    self.response = input()
                    if self.response == 'stop':
                        return
                    if self.response == 'skip':
                        print(f'Skipped. Answer was "{self.answer}"\n')
                        continue
                    if self.response == 'switch':
                        self.lang = (self.lang + 1) % 2
                        print('Switching doesn\'t do anything to t/f questions but ok.\n')
                        continue
                    if self.response == str(self.answer):
                        print('Correct.')
                        continue
                    if self.response != str(self.answer):
                        print(f'Incorrect. Answer was "{self.answer}"')
                        continue
                else:
                    self.totest = choice(self.vocab)
                    self.bait = choice(self.vocab)
                    while self.bait == self.totest:
                        self.bait = choice(self.vocab)
                    print(f'True or False question. Is "{self.totest[1]}" the definition of "{self.bait[0]}"? Answer 0 (False) or 1 (True).')
                    
                    self.response = input()
                    if self.response == 'stop':
                        return
                    if self.response == 'skip':
                        print(f'Skipped. Answer was "{self.answer}"\n')
                        continue
                    if self.response == 'switch':
                        self.lang = (self.lang + 1) % 2
                        print('Switching doesn\'t do anything to t/f questions but ok.\n')
                        continue
                    if self.response == str(self.answer):
                        print('Correct.')
                        continue
                    if self.response != str(self.answer):
                        print(f'Incorrect. Answer was "{self.answer}"')
                        continue
            
            if self.method == 'flashcards':
                self.word = choice(self.vocab)
                
                print('Flashcard question. Press "enter" to flip card.')
                if self.lang == 0:
                    print(f'Word: "{self.word[self.lang]}"')
                else:
                    print(f'Definition: "{self.word[self.lang]}"')
                self.response = input()
                if self.response == 'stop':
                    return
                if self.response == 'skip':
                    print('Skipped. Why would you skip a flashcard?\n')
                    continue
                if self.response == 'switch':
                    self.lang = (self.lang + 1) % 2
                    print('\n')
                    continue
                else:
                    if self.lang == 0:
                        print(f'Definition: "{self.word[(self.lang + 1) % 2]}"\n')
                    else:
                        print(f'Word: "{self.word[(self.lang + 1) % 2]}"\n')

    def start_test(self, mc, openr, tf, num = None, lang = None):
        self.input = {'mc':mc, 'openr':openr, 'tf':tf}
        self.options = [name for name, value in self.input.items() if value]
        self.response = ''
        self.wrong = 0
        self.correct = 0
        
        if not lang:
            self.lang = None
        else:
            self.lang = lang
        print('Starting test.')
        while self.lang not in [0, 1]:
            try:
                self.lang = int(input('Enter which language you would like to start with ' + str(self.language) + ' (0 or 1)'))
            except ValueError:
                continue
        if not num:
            self.num = ''
        else:
            self.num = num
        while not str(self.num).isdigit() or not self.num:
            try:
                self.num = int(input(f'Enter the number of questions you would like to test between.'))
            except ValueError:
                continue
        print('Using ' + str(self.language[self.lang]) + '. Testing with ' + str(self.options) + ' for ' + str(self.num) + ' question(s). Type "skip" to skip a question. Type "stop" to exit the test.')
        for i in range(self.num):
            sleep(1)
            self.method = choice(self.options)
            self.question_number = i + 1
            
            if self.method == 'mc':
                self.available = choices(self.vocab, k = 4)
                self.totest = choice(self.available)
                self.answers = {letter:word for letter, word in zip(['A', 'B', 'C', 'D'], self.available)}
                print('Multiple choice question: ' + str(self.totest[self.lang]))
                print('\n'.join(str(letter) + '. ' + str(word[(self.lang + 1) % 2]) for letter, word in self.answers.items()))

                self.response = input()
                if self.response == 'stop':
                    self.wrong += 1
                    print(f'{self.wrong} wrong. {self.correct} correct.')
                    return
                if self.response.upper() not in self.answers.keys() and self.response not in ['skip', 'stop', 'switch']:
                    print('???')
                    self.wrong += 1
                    continue
                if self.response == 'skip':
                    print('Skipped.\n')
                    self.wrong += 1
                    continue
                if self.answers[self.response.upper()] == self.totest:
                    self.correct += 1
                    continue
                else:
                    self.wrong += 1
            
            if self.method == 'openr':
                self.totest = choice(self.vocab)
                print(f'Open response question. Type the definition of "{self.totest[self.lang]}"')
                
                self.response = input()
                if self.response == 'stop':
                    self.wrong += 1
                    print(f'{self.wrong} wrong. {self.correct} correct.')
                    return
                if self.response == 'skip':
                    print(f'Skipped.\n')
                    self.wrong += 1
                    continue
                if self.response == self.totest[(self.lang + 1) % 2]:
                    self.correct += 1
                    continue
                else:
                    self.wrong += 1
                    
            if self.method == 'tf':
                self.answer = randint(0, 1)
                if self.answer:
                    self.totest = choice(self.vocab)
                    print(f'True or False question. Is "{self.totest[1]}" the definition of "{self.totest[0]}"? Answer 0 (False) or 1 (True).')
                    
                    self.response = input()
                    if self.response == 'stop':
                        self.wrong += 1
                        print(f'{self.wrong} wrong. {self.correct} correct.')
                        return
                    if self.response == 'skip':
                        print(f'Skipped.\n')
                        self.wrong += 1
                        continue
                    if self.response == str(self.answer):
                        self.correct += 1
                        continue
                    if self.response != str(self.answer):
                        self.wrong += 1
                        continue
                else:
                    self.totest = choice(self.vocab)
                    self.bait = choice(self.vocab)
                    while self.bait == self.totest:
                        self.bait = choice(self.vocab)
                    print(f'True or False question. Is "{self.totest[1]}" the definition of "{self.bait[0]}"? Answer 0 (False) or 1 (True).')
                    
                    self.response = input()
                    if self.response == 'stop':
                        self.wrong += 1
                        print(f'{self.wrong} wrong. {self.correct} correct.')
                        return
                    if self.response == 'skip':
                        print(f'Skipped.\n')
                        self.wrong += 1
                        continue
                    if self.response == str(self.answer):
                        self.correct += 1
                        continue
                    if self.response != str(self.answer):
                        self.wrong += 1
                        continue
                    
        print(f'{self.correct}/{self.num} questions correct.')

path = input('What is your files name (Without ".txt")?  ')
vocab = Vocabulary(path)

activity = None
types = [None]
while activity not in ['flashcards', 'learn', 'test']:
    activity = input('Would you like to view "flashcards", "learn", or take a "test"?  ')
    
if activity == 'flashcards':
    vocab.start_flashcards()

if activity == 'learn':
    while not set(types).issubset(set(['mc', 'openr', 'tf', 'flashcards'])):
        print(types)
        types = input('Which of the following would you like to learn with? Separate with a comma (no space):\nMultiple choice (mc)\nOpen response (openr)\nTrue/False (tf)\nFlashcards (flashcards)\n').split(',')
    vocab.start_learn(mc = 'mc' in types, openr = 'openr' in types, tf = 'tf' in types, flashcards = 'flashcards' in types)

if activity == 'test':
    while not set(types).issubset(set(['mc', 'openr', 'tf'])):
        types = input('Which of the following would you like to test with? Separate with a comma (no space):\nMultiple choice (mc)\nOpen response (openr)\nTrue/False (tf)\n').split(',')
    vocab.start_test(mc = 'mc' in types, openr = 'openr' in types, tf = 'tf' in types)