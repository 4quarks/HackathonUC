
# Modified from Tetromino by lusob luis@sobrecueva.com
# http://lusob.com
# Released under a "Simplified BSD" license

import random, time, pygame, sys
from pygame.locals import *


##               R    G    B
#WHITE       = (255, 255, 255)
#GRAY        = (185, 185, 185)
#BLACK       = (  0,   0,   0)
#RED         = (155,   0,   0)
#LIGHTRED    = (175,  20,  20)
#GREEN       = (  0, 155,   0)
#LIGHTGREEN  = ( 20, 175,  20)
#BLUE        = (  0,   0, 155)
#LIGHTBLUE   = ( 20,  20, 175)
#YELLOW      = (155, 155,   0)
#LIGHTYELLOW = (175, 175,  20)



A=['OOOOOO....',
   'OOOOOO....',
   'OOOOO.....',
   'OOOO......',
   'OOO.......',
   'OO........',
   'O.........',
   '..........',
   '..........',
   '..........']

B =['..O.......',
    '.OO.......',
    'OOO.......',
    'OOO.......',
    'OO........',
    'O.........',
    '..........',
    '..........',
    '..........',
    '..........']

C = ['....OO....',
     '...OOOO...',
     '..OOOOOO..',
     '.OOOOOOOO.',
     'OOOOOOOOOO',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']

D = ['O.........',
     'OO........',
     'OO........',
     'O.........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']

E = ['.O........',
     'OOO.......',
     '.O........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']

F = ['OOOO......',
     '.OO.......',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']

G = ['....O.....',
     '...OO.....',
     '..OOO.....',
     '.OOOO.....',
     'OOOOO.....',
     '.OOOO.....',
     '..OOO.....',
     '...OO.....',
     '....O.....',
     '..........']



import numpy as np
Q=np.ones((10,10))
x=0
y=0
LLETRA  = F
for row in range(len(LLETRA[0])):
    for column in range(len(LLETRA[0])):
        if LLETRA[row][column]!='.':
            try:
                Q[row+x][column+y]=6
            except:
                print('NO!')