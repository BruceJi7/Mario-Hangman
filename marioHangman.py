import random, openpyxl, os, pygame, sys
from pygame.locals import *
import marioAssets
from string import ascii_lowercase

# wordsToPlayWith = ['horse', 'tractor', 'goat', 'chicken', 'tuesday' ]
alphabet = [letter for letter in ascii_lowercase]

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

def excelGetGameScheme(book, units):
    
    excelPath = r'C:\Come On Python Games\resources\marioHangman\quiz\marioQuiz.xlsx'
    
    wb = openpyxl.load_workbook(excelPath)
    
    wordsLoadedFromExcel = []
    
    sheet = wb[book]
    

    for unit in units:
        row = 2
        endOfWords = False
        while not endOfWords:
            cellContents = sheet.cell(row=row, column=unit).value
            if not cellContents:
                endOfWords = True
            else:
                wordsLoadedFromExcel.append(cellContents.lower())
                row += 1
    random.shuffle(wordsLoadedFromExcel)
    return wordsLoadedFromExcel


def getBooks():
    excelPath = r'C:\Come On Python Games\resources\marioHangman\quiz\marioQuiz.xlsx'
    
    wb = openpyxl.load_workbook(excelPath)
    
    sheets = wb.sheetnames
    print(sheets)
    return sheets

difficulty = 12

     

# book = 'NP'
# unit = ['U3']
# unit = ['U1', 'U2', 'U3', 'U4']

# TODO
# There should be a menu for books,
# And a menu for units, where you can select multiple units.
# It will need a submit button


FPS = 30

WINDOWWIDTH = 1024
WINDOWHEIGHT = 786

BLACK           =(  0,   0, 0)
WHITE           =(255, 255, 255)

BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK

def marioFont(size=35):
    pygame.font.init()
    return pygame.font.SysFont('minecraft', size)

menuFont = marioFont()

def beginMusic(track):
    pygame.mixer.init()
    pygame.mixer.music.load(marioAssets.music[track])
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)


def hangmanRound(initObjects, difficulty=12):
    screen = initObjects[0]
    FPSCLOCK = initObjects[1]
    DISPLAYSURF = initObjects[2]
    DISPLAYRECT = initObjects[3]
    wordsToPlayWith = initObjects[4]

    sessionWord = random.choice(wordsToPlayWith)
    try:
        wordsToPlayWith.remove(sessionWord)
        print(len(wordsToPlayWith))
    except:
        print('Failed to remove word')

    print(sessionWord)
    progress = produceProgessWord(sessionWord)
    guessedLetters = []
    wonTheGame = False
    currentScore = 0
    
    mario = marioAssets.Mario
    mario.state = 'standing'

    musicBkg = random.choice(['world1', 'world2', 'cave'])
    bkgImg = marioAssets.backgrounds[musicBkg]

    beginMusic(musicBkg)
    

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
            elif event.type == USEREVENT:
                beginMusic(musicBkg)
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
        DISPLAYSURF.blit(bkgImg, (0, 0))

        
        # Drawing the ??? filled secret word
        qBox = marioAssets.boxImg
        qBoxRect = qBox.get_rect()
        qBoxRect.centery = WINDOWHEIGHT/4
        startingX = 100
        boxSpacing = 56
        charCount = 0

        for char in progress:
            charCount += 1
            if char == '?':
                qBoxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(qBox, qBoxRect)
            elif char == ' ':
                continue
            else:
                boxSurf = marioAssets.alphaBoxDict[char]
                boxRect = boxSurf.get_rect()
                boxRect.centery = WINDOWHEIGHT/4
                boxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(boxSurf, boxRect)               

        # Drawing the remaining alphabet boxes
        alphaMenuTopY = (WINDOWHEIGHT/4) * 3
        alphaMenuBottomY = alphaMenuTopY + boxSpacing
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
                alphaBoxSurf = marioAssets.usedBox

            
            DISPLAYSURF.blit(alphaBoxSurf, alphaBoxRect)

        # Drawing Mario
        marioX = 72
        marioY = 418
        marioSurf = mario.surface
        marioRect = mario.rect
        marioRect.bottomleft = ((marioX, marioY))
        DISPLAYSURF.blit(marioSurf, marioRect)

        # Drawing the enemy
        enemyX = marioX + (64 * (difficulty - currentScore)) # Calculate from Mario's position
        enemyY = 418 + 42
        enemy = marioAssets.Goomba
        if currentScore % 2:
            enemy.direction = 'LEFT'
        else:
            enemy.direction = 'RIGHT'
        enemySurf = enemy.surface
        enemyRect = enemy.rect
        enemyRect.bottomleft = ((enemyX, enemyY))
        DISPLAYSURF.blit(enemySurf, enemyRect)




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
            return 'LOSE', sessionWord, progress, musicBkg
        if wonTheGame:
            print('Winner Winner, Chicken Dinner')
            return 'WIN', sessionWord, progress, musicBkg

        
        
        
        
        
        
        screen.blit(DISPLAYSURF, DISPLAYRECT)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

