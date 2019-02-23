import gym
from gym import error, spaces, utils
from gym.utils import seeding


class tangraiENV(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    ...
  def step(self, action):
    ...
    #return observation, reward , done, additional info
  def reset(self):
    ...
  def render(self, mode='human', close=False):
    ...