#!/usr/bin/python3
class Solver:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    empty_freqs = {}
    word_list = []
    allowed_list = []

    def initGame():
        word_csv = open("data/wordle_small.txt", "r")
        for word in word_csv:
            Solver.word_list.append(word.strip())
            Solver.allowed_list.append(word.strip())
        word_csv.close()

        word_csv = open("data/wordle_large.txt", "r")
        for word in word_csv:
            if word not in Solver.allowed_list:
                Solver.allowed_list.append(word.strip())
        word_csv.close()

        Solver.allowed_list.sort()
        Solver.word_list.sort()

        for letter in Solver.alphabet:
            Solver.empty_freqs[letter] = 0

    def gen_response(guess, answer):
        if len(guess) != len(answer):
            print("Guess length does not match answer length, please retry")
            raise ValueError

        response = ""
        for i in range(len(guess)):
            if guess[i] in answer and guess[i] == answer[i]:
                response += "2"
            elif guess[i] in answer and guess[i] != answer[i]:
                response += "1"
            elif guess[i] not in answer:
                response += "0"

        return response

    def skip_word(word, dissallowed, letters_in, not_in, solved):
        should_use = True
        
        for l in dissallowed:
            if l in word:
                should_use = False
        for l in letters_in:
            if l not in word:
                should_use = False
            num_letter = letters_in.count(l)
            if num_letter > word.count(l):
                should_use = False
        i = 0
        for l in word:
            if l not in Solver.alphabet:
                continue
            if (l in not_in[i]) and (l != solved[i]):
                should_use = False
            if (solved[i] != "") and (l != solved[i]):
                should_use = False
            i += 1
        return should_use

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
            letter_frequency = Solver.empty_freqs.copy()

            for word in Solver.word_list:
                if not Solver.skip_word(word, dissallowed, letters_in, notin, solved):
                    continue
                for letter in word:
                    if letter not in Solver.alphabet:
                        continue
                    letter_frequency[letter] += 1
                #print(word)

            for word in Solver.allowed_list:
                if not Solver.skip_word(word, dissallowed, letters_in, notin, solved):
                    continue

                print(word)

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

            response = input("Reponse: ")

            if len(guess) != len(response):
                print("Guess length does not match response length, please retry")
                continue

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
                    if letter not in letters_in:
                        letters_in += letter
                    notin[i] += letter
                elif num == 2:
                    solved[i] = letter
                    if letter not in letters_in:
                        letters_in += letter
                else:
                    raise ValueError
            
            print(letters_in, dissallowed, notin, solved)

        print("Solved in %d guess(es)" % num_guesses)
            

def main():
    initGame()
    run()

if __name__ == "__main__":
    main()
