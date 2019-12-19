import random

wordsToPlayWith = ['horse', 'tractor', 'goat', 'chicken', 'tuesday' ]




def printWord(word):

    outWord = ' '.join(word)
    print('-' * len(outWord))
    print(outWord)
    print('-' * len(outWord) + '\n')

def produceProgessWord(wordToGuess):
    progress = []
    for letter in wordToGuess:
        if letter == ' ':
            progress.append('/')
        else:
            progress.append('_')
    return progress 

def checkAndReveal(guess, progressWord, wordToGuess):
    continueGame = None
    for index, letter in enumerate(wordToGuess):
        if letter == guess:
            print(f'found {letter}')
            progressWord[index] = letter

    print(' '.join(progressWord))

    if '_' in progressWord:
        continueGame = True
    else:
        continueGame = False
    
    return continueGame, progressWord


def getGuess(previousGuesses):
    
    validGuess = False
    while not validGuess:
        print(f'Previous guesses are: {previousGuesses}')
        print('Guess a letter!')
        inputLetter = input(': ').upper()
        if inputLetter not in previousGuesses:
            return inputLetter           
        else:
            print('You already entered that letter. Try again!')
        




difficulty = 12

def hangmanGame(howManyChances):

    wordToGuess = random.choice(wordsToPlayWith).upper()
    progressWord = produceProgessWord(wordToGuess)
    guessedLetters = []
    currentGuess = None
    playing = True

    while playing:
        playing, progressWord = checkAndReveal(currentGuess, progressWord, wordToGuess)
        if playing:
            currentGuess = getGuess(guessedLetters)
            guessedLetters.append(currentGuess)
    
    print('You guessed the word!')
        
for n in range(6):

    hangmanGame(difficulty)







