# Lab 1: Neural Networks applied in NLP
# @Author: Diana Mocanu
# @Date: October 8th 2023
from nltk.corpus import wordnet
import random
import tkinter as tk



# WORDNET METHODS
def get_hyponyms(word):
    word = wordnet.synsets(word, 'n')[0]
    hypos = lambda s: s.hyponyms()
    synset = list(word.closure(hypos))
    result = []
    for syn in synset:
        names = syn.lemma_names()
        for name in names:
            result.append(name)
    return result


def get_hypernyms(word):
    result = []
    for ss in wordnet.synsets(word):
        for hyper in ss.hypernyms():
            names = hyper.lemma_names()
            for name in names:
                result.append(name)
    return result


def get_definition(word):
    syns = wordnet.synsets(word)
    return syns[0].definition()


def get_synonym(word):
    synonyms = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
    return synonyms


def get_antonyms(word):
    antonyms = []
    synsets = wordnet.synsets(word)
    for synset in synsets:
        for lemma in synset.lemmas():
            for antonym in lemma.antonyms():
                antonyms.append(antonym.name())

    return antonyms


# CROSSWORD GENERATION
def create_empty_crossword(n):
    return [[' ' for _ in range(n)] for _ in range(n)]


def try_place_word(crossword, word, direction, x, y):
    if direction == 'horizontal':
        if y + len(word) > len(crossword):
            return False
        for i in range(len(word)):
            if crossword[x][y + i] != ' ' and crossword[x][y + i] != word[i]:
                return False
            crossword[x][y + i] = word[i]
    else:
        if x + len(word) > len(crossword):
            return False
        for i in range(len(word)):
            if crossword[x + i][y] != ' ' and crossword[x + i][y] != word[i]:
                return False
            crossword[x + i][y] = word[i]
    return True


def generate_crossword(words):
    average_word_length = sum(len(word) for word in words) / len(words)
    n = int(2 * average_word_length)
    crossword = create_empty_crossword(n)
    placed_words = []
    random.shuffle(words)
    for word in words:
        if len(placed_words) == 7:
            break
        if len(word) < n:
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                x = random.randint(0, n - 1)
                y = random.randint(0, n - len(word))
            else:
                x = random.randint(0, n - len(word))
                y = random.randint(0, n - 1)
            try_place_word(crossword, word, direction, x, y)
            placed_words.append((word, direction, x, y))
    return crossword, placed_words, n


# USER INTERFACE


class Game(object):

    def __init__(self, root, size, crossword, clues):
        self.clues = clues
        self.root = root
        self.crossword = crossword
        self.size = size
        self.root.title('DL4NLP - Crossword Game')
        self.root.geometry('650x650')
        self.root.configure(bg='#8c1aff')

        self.frame = tk.Frame(root, bg='#8c1aff')
        self.frame.pack(expand=True, fill="both")

        self.grid_frame = tk.Frame(self.frame, bg="#8c1aff")
        self.grid_frame.grid(row=0, column=0, padx=(10, 0), sticky="nsew")

        # crossword grid
        self.entries = [[tk.Entry(self.grid_frame, width=2, font=('Arial', 14, 'bold')) for _ in range(self.size + 1)]
                        for _
                        in
                        range(self.size + 1)]

        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                self.entries[i][j].grid(row=i, column=j)

        #labels
        for i in range(self.size):
            row_label = tk.Label(self.grid_frame, text=str(i + 1), bg='#8c1aff', fg="white", font=('Helvetica', 12))
            row_label.grid(row=i + 1, column=0)

        for j in range(self.size):
            col_label = tk.Label(self.grid_frame, text=chr(ord('@') + j + 1), bg='#8c1aff', fg="white",
                                 font=('Helvetica', 12))
            col_label.grid(row=0, column=j + 1)

        # clues
        self.clue_listbox = tk.Listbox(self.frame, width=40, height=10, bg="#8c1aff", fg="white",
                                       font=('Helvetica', 12))
        self.clue_listbox.grid(row=0, column=1, padx=10, sticky="nsew")
        scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        scrollbar.config(command=self.clue_listbox.xview)
        scrollbar.grid(row=1, column=1, padx=10, sticky="ew")

        for clue in self.clues:
            self.clue_listbox.insert(tk.END, clue)

        # check
        self.check_button = tk.Button(self.frame, text="Check Answers", command=self.check_answers, bg="#4CAF50",
                                      fg="white", font=('Arial', 14, 'bold'))
        self.check_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def check_answers(self):
        for i in range(1,self.size+1):
            for j in range(1,self.size+1):
                user_input = self.entries[i][j].get()
                correct_answer = self.crossword[i-1][j-1]

                if user_input != correct_answer:
                    self.entries[i][j].config(bg="#FF6347")
                else:
                    self.entries[i][j].config(bg="green")


if __name__ == "__main__":

    # 1. Exploit WordNet’s hyponym/hypernym hierarchy to collect words that are related to
    # a user given theme (e.g. sport, books, food).

    category = input()
    #category = 'food'
    hyponyms = get_hyponyms(category)
    hypernyms = get_hypernyms(category)
    # print('Category: ', category)
    # print('Hyponyms: ', end = '')
    # for hypo in hyponyms: print(hypo, end = ',')
    # print()
    # print('Hyponyms: ', end='')
    # for hyper in hypernyms: print(hyper, end=',')

    # 2. Generate the crosswords puzzle
    crossword, placed_words, n = generate_crossword(hyponyms + hypernyms)
    for row in crossword:
        print(" ".join(row))


    # 3. For each mapped word, extract a linguistic feature using NLTK’s interface to Wordnet
    # (synonyms, antonyms, meronyms, definitions etc.)
    clues = []
    for placed in placed_words:
        word = placed[0]
        direction = placed[1]
        row = placed[2] + 1
        column = placed[3] + 1
        definition = get_definition(word)
        clues.append(direction + " row: " + str(row) + " column: " + str(chr(ord('@') + column + 1)) + " - " + definition)

    # 4. Provide it in a user-friendly manner
    root = tk.Tk()
    game = Game(root, n, crossword, clues)
    root.mainloop()
