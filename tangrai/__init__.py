from gym.envs.registration import register

register(
    id='TangrAI-v0',
    entry_point='tangrai.envs:tangraiENV',
)


#import gym
#import tangrai
#env = gym.make('TangrAI-v0')