from gym.envs.registration import register

register(
    id='gym_cell/cg-v0',
    entry_point='gym_cell.envs:CellEnv',
)
