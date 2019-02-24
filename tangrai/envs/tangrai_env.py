import gym, numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
import tangrai_engine as game

screenHeight=480
screenWidth=480

class tangraiENV(gym.Env):
    def __init__(self):
        self.game_state = game.GameState()
        self._action_set = self.game_state.getActionSet()
        self.action_space = spaces.Discrete(len(self._action_set))
        
    def _step(self, a):
        self._action_set = np.zeros([len(self._action_set)])
        self._action_set[a] = 1
        reward = 0.0
        state, reward, terminal = self.game_state.frame_step(self._action_set)
        return state, reward, terminal, {}
    
    @property
    def _n_actions(self):
        return len(self._action_set)
    
    def _reset(self):
        do_nothing = np.zeros(len(self._action_set))
        do_nothing[0] = 1
        self.observation_space = spaces.Box(low=0, high=255, shape=(screenHeight, screenWidth, 3))
        state, _, _= self.game_state.frame_step(do_nothing)
        return state