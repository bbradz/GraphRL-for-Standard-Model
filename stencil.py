import torch
import torch.nn as nn
import torch.optim as optim
import networkx as nx
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.envs import DummyVecEnv
from stable_baselines3.common.env_checker import check_env
from gym import Env
from gym.spaces import Box
from random import uniform

# Step 1: Define the Graph Environment
# ==================================== #
class BSMGraphEnv(Env):
    def __init__(self):
        super(BSMGraphEnv, self).__init__()
        # Action space: continuous range of how much to change each tunable parameter by
        self.action_space = Box(low=-1, high=1, shape=(6,), dtype=np.float32)
        # Observation space: current parameter values
        self.observation_space = Box(low=-5, high=5, shape=(6,), dtype=np.float32)
        
        # Initialize parameters and graph
        # Q: Do we have reasonable initial vals here?
        self.m1 = 1.0  # initial vals
        self.m2 = 1.0
        self.v1 = 1.0
        self.v2 = 1.0
        self.y1 = 0.1
        self.y2 = 0.1
        self.graph = self.create_graph()

    def create_graph(self):
        # Graph representing BSM model to be inspired by (https://arxiv.org/pdf/2407.07203)
        G = nx.Graph()
        G.add_node("H1", type="Higgs", params={"m": self.m1, "v": self.v1, "y": self.y1})
        G.add_node("H2", type="Higgs", params={"m": self.m2, "v": self.v2, "y": self.y2})
        G.add_edge("H1", "H2", type="coupling")
        return G
    
    def reset(self):
        # Reset parameters to random values over range, not how we will do it in the end probably
        self.m1 = uniform(0.5, 2.0)
        self.m2 = uniform(0.5, 2.0)
        self.v1 = uniform(0.5, 2.0)
        self.v2 = uniform(0.5, 2.0)
        self.y1 = uniform(0.0, 0.2)
        self.y2 = uniform(0.0, 0.2)
        self.graph = self.create_graph()
        return np.array([self.m1, self.m2, self.v1, self.v2, self.y1, self.y2], dtype=np.float32)
    
    def step(self, action):
        # Update parameters based on action
        self.m1 += action[0]
        self.m2 += action[1]
        self.v1 += action[2]
        self.v2 += action[3]
        self.y1 += action[4]
        self.y2 += action[5]
        
        # Update graph with new parameters
        self.graph.nodes["H1"]["params"] = {"m": self.m1, "v": self.v1, "y": self.y1}
        self.graph.nodes["H2"]["params"] = {"m": self.m2, "v": self.v2, "y": self.y2}
        
        reward = self.calculate_alignment_reward()
        done = bool(abs(reward) < 0.01)  # Example termination condition or steps = max_steps
        obs = np.array([self.m1, self.m2, self.v1, self.v2, self.y1, self.y2], dtype=np.float32)

        return obs, reward, done, {}
    
    # Define reward calculation based on LHC data matching
    def calculate_lhc_reward(self):
        # Generate model's projected data based on current parameters
        projected_data = self.generate_projected_data()
        lhc_data = np.array([...]) # TODO how to load & parse

        #TODO Reproduciton rate
        
        # Calculate reward based on discrepancy between projected data and LHC data
        reward = -np.mean((projected_data - lhc_data) ** 2)
        
        return reward

    # Method to generate projected data based on current parameter values
    def generate_projected_data(self):
        #TODO
        projected_data = []
        return projected_data

# Step 2: Define and Train PPO Model
# ==================================== #
env = DummyVecEnv([lambda: BSMGraphEnv()])
check_env(env)

ppo_model = PPO("MlpPolicy", env, verbose=1) # Initialize PPO

print("Training PPO model...")
ppo_model.learn(total_timesteps=10000) # Train PPO model





# Step 3: Test the PPO agent
# ==================================== #
obs = env.reset()
for _ in range(10):
    action, _states = ppo_model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print(f"Obs: {obs}, Reward: {rewards}, Done: {dones}")








# Step 4: Compare with Random Search
# ==================================== #
def random_search(env, num_episodes=10):
    rewards = []
    for _ in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        while not done:
            action = env.action_space.sample()  # Random action
            obs, reward, done, _ = env.step(action)
            total_reward += reward
        rewards.append(total_reward)
    return rewards

# Run random search and calculate average reward
random_rewards = random_search(BSMGraphEnv())
ppo_rewards = [env.step(ppo_model.predict(env.reset())[0])[1] for _ in range(10)]

print(f"Average PPO Reward: {np.mean(ppo_rewards)}")
print(f"Average Random Search Reward: {np.mean(random_rewards)}")

