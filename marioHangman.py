import random, openpyxl, os, pygame, sys
from pygame.locals import *
import marioAssets
from string import ascii_lowercase

# wordsToPlayWith = ['horse', 'tractor', 'goat', 'chicken', 'tuesday' ]
alphabet = [letter for letter in ascii_lowercase]


def printWord(word):

    outWord = ' '.join(word)
    print('-' * len(outWord))
    print(outWord)
    print('-' * len(outWord) + '\n')

def produceProgessWord(wordToGuess):
    progress = []
    for letter in wordToGuess:
        if letter == ' ':
            progress.append(' ')
        else:
            progress.append('?')
    return progress 

def checkAndReveal(guess, progressWord, wordToGuess):
    continueGame = None
    for index, letter in enumerate(wordToGuess):
        if letter == guess:
            print(f'found {letter}')
            progressWord[index] = letter

    print(' '.join(progressWord))

    if '?' in progressWord:
        hasWon = False
    else:
        hasWon = True
    return hasWon, progressWord

def calculateScore(previousGuesses, progressWord):
    return len([letter for letter in previousGuesses if letter not in progressWord])

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
        


def excelGetGameScheme(book, units):
    path = r'C:\Come On Python Games\resources\marioHangman\quiz'
    bookPath = f'{book}.xlsx'
    excelPath = os.path.join(path, bookPath)

    

    wb = openpyxl.load_workbook(excelPath)
    
    wordsLoadedFromExcel = []
    for unit in units:
    
        sheet = wb[unit]
        row = 1
        endOfWords = False
        while not endOfWords:
            cellContents = sheet.cell(row=row, column=1).value
            if not cellContents:
                endOfWords = True
            else:
                wordsLoadedFromExcel.append(cellContents)
                row += 1
    return wordsLoadedFromExcel

    



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
        

book = 'EB2'
unit = ['U1', 'U2', 'U3']

# TODO
# There should be a menu for books,
# And a menu for units, where you can select multiple units.
# It will need a submit button


wordsToPlayWith = excelGetGameScheme(book, unit)


FPS = 30

WINDOWWIDTH = 1024
WINDOWHEIGHT = 786

BLACK           =(  0,   0, 0)
WHITE           =(255, 255, 255)

BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK


def hangmanRound(initObjects, difficulty=12):
    screen = initObjects[0]
    FPSCLOCK = initObjects[1]
    DISPLAYSURF = initObjects[2]
    DISPLAYRECT = initObjects[3]

    sessionWord = random.choice(wordsToPlayWith)

    progress = produceProgessWord(sessionWord)
    guessedLetters = []
    wonTheGame = False
    currentScore = 0
    

    key = None
    while True:
        checkForQuit()

        
        #Event-related variables:
        newW, newH = None, None
        submitLetter = False

        #Event-reading loop:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newW, newH = event.size
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key in (K_RETURN, K_KP_ENTER):
                    submitLetter = True
                else:
                    key = event.key

        
        if newW and newH:
            screen = pygame.display.set_mode((newW, newH ), pygame.RESIZABLE, display=0)
            DISPLAYRECT.center = (newW/2, newH/2)
        
        screen.fill(BLACK)
        DISPLAYSURF.blit(marioAssets.bkImage, (0, 0))

        
        # Drawing the ??? filled secret word
        qBox = marioAssets.boxImg
        qBoxRect = qBox.get_rect()
        qBoxRect.centery = WINDOWHEIGHT/4
        startingX = WINDOWWIDTH/4
        boxSpacing = 56
        charCount = 0

        for char in progress:
            charCount += 1
            if char == '?':
                qBoxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(qBox, qBoxRect)
            else:
                boxSurf = marioAssets.alphaBoxDict[char]
                boxRect = boxSurf.get_rect()
                boxRect.centery = WINDOWHEIGHT/4
                boxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(boxSurf, boxRect)               

        # Drawing the remaining alphabet boxes
        alphaMenuTopY = (WINDOWHEIGHT/4) * 2.6
        alphaMenuBottomY = alphaMenuTopY + boxSpacing*2
        alphaMenuXIndent = WINDOWWIDTH/7
        for number, letter in enumerate(marioAssets.alphaBoxDict.keys()):
            boxXCount = number+1
            alphaBoxSurf = marioAssets.alphaBoxDict[letter] 
            alphaBoxRect = alphaBoxSurf.get_rect()
            if number > 12:
                boxXCount -= 13
                alphaBoxRect.centery = alphaMenuBottomY
            else:
                alphaBoxRect.centery = alphaMenuTopY
            alphaBoxRect.centerx = alphaMenuXIndent + (boxSpacing * boxXCount)
            if letter in guessedLetters:
                continue
            else:
                DISPLAYSURF.blit(alphaBoxSurf, alphaBoxRect)

        # Drawing Mario
        marioX = 72
        marioY = 418
        mario = marioAssets.Mario
        marioSurf = mario.surface
        marioRect = mario.rect
        marioRect.bottomleft = ((marioX, marioY))
        DISPLAYSURF.blit(marioSurf, marioRect)


        #Submit chosen letter, and add to guessed letters
        if key and submitLetter:
            if key > 96 and key < 123:
                letterIndex = key - 97
                letterChosen = alphabet[letterIndex]
                if letterChosen not in guessedLetters:
                    guessedLetters.append(letterChosen)
                    print(letterChosen)
                    wonTheGame, progress = checkAndReveal(letterChosen, progress, sessionWord)
                    currentScore = calculateScore(guessedLetters, progress)
                    print(currentScore)
                else:
                    print('Already tried that letter')
                key = None
        
        if currentScore >= difficulty:
            print('You lose')
            return 'LOSE'
        if wonTheGame:
            print('Winner Winner, Chicken Dinner')
            return 'WIN'

        
        
        
        
        
        
        screen.blit(DISPLAYSURF, DISPLAYRECT)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
        





def terminate():
    print('Terminating game...')
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def main():

    FPSCLOCK = pygame.time.Clock()

    BKGWIDTH = WINDOWWIDTH
    BKGHEIGHT = WINDOWHEIGHT

    screen = pygame.display.set_mode((BKGWIDTH, BKGHEIGHT), pygame.RESIZABLE, display=0)
    pygame.display.set_caption('Mario Hangman')

    DISPLAYSURF = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYRECT = DISPLAYSURF.get_rect()
    DISPLAYRECT.center = (BKGWIDTH/2, BKGHEIGHT/2)
    
    initObjects = [screen, FPSCLOCK, DISPLAYSURF, DISPLAYRECT]
    while True:
        roundResult = hangmanRound(initObjects)



    





main()
