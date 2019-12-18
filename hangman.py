import random

wordList = ['telescope', 'orange', 'toy car']
wordToGuess = wordList[2]

hiddenWordList = []
for letter in wordToGuess:
    if letter.isalpha():
        hiddenWordList.append('_')
    elif letter.isspace():
        hiddenWordList.append(' ')

# This part helps for displaying the word in this test CLI version.
hiddenWordString = ' / '.join(hiddenWordList)    

wordGuessed = False

guessedLetters = []



def revealGuessedLetters(guessedLetters, wordToGuess):
    partiallyRevealed = []
    
 
    for hiddenLetter in wordToGuess:
        if hiddenLetter in guessedLetters:
            partiallyRevealed.append(hiddenLetter)
        else:
            if hiddenLetter.isspace():
                partiallyRevealed.append(' ')
            else:
                partiallyRevealed.append('_')
    return partiallyRevealed
        
def getNextGuess(guessedLetters):
    while True:
        currentGuess = input('Guess a letter: ').lower()
        if currentGuess not in guessedLetters:
            break
    guessedLetters.append(currentGuess)
    return guessedLetters

def winCondition(progressWord, hiddenWord):
    if '_' not in  progressWord:
        return True
    else:
        return False


while not wordGuessed:
    progressWord = revealGuessedLetters(guessedLetters, wordToGuess)
    print(' / '.join(progressWord))
    guessedLetters = getNextGuess(guessedLetters)

    wordGuessed = winCondition(progressWord, wordToGuess)
