#EXECUTE ENVIRONMENT

import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import keras
import time
import matplotlib.pyplot as plt
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tangrai import __init__
        

class App():
    def __init__(self,root,board):
        self.board=board
        self.newState(root,board)
    def newState(self,root,board):
        self.board=board
        frame = tkinter.Frame(root)
        
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.clear()
        img=ax.imshow(board)
        img.set_cmap('hot')
        ax.axis('off')
        self.canvas = FigureCanvasTkAgg(fig,master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()
        
#board=np.ones((10,10))
#board2=np.random.rand(10,10)
#
#root = tkinter.Tk()
#app = App(board2)
#app.newState(board)
#app.newState(board2)
#root.mainloop()      

class DQNAgent():
    def __init__(self, env_id, path, episodes, max_env_steps, win_threshold, epsilon_decay,
                 state_size=None, action_size=None, epsilon=1.0, epsilon_min=0.01, 
                 gamma=1.0, learning_rate=.001, alpha_decay=.01, batch_size=16, prints=False):
        self.memory = deque(maxlen=100000)
        self.env = gym.make(env_id)
        if state_size is None: 
            self.state_size = self.env.observation_space.n 
        else: 
            self.state_size = state_size
 
        if action_size is None: 
            self.action_size = self.env.action_space.n 
        else: 
            self.action_size = action_size
 
        self.episodes = episodes
        self.env._max_episode_steps = max_env_steps
        self.win_threshold = win_threshold
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.alpha_decay = alpha_decay
        self.batch_size = batch_size
        self.path = path                     #location where the model is saved to
        self.prints = prints                 #if true, the agent will print his scores
        self.learning_rate=learning_rate
        self.model = self.NN_model()        
        
    def NN_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(48, activation='relu'))
        model.add(Dense(self.action_size, activation='relu'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate, decay=self.alpha_decay),metrics=['mse'])
        return model
    
    def act(self, state):
        if(np.random.random() <= self.epsilon):
#            print('Random')
            return self.env.action_space.sample()
        
        state =  state.flatten()
        state=np.reshape(state,(1,100))   
#        print(self.model.predict(state)) #Q-Table!!!!
#        print('Q-Table')
        return np.argmax(self.model.predict(state))
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size)) #select random samples in batchsize
        for state, action, reward, next_state, done in minibatch:
            state =  state.flatten()
            state=np.reshape(state,(1,100))
            
            next_state =  next_state.flatten()
            next_state=np.reshape(next_state,(1,100))
            
#            print('Next state',next_state)
            y_target = self.model.predict(state)
            y_target[0][action] = reward if done else reward + self.gamma * np.max(self.model.predict(next_state)[0])
            x_batch.append(state[0])#
#            print(y_target[0])
            y_batch.append(y_target[0])
            
        history=self.model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch),verbose=0)
        print('MSE:',history.history['mean_squared_error'])
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
                
    def train(self):
#        state_space=self.env.observation_space.n
        #root = tkinter.Tk()
        scores=[]
        for episode in range(self.episodes):
            state=self.env.reset()
#            app = App(root,state)
            done=False
            counter_steps=0
            score=0
            print('### New episode ###')
            rewards=[]
            for _ in range (self.env._max_episode_steps):
                action_space=self.act(state)
                
                next_state, reward, done,_ = self.env.step(action_space)
                
                self.remember(state, action_space, reward, next_state, done)

                self.replay(self.batch_size) #Only train
                
                # Add up the score               
                score += reward
#                print('State',state)
#                print('NextState',next_state)
                rewards=np.append(rewards,reward)
                state = next_state
                #app.newState(root,state)

                plt.imshow(state)
                plt.show()
                
                print('Reward',reward)
                print('Score',score)
                
                if counter_steps==6:
                    done=True 
#                    print('All rewards',rewards)
                    scores=np.append(scores,score)
#                    self.remember(state, action_space, reward, next_state, done)
#                    self.replay(self.batch_size)
                    Gt=0
                    for score_i in scores: 
                        Gt+=self.gamma**counter_steps*score_i
                    next_score=max(scores)+self.learning_rate*(Gt-max(scores))
                    break                
                else:
                    done=False
                    
                counter_steps +=1   
        #root.mainloop()              
        self.model.save_weights('model/model_RL.h5')



if __name__ == "__main__":           
    agent= DQNAgent(env_id='TangrAI-v0', 
                    path='model/', 
                    episodes=50000, 
                    max_env_steps=7, 
                    win_threshold=None, 
                    epsilon_decay=1,
                    state_size=None, 
                    action_size=None, 
                    epsilon=0.6, 
                    epsilon_min=0.01, 
                    gamma=0.8, 
                    learning_rate=.001, 
                    alpha_decay=.01, 
                    batch_size=4, 
                    prints=True)
               
    
    agent.train()




#root = tkinter.Tk()
#app = App(root,board)

