from stable_baselines3 import PPO, SAC, A2C, DDPG, DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor
import time
import subprocess
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
# subprocess.Popen('pip install -e .', shell=True)
import os
import pickle
import csv
import numpy as np
import gym
from gym.envs.registration import register


register(
    id='gym_cell/cg-v0',
    entry_point='gym_cell.envs:CellEnv',
    max_episode_steps=10000,
)

time.sleep(3)







log_dir = './cross_base_case'



eval_vec_env = gym.make('gym_cell/cg-v0')
eval_vec_env = Monitor(eval_vec_env,log_dir)



eval_callback = EvalCallback(eval_vec_env, best_model_save_path=log_dir,
                             log_path=log_dir, eval_freq=1000,
                             deterministic=True, render=False, verbose=0, n_eval_episodes=11)


case_name = './strategy_base_case_test'
# model = PPO.load(case_name+"/best_model.zip", env=eval_vec_env)


model = PPO("MultiInputPolicy", eval_vec_env, seed = 89, verbose=0, tensorboard_log=log_dir)
# model.learn(5e5, callback=[eval_callback], progress_bar=False)

# print("finished!!!!")
print(model.policy)