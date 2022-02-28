#!/usr/bin/python3
from urllib import response


class Solver:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    empty_freqs = {}
    word_list = []
    allowed_list = []

    allowed_letters = []

    def parseWord(word):
        i = 0
        for l in word:
            if l not in Solver.allowed_letters[i]:
                Solver.allowed_letters[i] += l
            i += 1

    def initGame():
        word_csv = open("data/wordle_small.txt", "r")

        first = word_csv.readline().strip()

        i = 0
        for l in first:
            Solver.allowed_letters.insert(i, l)
            i += 1

        Solver.word_list.append(first)
        Solver.allowed_list.append(first)
        for word in word_csv:
            Solver.word_list.append(word.strip())
            Solver.allowed_list.append(word.strip())
            Solver.parseWord(word.strip())
        word_csv.close()

        word_csv = open("data/wordle_large.txt", "r")
        for word in word_csv:
            if word not in Solver.allowed_list:
                Solver.allowed_list.append(word.strip())
                Solver.parseWord(word.strip())
        word_csv.close()

        Solver.allowed_list.sort()
        Solver.word_list.sort()

        for letter in Solver.alphabet:
            Solver.empty_freqs[letter] = 0

    def gen_response(guess, solution):
        if len(guess) != len(solution):
            print("Guess length does not match answer length, please retry")
            raise ValueError
        
        if guess == solution:
            return "22222"

        #Code snagged from here:
        # https://mathspp.com/blog/solving-wordle-with-python
        pool = {}
        for g, s in zip(guess, solution):
            if g == s:
                continue
            if s in pool:
                pool[s] += 1
            else: 
                pool[s] = 1

        response = []
        for guess_letter, solution_letter in zip(guess, solution):
            if guess_letter == solution_letter:
                response += 2
            elif guess_letter in solution and guess_letter in pool and pool[guess_letter] > 0:
                response += 1
                pool[guess_letter] -= 1
            else:
                response += 0
        return response

    def skip_word(word, contained):        
        i = 0
        for l in contained:
            if contained.count(l) > word.count(l):
                return False

        for l in word:
            if l not in Solver.alphabet:
                continue
            if l not in Solver.allowed_letters[i]:
                return False
            i += 1
        return True

    def run():
        contained = ""


        response = "00000"

        num_guesses = 0

        while response != "22222":
            num_guesses += 1
            letter_frequency = Solver.empty_freqs.copy()

            for word in Solver.word_list:
                if not Solver.skip_word(word, contained):
                    continue
                for letter in word:
                    if letter not in Solver.alphabet:
                        continue
                    letter_frequency[letter] += 1
                print(word)

            for word in Solver.allowed_list:
                if not Solver.skip_word(word, contained):
                    continue
                #for letter in word:
                #    if letter not in Solver.alphabet:
                #        continue
                #    letter_frequency[letter] += 1
                #print(word)

            marklist = sorted(letter_frequency.items(), key=lambda x:x[1], reverse=True)
            sortdict = dict(marklist)

            for key in sortdict:
                if sortdict[key] == 0:
                    continue
                print(key, sortdict[key])

            guess = input("Guess: ")

            if guess == "EXIT":
                print("Exiting program")
                return

            response = input("Response: ")

            if len(guess) != len(response):
                print("Guess length does not match response length, please retry")
                continue

            solved_letters = ""

            for i in range(5):
                num    = int(response[i])
                letter = guess[i]
                if num == 0:
                    for x in range(len(Solver.allowed_letters)):
                        if len(Solver.allowed_letters[x]) != 1:
                            Solver.allowed_letters[x] = Solver.allowed_letters[x].replace(letter, '')
                elif num == 1:
                    Solver.allowed_letters[i] = Solver.allowed_letters[i].replace(letter, '')
                    contained = contained.replace(letter, '')
                    solved_letters += letter
                elif num == 2:
                    solved_letters += letter
                    contained = contained.replace(letter, '')
                    Solver.allowed_letters[i] = letter
                else:
                    raise ValueError
            
            contained += solved_letters
            
            print(Solver.allowed_letters, contained)

        print("Solved in %d guess(es)" % num_guesses)