def getHowManyUnits(book):

    excelPath = r'C:\Come On Python Games\resources\marioHangman\quiz\marioQuiz.xlsx'
    
    wb = openpyxl.load_workbook(excelPath)
    
    wordsLoadedFromExcel = []
    
    sheet = wb[book]
    
    endOfWords = False

    unit = 1
    unitColumns = []
    while not endOfWords:

        cellContents = sheet.cell(row=1, column=unit).value
        if not cellContents:
            endOfWords = True
        else:
            unitColumns.append(cellContents)
            unit += 1

    return unitColumns


def startMenu(initObjects):
    screen = initObjects[0]
    FPSCLOCK = initObjects[1]
    DISPLAYSURF = initObjects[2]
    DISPLAYRECT = initObjects[3]

    booksheets = getBooks()
    bookIndex = 0
    
    menuType = 'book'

    numberKey = None

    chosenUnits = []
    chosenBook = None

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
                elif event.key == K_UP:
                    bookIndex -= 1
                elif event.key == K_DOWN:
                    bookIndex += 1
                else:
                    numberKey = event.key
            
        
        if bookIndex > len(booksheets)-1:
            bookIndex = 0
        elif bookIndex < 0:
            bookIndex = len(booksheets)-1

        screen.fill(BLACK)
        DISPLAYSURF.blit(marioAssets.menuBKG, (0, 0))
        
        if newW and newH:
            screen = pygame.display.set_mode((newW, newH ), pygame.RESIZABLE, display=0)
            DISPLAYRECT.center = (newW/2, newH/2)
        if menuType == 'book':
            bookSelection = booksheets[bookIndex]
            menuLabel = menuFont.render(f'- {bookSelection} -', 1, BLACK)
            menuRect = menuLabel.get_rect()

            menuRect.center = ((WINDOWWIDTH/2, 450))

            DISPLAYSURF.blit(menuLabel, menuRect)

        if menuType == 'unit':
            getUnits = False
            presentUnits = 8
            if getUnits == False:
                presentUnits = len(getHowManyUnits(bookSelection))
                getUnits = True
            

            boxSpacing = 56
            numMenuTopY = 500
            numMenuBottomY = numMenuTopY + boxSpacing
            numMenuXIndent = WINDOWWIDTH/2 - (boxSpacing * (presentUnits/2+1))

            for unit in range(1, presentUnits+1):
                boxXCount = unit+1
                numBoxSurf = marioAssets.numBoxDict[str(unit)]
                numBoxRect = numBoxSurf.get_rect()
                if unit > 12:
                    boxXCount -= 13
                    numBoxRect.centery = numMenuBottomY
                else:
                    numBoxRect.centery = numMenuTopY
                numBoxRect.centerx = numMenuXIndent + (boxSpacing * boxXCount)
                if unit in chosenUnits:
                    numBoxSurf = marioAssets.usedBox

            
                DISPLAYSURF.blit(numBoxSurf, numBoxRect)

                if numberKey:
                    unitNumber = numberKey -48

                    if unitNumber not in chosenUnits:
                        chosenUnits.append(unitNumber)
                    else:
                        chosenUnits.remove(unitNumber)

                    numberKey = None


        if submitLetter and menuType == 'book':
            chosenBook = bookSelection
            menuType = 'unit'

        elif submitLetter and menuType == 'unit':
            if len(chosenUnits) >= 1:
                print(f'Playing with words from book {chosenBook}, unit(s) {chosenUnits}')
                return chosenBook, chosenUnits
        
    
            


        screen.blit(DISPLAYSURF, DISPLAYRECT)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)




