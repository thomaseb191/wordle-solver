#!/usr/bin/python3

import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"
empty_freqs = {}
word_list = []

def initGame():
    word_csv = open("data/words.csv", "r")
    for word in word_csv:
        word_list.append(word.strip())
    word_csv.close()

    for letter in alphabet:
        empty_freqs[letter] = 0

def run():
    letters_in = ""

    dissallowed = ""

    notin = [   "",
            "",
            "",
            "",
            ""
    ]

    solved = ["", "" , "", "", ""]

    response = "00000"

    num_guesses = 0

    while response != "22222":
        num_guesses += 1
        letter_frequency = empty_freqs.copy()

        for word in word_list:
            should_use = True
    
            for l in dissallowed:
                if l in word:
                    should_use = False
            for l in letters_in:
                if l not in word:
                    should_use = False
            i = 0
            for l in word:
                if (solved[i] != "") and (l != solved[i]):
                    should_use = False
                i += 1
            i = 0
            for l in word:
                if l not in alphabet:
                    continue
                if l in notin[i]:
                    should_use = False
                i += 1
            if not should_use:
                continue
            for letter in word:
                if letter not in alphabet:
                    continue
                letter_frequency[letter] += 1
            print(word)

        marklist = sorted(letter_frequency.items(), key=lambda x:x[1], reverse=True)
        sortdict = dict(marklist)

        for key in sortdict:
            if sortdict[key] == 0:
                continue
            print(key, sortdict[key])

        guess = input("Guess: ")
        response = input("Reponse: ")

        for i in range(5):
            num    = int(response[i])
            letter = guess[i]
            if num == 0:
                if letter in letters_in:
                    skip = [index for index in range(len(solved)) if solved[index] == letter]
                    for j in range(5):
                        if j in skip:
                            continue
                        notin[j] += letter
                else:
                    dissallowed += letter
            elif num == 1:
                letters_in += letter
                notin[i] += letter
            elif num == 2:
                solved[i] = letter
            else:
                raise ValueError
    print("Solved in %d guess(es)" % num_guesses)
            

def main():
    initGame()
    run()

if __name__ == "__main__":
    main()
