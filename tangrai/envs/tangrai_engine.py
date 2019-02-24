import numpy as np
import random, time, pygame, sys
from pygame.locals import *

def getColors():
    #               R    G    B
#    white       = (255, 255, 255)
#    gray        = (185, 185, 185)
#    black       = (  0,   0,   0)
    red         = (155,   0,   0)
    lightred    = (175,  20,  20)
    green       = (  0, 155,   0)
    lightgreen  = ( 20, 175,  20)
    blue        = (  0,   0, 155)
    lightblue   = ( 20,  20, 175)
    yellow      = (155, 155,   0)
    lightyellow = (175, 175,  20)
    
    colors=(blue,green,red,yellow)
    lightcolors=(lightblue,lightgreen,lightred,lightyellow)
    
    assert len(colors) == len(lightcolors)
    
    return colors,lightcolors

colors,lightcolors= getColors()

bgColor = (0,0,0) #Black

FPS = 25
boxsize = 20
boardWidth = 20
boardHeigh = 20
windoWidth = boxsize * boardWidth
windowHeigh = boxsize * boardHeigh

A=[['OOOOOO....',
   'OOOOOO....',
   'OOOOO.....',
   'OOOO......',
   'OOO.......',
   'OO........',
   'O.........',
   '..........',
   '..........',
   '..........']]


B =[['..O.......',
    '.OO.......',
    'OOO.......',
    'OOO.......',
    'OO........',
    'O.........',
    '..........',
    '..........',
    '..........',
    '..........']]

C = [['....OO....',
     '...OOOO...',
     '..OOOOOO..',
     '.OOOOOOOO.',
     'OOOOOOOOOO',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']]

D = [['O.........',
     'OO........',
     'OO........',
     'O.........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']]

E = [['.O........',
     'OOO.......',
     '.O........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']]

F = [['OOOO......',
     '.OO.......',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........',
     '..........']]

G = [['....O.....',
     '...OO.....',
     '..OOO.....',
     '.OOOO.....',
     'OOOOO.....',
     '.OOOO.....',
     '..OOO.....',
     '...OO.....',
     '....O.....',
     '..........']]

board=np.ones((10,10))

boardWidth=10
boardHeigh=10
templeteWidth=10
templeteHeigh=10

blank='.'
full='O'

pieces = {'A': A,
          'B': B,
          'C': C,
          'D': D,
          'E': E,
          'F': F,
          'G': G}


shape='A'
rotation=0
color=0

x_Position=6
y_Position=2

class GameState:
    global FPSclock, displayWindow, basicFont, bigFont
    def __init__(self):
#        pygame.init()
#        FPSclock=pygame.time.Clock()  
#        displayWindow = pygame.display.set_mode((windoWidth, windowHeigh))      
#        basicFont = pygame.font.Font('freesansbold.ttf', 18)
#        bigFont = pygame.font.Font('freesansbold.ttf', 100)
#        pygame.display.iconify()
#        pygame.display.set_caption('TangrAI') 
        
        self.board = self.getBlankBoard()
        self.currentPiece = self.getNewPiece()
        self.nextPiece = self.getNewPiece()

#        pygame.display.update()
        
    def reinit(self):
        self.board = self.getBlankBoard()
        self.currentPiece = self.getNewPiece()
        self.nextPiece = self.getNewPiece()

#        pygame.display.update()
        
    def getActionSet(self):
        return range(4)    
    
    def getReward(self):
        self.counter_ones=0
        for row in self.board:
            for value in row:
                if value==1:
                    self.counter_ones+=1
        return self.counter_ones
    
    def isGameOver(self):
        return self.currentPiece == None and not self.isValidPosition()   
    
    def getNewPiece(self):
        # return a random new piece in a random rotation and color
        shape = random.choice(list(pieces.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(pieces[shape]) - 1),
                    'x': int(boardWidth / 2) - int(templeteWidth / 2),
                    'y': 0, # start it above the self.board (i.e. less than 0)
                    'color': random.randint(0, len(colors)-1)}
        return newPiece
    
    def addToBoard(self):
        isOnBoard=True
        global original_board
        for row in range(templeteWidth):
            for column in range(templeteHeigh):
                if pieces[self.currentPiece['shape']][self.currentPiece['rotation']][row][column]!=blank:
                    try:
                        self.board[row+self.currentPiece['x']][column+self.currentPiece['y']]=self.currentPiece['color']
                    except:
                        isOnBoard=False
                        
        return isOnBoard
     
    def getBlankBoard(self):
        self.board = []
        for i in range(boardWidth):
            self.board=np.append(self.board,[blank] * boardWidth)
        self.board=np.reshape(self.board,(boardWidth,boardHeigh))
        return self.board
    
    def isOnBoard(self,x,y):
        return x >= 0 and x < boardWidth and y < boardHeigh

    def piecetoMatrix(self):
        self.piece_array=[]
        for column in range(templeteHeigh):
            print(pieces[self.currentPiece['shape']][self.currentPiece['rotation']][column])
            for value in pieces[self.currentPiece['shape']][self.currentPiece['rotation']][column]:
                if value ==blank:
                    self.piece_array=np.append(self.piece_array,1)
                else:
                    self.piece_array=np.append(self.piece_array,self.currentPiece['color'])
                    
        self.piece_array=np.reshape(self.piece_array,(templeteWidth,templeteHeigh))
        return self.piece_array
    
    def isValidPosition(self):
        valid = True
        peca_nova= piecetoMatrix()
        for row in range(len(pieces[self.currentPiece['shape']][self.currentPiece['rotation']][0])):
                for column in range(len(pieces[self.currentPiece['shape']][self.currentPiece['rotation']][0])):
                    if peca_nova[row][column] == self.currentPiece['color']:
                        if self.currentPiece['x']+row > 4 or self.currentPiece['y']+column > 4:
                            valid = False
                        else:
                            if valid:
                                if self.board[self.currentPiece['x']+row][self.currentPiece['y']+column]==1:
                                    valid = True
                                else:
                                    valid = False    
        return valid           
    
    def convertToStrBoard(self):
        self.new_board=[]
        for row in range(templeteWidth):
            for column in range(templeteHeigh):
                if board[row,column]==1:
                    self.new_board=np.append(self.new_board,blank)
                else:
                    self.new_board=np.append(self.new_board,full)
                    
        self.new_board=np.reshape(self.new_board,(templeteWidth,templeteHeigh))
        return self.new_board           


