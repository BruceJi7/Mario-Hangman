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



