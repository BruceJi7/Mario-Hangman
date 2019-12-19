import logging, random
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)


wordsToPlayWith = ['horse', 'tractor', 'goat', 'chicken' ]

# This prints the word with the leading and trailing ----s.
def printHidden(word):
    outWord = ' '.join(word)
    print('-' * len(outWord))
    print(outWord)
    print('-' * len(outWord) + '\n')
    

def startGame(chances):
    targetWord = random.choice(wordsToPlayWith)
    logging.debug(f'Word is {targetWord}\n')
    
    secretWord = [char.upper() for char in targetWord]
    guessedLetters = []
        
    return (secretWord, obfuscate(secretWord), chances, guessedLetters)


def getGuess():
    guess = input('Guess a letter:\n').upper()
    logging.debug(f'Guess is {guess}\n')
    return guess

def obfuscate(inwordL):
    secretWord = ['_' for char in inwordL]
    if ' ' in inwordL:
        for index, char in enumerate(inwordL):
            if char == ' ':
                secretWord[index] = '/'
    return secretWord

def revealLetter(guess, wordT):
    targetWord = wordT[0]
    hiddenWord = wordT[1]
    chances = wordT[2]
    guessedLetters = wordT[3]
    
    if guess in guessedLetters: # What if you enter a letter twice?
        print('That letter has already been guessed')
        printHidden(hiddenWord)
        print(f'Letters guessed so far: {", ".join(guessedLetters)}')
        return(targetWord, hiddenWord, chances, guessedLetters)
    else:
        if guess in targetWord: # If your guess is correct
            guessedLetters.append(guess) # Add guess to guessed letter
            for index, char in enumerate(targetWord): # Handles replacing _ for the correct letter
                if char == guess:
                    hiddenWord[index] = targetWord[index]
                    logging.debug(f'{hiddenWord} character {hiddenWord[index]} matched')
            print(f'{guess} is in the word!')    
            printHidden(hiddenWord)
            print(f'Letters guessed so far: {", ".join(guessedLetters)}')
            return(targetWord, hiddenWord, chances, guessedLetters)
                
        else:
            chances -= 1 # If you are wrong, lose a chance.
            guessedLetters.append(guess)
            print(f'{guess} is not in the word\n')
            printHidden(hiddenWord)
            print(f'Letters guessed so far: {", ".join(guessedLetters)}')
            return(targetWord, hiddenWord, chances, guessedLetters)

def checkProgress(wordT):

    hiddenWord = wordT[1]
    
    if '_' in hiddenWord:
        return False
    else:
        return True

# Below is game code:
 
print("Let's play hangman!\n")
difficulty = 12       
secretWordT = startGame(difficulty)
print(f'Okay. You now have {difficulty} guesses to guess the word\n')

remainingChances = difficulty
while remainingChances > 0:
    
    guess = getGuess()
    updatedWord = revealLetter(guess, secretWordT)
    secretWordT = updatedWord
    if checkProgress(updatedWord):
        print('Word successfully guessed!')
        break
    else:
        remainingChances = updatedWord[2]
        if remainingChances == 1:
            guessplu = 'guess'
        else:
            guessplu = 'guesses'
        print(f'You have {remainingChances} {guessplu} left!')
print(f"The game is over! The word was {''.join(secretWordT[0])}")   