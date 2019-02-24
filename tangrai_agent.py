# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 12:27:38 2019

@author: cpreg
"""

#EXECUTE ENVIRONMENT

import random
import gym
import numpy as np
from collections import deque

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
 
class DQNAgent():
    def __init__(self, env_id, path, episodes, max_env_steps, win_threshold, epsilon_decay,
                 state_size=None, action_size=None, epsilon=1.0, epsilon_min=0.01, 
                 gamma=1, alpha=.01, alpha_decay=.01, batch_size=16, prints=False):
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
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.batch_size = batch_size
        self.path = path                     #location where the model is saved to
        self.prints = prints                 #if true, the agent will print his scores
 
        self.model = self.NN_model()
        


def NN_model(self):
    model = Sequential()
    model.add(Dense(24, input_dim=self.state_size, activation='tanh'))
    model.add(Dense(48, activation='tanh'))
    model.add(Dense(self.action_size, activation='linear'))
    model.compile(loss='mse',
                  optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))
    return model

def act(self, state):
    if(np.random.random() <= self.epsilon):
        return self.env.action_space.sample()
    return np.argmax(self.model.predict(state))

def remember(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done))
    
def replay(self, batch_size):
    x_batch, y_batch = [], []
    minibatch = random.sample(
        self.memory, min(len(self.memory), batch_size))
    for state, action, reward, next_state, done in minibatch:
        y_target = self.model.predict(state)
        y_target[0][action] = reward if done else reward + self.gamma * np.max(self.model.predict(next_state)[0])
        x_batch.append(state[0])
        y_batch.append(y_target[0])
        
    self.model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)
    if self.epsilon > self.epsilon_min:
        self.epsilon *= self.epsilon_decay
        
        