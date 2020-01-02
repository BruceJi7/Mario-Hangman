import pygame, sys, random, os
from pygame.locals import *
from string import ascii_uppercase, ascii_lowercase


backgroundPath = r'C:\Come On Python Games\resources\marioHangman\background\bkg.png'

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
                }
}
class marioCharacter():
    def __init__(self):
        self.path = marioPaths
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
    def directon(self, setDirection):
        self.__direction = setDirection

    @property
    def surface(self):
        w, h = 56, 108
        self.__surface = pygame.Surface((w, h), pygame.SRCALPHA)
        image = self.path[self.state][self.direction]
        imgRect = image.get_rect()
        imgRect.center = (w/2, h/2)
        self.__surface.blit(image, imgRect)
        return self.__surface
    
    def makeRect(self):
        return self.surface.get_rect()

Mario = marioCharacter()
