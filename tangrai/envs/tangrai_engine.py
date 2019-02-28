import numpy as np
import random, time, pygame, sys
from pygame.locals import *


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

colors={'A': 1,
          'B': 2,
          'C': 3,
          'D': 4,
          'E': 5,
          'F': 6,
          'G': 7}

class GameState:
    global FPSclock, displayWindow, basicFont, bigFont
    def __init__(self):
       
        self.board = self.getBlankBoard()
        self.currentPiece = None

        self.str_board=[]
        self.step=0
    def reinit(self):
        self.board = self.getBlankBoard()
        self.currentPiece = None
        
    def getActionSet(self):
        return range(100)    
    
    def getReward(self,valid=True):
        counter_ones=0
        for row in self.int_board:
            for value in row:
                if value!=8:
                    counter_ones+=1
        if valid:
            reward=counter_ones**2/100
        else:
            reward=counter_ones**2/100*0.01
        return reward
    
    def isGameOver(self):
        return self.currentPiece == None and not self.isValidPosition()   
    
    def getNewPiece(self,shape):
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(pieces[shape]) - 1),
                    'x': random.randint(0, len(pieces[shape][0][0]) - 1),
                    'y': random.randint(0, len(pieces[shape][0][0]) - 1), # start it above the self.board (i.e. less than 0)
                    'color': colors[shape]}
        return newPiece

#    def econstructBoard(self,prediction):
#        positions=[]
#        for row in prediction:
#            if len(str(row))==1:
#                x=0
#                y=row
#            else:
#                x=row[0]
#                y=row[1]
#            positions=np.append(positions,[x,y])
#        return positions
    
#   positions=self.econstructBoard(prediction)  
#   for num_pos,position in enumerate(positions):
#        addToBoard(pieces[num_pos],random=False,position[0],position[1])
#        self.convertToIntBoard()
#        board=self.int_board  
#        
#   next_state=self.int_board 
#    
#    
#    
    def predictedPiece(self,shape,x,y):
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(pieces[shape]) - 1),
                    'x': int(x),
                    'y': int(y), # start it above the self.board (i.e. less than 0)
                    'color': colors[shape]}
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
                                if self.int_board[self.currentPiece['x']+row][self.currentPiece['y']+column]==8:
                                    valid = True
                                else:
                                    valid = False   
#        print(self.currentPiece['shape'])
#        print(self.currentPiece['rotation'])
#        print(self.currentPiece['x'])
#        print(self.currentPiece['y'])
#        print('Valid position to insert? ',valid)
        return valid     
    
    def addToBoard(self,shape,random=True):
        if random:
            self.currentPiece = self.getNewPiece(shape)
        if self.isValidPosition()==True:
            for row in range(templeteWidth):
                for column in range(templeteHeigh):
                    if pieces[self.currentPiece['shape']][self.currentPiece['rotation']][row][column]!=blank:
                        try:
                            self.board[row+self.currentPiece['x']][column+self.currentPiece['y']]=self.currentPiece['color']
                        except:
                            pass
            return self.getReward()
        else:
            return self.getReward(valid=False)     

    def addToBlankBoard(self,shape):
        board=self.getBlankBoard()
        for row in range(templeteWidth):
            for column in range(templeteHeigh):
                if pieces[self.currentPiece['shape']][self.currentPiece['rotation']][row][column]!=blank:
                    try:
                        board[row+self.currentPiece['x']][column+self.currentPiece['y']]=self.currentPiece['color']
                    except:
                        pass
        return board
                
    def getBlankBoard(self):
        self.board = []
        for i in range(boardWidth):
            self.board=np.append(self.board,[blank] * boardWidth)
        self.board=np.reshape(self.board,(boardWidth,boardHeigh))
        return self.board
    
    def isOnBoard(self,x,y):
        return x >= 0 and x < boardWidth and y < boardHeigh

#    def piecetoMatrix(self):
#        self.piece_array=[]
#        for column in range(templeteHeigh):
#            for value in pieces[self.currentPiece['shape']][self.currentPiece['rotation']][column]:
#                if value ==blank:
#                    self.piece_array=np.append(self.piece_array,1)
#                else:
#                    self.piece_array=np.append(self.piece_array,self.currentPiece['color'])
#                    
#        self.piece_array=np.reshape(self.piece_array,(templeteWidth,templeteHeigh))
#        return self.piece_array         
    
#    def convertToStrBoard(self):
#        self.str_board=[]
#        for row in range(templeteWidth):
#            for column in range(templeteHeigh):
#                if self.board[row,column]==blank:
#                    self.str_board=np.append(self.str_board,blank)
#                else:
#                    self.str_board=np.append(self.str_board,full)
#                    
#        self.str_board=np.reshape(self.str_board,(templeteWidth,templeteHeigh))
#        return self.str_board     
      
    def convertToIntBoard(self):
        self.int_board=[]
        for row in range(templeteWidth):
            for column in range(templeteHeigh):
                if self.board[row,column]==blank:
                    self.int_board=np.append(self.int_board,int(8))
                else:
                    self.int_board=np.append(self.int_board,int(self.board[row,column]))
                    
        self.int_board=np.reshape(self.int_board,(templeteWidth,templeteHeigh))
        return self.int_board  
    
    def frame_step(self,action):
        done=False
        if action==100:
            self.step=0
            board=self.getBlankBoard()
            self.convertToIntBoard()
            board=self.int_board
            done=True
            reward=None
#        elif action==6:
#            self.addToBoard(list(pieces)[action])
#            self.convertToIntBoard()
#            board=self.int_board
#            done=True
#            self.XY_positions=np.reshape(self.XY_positions,(int(len(self.XY_positions)/2),2))
#            
#            for num_row,row in enumerate(self.XY_positions):
#                value=''.join([str(int(row[0])),str(int(row[1]))])
#                self.joinXY=np.append(self.joinXY,int(value))
#                
#            positions= self.joinXY 
#            self.joinXY=[]    
#            self.XY_positions=[]
#            
        else:
#            print('ACTION!!!',action)
            if len(str(action))==1:
                x=0
                y=str(action)[0]            
            else:
                x=str(action)[0]
                y=str(action)[1]
#            print(self.board)
            self.currentPiece = self.predictedPiece(list(pieces)[self.step],x,y)
            
            reward=self.addToBoard(list(pieces)[self.step],random=False)
            self.convertToIntBoard()
            board=self.int_board
#            valid=self.isValidPosition()
#            print(valid)
#            if valid:
#                reward=self.getReward()
#                board=self.addToBlankBoard(list(pieces)[self.step])
#                self.convertToIntBoard()
#                board=self.int_board
#            else:
#                reward=self.getReward(valid=False)
#                board=self.getBlankBoard()
#                self.convertToIntBoard()
#                board=self.int_board
                
            self.step+=1
#            print('Board',board)
        return board, reward, done

#if __name__ == "__main__":
#    print('inici')
#    gamestate =  GameState()
#    gamestate.frame_step(1)
#    print(gamestate.getReward())