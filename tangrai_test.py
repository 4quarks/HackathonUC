from keras.models import load_model
import matplotlib.pyplot as plt
from tangrai import __init__ as aaaaa

import gym
env = gym.make("TangrAI-v0")
observation = env.reset()
for _ in range(1000):
  action = env.action_space.sample() # your agent here (this takes random actions)
  observation, reward, done, info = env.step(action)