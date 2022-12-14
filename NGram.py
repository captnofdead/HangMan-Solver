import json
import requests
import random
import string
import secrets
import time
import re
import collections

def build_dictionary(dictionary_file_location):
    text_file = open(dictionary_file_location, "r")
    dictionary = text_file.read().splitlines()
    text_file.close()
    return dictionary


class Hangman(object):
    def __init__(self):
        self.guessed_letters = [] # a list that stores guessed letters (well well)
        self.incorrect_guesses = [] # a list that stores incorrect guessed letter
        self.train_dictionary = build_dictionary("words_250000_train.txt")
        self.letters = sorted(set("".join(self.train_dictionary)))
        self.n = len(self.letters)
        self.weights = [0]*self.n
        self.oneMap = collections.defaultdict(lambda: collections.defaultdict(int))
        self.twoMap = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        self.threeMap = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        self.fourMap = collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))
        self.fiveMap = collections.defaultdict(lambda: collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))))
        self.sixMap = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))))
        self.tries_remaining = 6
        self.current_dictionary = self.train_dictionary
        self.not_guessed_letter = []

    def createFreqTable(self, dictionary):
        self.oneMap = collections.defaultdict(lambda: collections.defaultdict(int))
        self.twoMap = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        self.threeMap = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        self.fourMap = collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))
        self.fiveMap = collections.defaultdict(lambda: collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))))
        self.sixMap = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(
            lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int))))))
        for x in dictionary:
            for i in range(len(x)):
                self.oneMap[len(x)][x[i]] += 1
            for i in range(len(x)-1):
                self.twoMap[len(x)][x[i]][x[i+1]] += 1
            for i in range(len(x)-2):
                self.threeMap[x[i]][x[i+1]][x[i+2]] += 1
            for i in range(len(x)-3):
                self.fourMap[x[i]][x[i+1]][x[i+2]][x[i+3]] += 1
            for i in range(len(x)-4):
                self.fiveMap[x[i]][x[i+1]][x[i+2]][x[i+3]][x[i+4]] += 1

    def updateWeights(self, frequencyList, val):
        LocalWeights = [0] * self.n
        total = sum(frequencyList)
        if total > 0:
            for i in range(self.n):
                LocalWeights[i] = frequencyList[i] / total
                frequencyList[i] = 0
        self.weights = [self.weights[i] + LocalWeights[i] * val for i in range(self.n)]
        return frequencyList

    def guessHelper(self, x):
        m = len(self.not_guessed_letter)
        frequencyList = [0]*self.n

        for i in range(len(x)):
            frequencyList = [frequencyList[j] + self.oneMap[len(x)][self.letters[j]] if x[i] == '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j] for j in range(self.n)]
        frequencyList = self.updateWeights(frequencyList, 0.05)
        for i in range(len(x) - 1):
            frequencyList = [frequencyList[j]+self.twoMap[len(x)][x[i]][self.letters[j]] if x[i] != '_' and x[i+1] == '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.twoMap[len(x)][self.letters[j]][x[i+1]] if x[i] == '_' and self.letters[j] in self.not_guessed_letter and x[i+1] != '_' else frequencyList[j] for j in range(self.n)]
        frequencyList = self.updateWeights(frequencyList, 0.10)
        for i in range(len(x) - 2):
            frequencyList = [frequencyList[j]+self.threeMap[x[i]][x[i+1]][self.letters[j]] if x[i] != '_' and x[i+1] != '_' and x[i+2] == '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.threeMap[x[i]][self.letters[j]][x[i+2]] if x[i] != '_' and x[i+1] == '_' and x[i+2] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.threeMap[self.letters[j]][x[i+1]][x[i+2]] if x[i] == '_' and x[i+1] != '_' and x[i+2] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j] for j in range(self.n)]
        frequencyList = self.updateWeights(frequencyList, 0.20)
        for i in range(len(x) - 3):
            frequencyList = [frequencyList[j]+self.fourMap[x[i]][x[i+1]][x[i+2]][self.letters[j]] if x[i] != '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] == '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fourMap[x[i]][x[i+1]][self.letters[j]][x[i+3]] if x[i] != '_' and x[i+1] != '_' and x[i+2] == '_' and x[i+3] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fourMap[x[i]][self.letters[j]][x[i+2]][x[i+3]] if x[i] != '_' and x[i+1] == '_' and x[i+2] != '_' and x[i+3] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fourMap[self.letters[j]][x[i+1]][x[i+2]][x[i+3]] if x[i] == '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j] for j in range(self.n)]
        frequencyList = self.updateWeights(frequencyList, 0.25)
        for i in range(len(x) - 4):
            frequencyList = [frequencyList[j]+self.fiveMap[x[i]][x[i+1]][x[i+2]][x[i+3]][self.letters[j]] if x[i] != '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] == '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fiveMap[x[i]][x[i+1]][x[i+2]][self.letters[j]][x[i+4]] if x[i] != '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] == '_' and x[i+4] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fiveMap[x[i]][x[i+1]][self.letters[j]][x[i+3]][x[i+4]] if x[i] != '_' and x[i+1] != '_' and x[i+2] == '_' and x[i+3] != '_' and x[i+4] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fiveMap[x[i]][self.letters[j]][x[i+2]][x[i+3]][x[i+4]] if x[i] != '_' and x[i+1] == '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.fiveMap[self.letters[j]][x[i+1]][x[i+2]][x[i+3]][x[i+4]] if x[i] == '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j] for j in range(self.n)]
        frequencyList = self.updateWeights(frequencyList, 0.35)
        for i in range(len(x) - 5):
            frequencyList = [frequencyList[j]+self.sixMap[self.letters[j]][x[i+1]][x[i+2]][x[i+3]][x[i+4]][x[i+5]]if x[i] == '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] != '_' and x[i+5] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.sixMap[x[i]][self.letters[j]][x[i+2]][x[i+3]][x[i+4]][x[i+5]] if x[i] != '_' and x[i+1] == '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] != '_' and x[i+5] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.sixMap[x[i]][x[i+1]][self.letters[j]][x[i+3]][x[i+4]][x[i+5]] if x[i] != '_' and x[i+1] != '_' and x[i+2] == '_' and x[i+3] != '_' and x[i+4] != '_' and x[i+5] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.sixMap[x[i]][x[i+1]][x[i+2]][self.letters[j]][x[i+4]][x[i+5]]if x[i] != '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] == '_' and x[i+4] != '_' and x[i+5] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.sixMap[x[i]][x[i+1]][x[i+2]][x[i+3]][self.letters[j]][x[i+5]] if x[i] != '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] == '_' and x[i+5] != '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j]+self.sixMap[x[i]][x[i+1]][x[i+2]][x[i+3]][x[i+4]][self.letters[j]] if x[i] != '_' and x[i+1] != '_' and x[i+2] != '_' and x[i+3] != '_' and x[i+4] != '_' and x[i+5] == '_' and self.letters[j] in self.not_guessed_letter else frequencyList[j] for j in range(self.n)]
        frequencyList = self.updateWeights(frequencyList, 0.45)

        totalWeights = sum(self.weights)
        if totalWeights>0:
            self.weights = [p/totalWeights for p in self.weights]

        max_prob = 0
        guess_letter = ''
        for i, letter in enumerate(self.letters):
            if self.weights[i] > max_prob:
                max_prob = self.weights[i]
                guess_letter = letter

        if guess_letter == '':
            letters = self.letters.copy()
            letters_shuffled = ['e', 'a', 'i', 'o', 'u'] + letters
            random.shuffle(letters_shuffled)
            # letters_shuffled = ['e', 'a', 'i', 'o', 'u'] + letters
            for letter in letters_shuffled:
                if letter not in self.guessed_letters:
                    return letter

        return guess_letter

    def guess(self, word):  # word input example: "_ p p _ e "

        self.incorrect_guesses = list(set(self.guessed_letters) - set(word))

        if len(self.guessed_letters) > 0 and self.guessed_letters[-1] in self.incorrect_guesses and self.tries_remaining <= 3:
            self.current_dictionary = [word for word in self.current_dictionary if not set(word).intersection(set(self.incorrect_guesses))]
            self.createFreqTable(self.current_dictionary)

        self.weights = [0] * self.n

        clean_word = word[::2]

        return self.guessHelper(clean_word)
