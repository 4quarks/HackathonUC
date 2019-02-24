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
        self.currentPiece = None
#        pygame.display.update()
        self.str_board=[]
    def reinit(self):
        self.board = self.getBlankBoard()
        self.currentPiece = None
#        pygame.display.update()
        
    def getActionSet(self):
        return range(8)    
    
    def getReward(self):
        counter_ones=0
        for row in self.str_board:
            for value in row:
                if value==blank:
                    counter_ones+=1
        return counter_ones
    
    def isGameOver(self):
        return self.currentPiece == None and not self.isValidPosition()   
    
    def getNewPiece(self,shape):
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(pieces[shape]) - 1),
                    'x': random.randint(0, len(pieces[shape][0][0]) - 1),
                    'y': random.randint(0, len(pieces[shape][0][0]) - 1), # start it above the self.board (i.e. less than 0)
                    'color': random.randint(0, len(colors)-1)}
        return newPiece
    
    def isValidPosition(self):
        valid = True
        
        for row in range(templeteWidth):
                for column in range(templeteHeigh):
                    if pieces[self.currentPiece['shape']][self.currentPiece['rotation']][row][column] == full:
                        if self.currentPiece['x']+row > templeteWidth-1 or self.currentPiece['y']+column > templeteHeigh-1:
                            valid = False
                        else:
                            if valid:
                                if self.board[self.currentPiece['x']+row][self.currentPiece['y']+column]==blank:
                                    valid = True
                                else:
                                    valid = False   
        print('Valid position to insert? ',valid)
        return valid     
    
    def addToBoard(self,shape):
        self.currentPiece = self.getNewPiece(shape)
        print('Current Piece',self.currentPiece)
        if self.isValidPosition()==True:
            for row in range(templeteWidth):
                for column in range(templeteHeigh):
                    if pieces[self.currentPiece['shape']][self.currentPiece['rotation']][row][column]!=blank:
                        try:
                            self.board[row+self.currentPiece['x']][column+self.currentPiece['y']]=self.currentPiece['color']
                        except:
                            pass
            print(self.board)
     
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
    
    def convertToStrBoard(self):
        self.str_board=[]
        for row in range(templeteWidth):
            for column in range(templeteHeigh):
                if self.board[row,column]==blank:
                    self.str_board=np.append(self.str_board,blank)
                else:
                    self.str_board=np.append(self.str_board,full)
                    
        self.str_board=np.reshape(self.str_board,(templeteWidth,templeteHeigh))
        return self.str_board           

    def frame_step(self,action):
        done=False
        if action==7:
            board=self.getBlankBoard()
            done=True
        else:
            self.addToBoard(list(pieces)[action])
            self.convertToStrBoard()
            board=self.str_board
        
        reward=self.getReward()
        
        
        return board, reward, done

#if __name__ == "__main__":
#    print('inici')
#    gamestate =  GameState()
#    gamestate.frame_step()
#    print(gamestate.convertToStrBoard())
#    print(gamestate.getReward())