def winScreen(initObjects, word, background):
    screen = initObjects[0]
    FPSCLOCK = initObjects[1]
    DISPLAYSURF = initObjects[2]
    DISPLAYRECT = initObjects[3]

    musicTrack = marioAssets.winSound
    pygame.mixer.music.load(musicTrack)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

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


        
        if newW and newH:
            screen = pygame.display.set_mode((newW, newH ), pygame.RESIZABLE, display=0)
            DISPLAYRECT.center = (newW/2, newH/2)

        if submitLetter:
            return
        
        screen.fill(BLACK)
        DISPLAYSURF.blit(marioAssets.backgrounds[background], (0, 0))

        marioX = 72
        marioY = 418
        mario = marioAssets.Mario
        mario.state = 'win'
        marioSurf = mario.surface
        marioRect = mario.rect
        marioRect.bottomleft = ((marioX, marioY))
        DISPLAYSURF.blit(marioSurf, marioRect)

        qBox = marioAssets.boxImg
        qBoxRect = qBox.get_rect()
        qBoxRect.centery = WINDOWHEIGHT/4
        startingX = 100
        boxSpacing = 56
        charCount = 0

        for char in word:
            charCount += 1

            if char == ' ':
                continue
            else:

                boxSurf = marioAssets.alphaBoxDict[char]
                boxRect = boxSurf.get_rect()
                boxRect.centery = WINDOWHEIGHT/4
                boxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(boxSurf, boxRect)  


        screen.blit(DISPLAYSURF, DISPLAYRECT)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

def loseScreen(initObjects, word, progress, background):
    screen = initObjects[0]
    FPSCLOCK = initObjects[1]
    DISPLAYSURF = initObjects[2]
    DISPLAYRECT = initObjects[3]

    mario = marioAssets.Mario
    mario.state = 'fail'

    musicTrack = marioAssets.loseSound
    pygame.mixer.music.load(musicTrack)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    showWord = False
    finished = False



    while True:
        checkForQuit()

        
        #Event-related variables:
        newW, newH = None, None
        submit = 0

        #Event-reading loop:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newW, newH = event.size
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key in (K_RETURN, K_KP_ENTER):
                    if showWord == True:
                        finished = True

                    if showWord == False:
                        showWord = True
                    

        if finished:
            return

        
        if newW and newH:
            screen = pygame.display.set_mode((newW, newH ), pygame.RESIZABLE, display=0)
            DISPLAYRECT.center = (newW/2, newH/2)
        
        screen.fill(BLACK)
        DISPLAYSURF.blit(marioAssets.backgrounds[background], (0, 0))

        marioX = 72
        marioY = 418
        
        marioSurf = mario.surface
        marioRect = mario.rect
        marioRect.bottomleft = ((marioX, marioY))
        DISPLAYSURF.blit(marioSurf, marioRect)

        qBox = marioAssets.boxImg
        qBoxRect = qBox.get_rect()
        qBoxRect.centery = WINDOWHEIGHT/4
        startingX = 100
        boxSpacing = 56
        charCount = 0

        if showWord:
            progress = word

        for char in progress:
            charCount += 1
            if char == '?':
                qBoxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(qBox, qBoxRect)
            elif char == ' ':
                continue
            else:
                boxSurf = marioAssets.alphaBoxDict[char]
                boxRect = boxSurf.get_rect()
                boxRect.centery = WINDOWHEIGHT/4
                boxRect.centerx = startingX + (boxSpacing*charCount)
                DISPLAYSURF.blit(boxSurf, boxRect) 


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

    book, units = startMenu(initObjects)
    wordsToPlayWith = excelGetGameScheme(book, units)
    random.shuffle(wordsToPlayWith)

    initObjects.append(wordsToPlayWith)

    while True:
        roundResult, word, progress, bkg = hangmanRound(initObjects)
        if roundResult == 'WIN':
            winScreen(initObjects, word, bkg)
        elif roundResult == 'LOSE':
            loseScreen(initObjects, word, progress, bkg)




    




   
main()
