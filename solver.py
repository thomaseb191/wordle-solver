#!/usr/bin/python3
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
                    if len(Solver.allowed_letters[i]) != 1:
                        Solver.allowed_letters[i] = Solver.allowed_letters[i].replace(letter, '')
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
            

def main():
    initGame()
    run()

if __name__ == "__main__":
    main()
