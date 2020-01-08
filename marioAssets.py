import pygame, sys, random, os
from pygame.locals import *
from string import ascii_uppercase, ascii_lowercase


backgroundPath = r'C:\Come On Python Games\resources\marioHangman\background\bkg.png'
bkgPath = r'C:\Come On Python Games\resources\marioHangman\background'
backgrounds = {
    'world1' : pygame.image.load(os.path.join(bkgPath, 'bkg.png')),
    'world2' : pygame.image.load(os.path.join(bkgPath, 'world2.png')),
    'cave' : pygame.image.load(os.path.join(bkgPath, 'cave.png')),
}

bkImage = pygame.image.load(backgroundPath)

boxPath = r'C:\Come On Python Games\resources\marioHangman\background\box.png'

boxImg = pygame.image.load(boxPath)

alphaboxPath = r'C:\Come On Python Games\resources\marioHangman\box'
alphaBoxImgs = [pygame.image.load(os.path.join(alphaboxPath, f'{letter}.PNG')) for letter in ascii_uppercase]

alphaBoxDict = {}
for letter in range(len(alphaBoxImgs)):
    keyLetter = ascii_lowercase[letter]
    valueImage = alphaBoxImgs[letter]
    alphaBoxDict[keyLetter] = valueImage

blankBox = pygame.image.load(os.path.join(alphaboxPath, 'blank.PNG'))

LEFT = 'LEFT'
RIGHT = 'RIGHT'
characterPath = r'C:\Come On Python Games\resources\marioHangman\character'
marioCharacterPath = os.path.join(characterPath, 'mario')
marioPaths = {
    'standing': {
                'RIGHT': pygame.image.load(os.path.join(marioCharacterPath, 'marioStandingRight.png')),
                'LEFT' : pygame.image.load(os.path.join(marioCharacterPath, 'marioStandingLeft.png')),
                },
    'win':      {
                'RIGHT': pygame.image.load(os.path.join(marioCharacterPath, 'marioWin.png')),
                'LEFT': pygame.image.load(os.path.join(marioCharacterPath, 'marioWin.png'))
                },
    'fail':
                {
                'RIGHT': pygame.image.load(os.path.join(marioCharacterPath, 'marioFail.png')),
                'LEFT': pygame.image.load(os.path.join(marioCharacterPath, 'marioFail.png')) 
                }
}

class marioCharacter():
    def __init__(self):
        self.path = marioPaths
        self.w = 68
        self.h = 108
        self.__state = 'standing'
        self.__direction = 'RIGHT'
        self.__surface = None
        self.rect = self.makeRect()
        
    
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, setState):
        self.__state = setState

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, setDirection):
        self.__direction = setDirection

    @property
    def surface(self):
        self.__surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        image = self.path[self.state][self.direction]
        imgRect = image.get_rect()
        imgRect.center = (self.w/2, self.h/2)
        self.__surface.blit(image, imgRect)
        return self.__surface
    
    def makeRect(self):
        return self.surface.get_rect()

Mario = marioCharacter()

goombaCharacterPath = os.path.join(characterPath, 'goomba')
goombaPaths = {
    'walking': {
                'RIGHT': pygame.image.load(os.path.join(goombaCharacterPath, 'goombaWalkingRight.png')),
                'LEFT' : pygame.image.load(os.path.join(goombaCharacterPath, 'goombaWalkingLeft.png')),
                }
}

class enemyCharacter(marioCharacter):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.state = 'walking'
        self.w = 64
        self.h = 64

Goomba = enemyCharacter(goombaPaths)


musicPath = r'C:\Come On Python Games\resources\marioHangman\music'

music = {
    'world1' : os.path.join(musicPath, 'over1.ogg'),
    'world2' : os.path.join(musicPath, 'over2.ogg'),
    'cave' : os.path.join(musicPath, 'under.ogg')
}

fort = os.path.join(musicPath, 'fortress.ogg')

loseSound = os.path.join(musicPath, 'fail.ogg')
winSound = os.path.join(musicPath, 'success.ogg')