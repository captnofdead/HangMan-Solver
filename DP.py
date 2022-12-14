import json
import requests
import random
import string
import secrets
import time
import re
import collections
import numpy as np

letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
, 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
vowels = {'a', 'e', 'i', 'o', 'u'}

class Hangman(object):
    def __init__(self):
        self.full_dictionary = self.build_dictionary("train.txt")
        self.dict_word = self.build(self.full_dictionary)
        self.current_dictionary = self.full_dictionary
        self.guessed = []
        self.notGuessed = []

    def build(self, dict):
        temp = {i: [] for i in range(2, 40)}
        for i in range(2, 40):
            for x in dict:
                if len(x) > i:
                    for j in range(len(x)-i+1):
                        temp[i].append(x[j:j+i])
        return temp

    def build_dictionary(self, dictionary_file_location):
        text_file = open(dictionary_file_location, "r")
        dictionary = text_file.read().splitlines()
        text_file.close()
        return dictionary

    def helper(self, p, guess_word):    
        l = len(guess_word)
        xx = int(l/p)
        if xx >= 3: 
            ans = collections.defaultdict(int)
            for i in range(l-xx+1):
                s = guess_word[i:i+xx]
                new = []
                for y in self.dict_word[len(s)]:
                    flagg = 0
                    for i in range(len(s)):
                        if y[i] != s[i] and s[i]!='.':
                            flagg = 1
                            break
                    if flagg == 0:
                        new.append(y)
                res = collections.defaultdict(int)
                for x in new:
                    for y in set(x):
                        res[y] += 1
                res = sorted(res.items(), key=lambda x: (-1 * x[1], x[0]))
                for k, j in res:
                    ans[k] += j
            ans = sorted(ans.items(), key=lambda x: (-1 * x[1], x[0]))
            for x, y in ans:
                if x not in self.guessed:
                    return x
        return ''

    def updateDict(self, l, guess_word):
        temp = []
        for x in self.current_dictionary:
            if len(x) == l:
                flag = 0
                for i in range(l):
                    if guess_word[i] != '.' and x[i] != guess_word[i]:
                        flag = 1
                        break
                if flag == 0:
                    temp.append(x)
        self.current_dictionary = temp
    
    def guess(self, word):  # word input example: "_ p p _ e "
        
        guess_word = word[::2].replace("_", ".")
        incorrectGuess = list(set(self.guessed) - set(guess_word))
        l = len(guess_word)
        # possibleLetters = sorted(set("".join(self.current_dictionary)))

        self.updateDict(l,guess_word)
        
        flag = 0
        cnt = 0
        for i in range(l):
            if guess_word[i] in vowels:
                cnt+=1
        if 2*cnt >= l:
            flag = 1
        for i in range(l):
            if guess_word != '.':
                cnt+=1
        
        if len(self.current_dictionary)>=1 and len(incorrectGuess)<=3:
            res = {x:0 for x in letters}
            for x in self.current_dictionary:
                for y in set(x):
                    res[y] += 1
            res = sorted(res.items(), key=lambda x:(-1*x[1], x[0]))
            for x, y in res:
                if y<=0:
                    break
                if x not in self.guessed and (x not in vowels or (x in vowels and flag == 0)):
                    return x

        new = []
        for y in self.dict_word[l]:
            flagg = 0
            for i in range(l):
                if y[i] in incorrectGuess or (y[i] != guess_word[i] and guess_word[i]!='.'):
                    flagg = 1
                    break
            if flagg == 0:
                new.append(y)
                
        if len(new) >= 1 and len(incorrectGuess)<=4:
            res = collections.defaultdict(int)
            for x in new:
                for y in set(x):
                    res[y] += 1
            res = sorted(res.items(), key=lambda x:(-1*x[1], x[0]))
            for x, y in res:
                if x not in self.guessed and (x not in vowels or (x in vowels and flag == 0)):
                    return x

        for t in range(2, 6):
            guess_letter = self.helper(t, guess_word)
            if guess_letter != '':
                return guess_letter

        res = {x:0 for x in letters}
        for x in self.full_dictionary:
            for y in set(x):
                res[y] += 1
        res = sorted(res.items(), key=lambda x: (-1 * x[1], x[0]))
        for x, y in res:
            if x not in self.guessed:
                return x
