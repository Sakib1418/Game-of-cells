from gym_cell.envs.cell.helper import access_dict_maker
import math
#################################################################################

        ###########               display variables    ########################

##################################################################################

TILESIZE = 8
GRIDNUM = 50
WIDTH = TILESIZE*GRIDNUM
HEIGHT = TILESIZE*GRIDNUM
BLUE = (30,30,250)
RED = (250,30,30)
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGREY = (20, 20, 20)
LIGHTGREY = (40, 40, 40)
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE
FPS = 1
attached_size = (TILESIZE-1)/2

#################    game variables  ###########################

bead_to_start_with = 0
exploration_step = 100
max_cell = math.pow(GRIDNUM,2)/2#total number of cell that can be accomodated
position_points = [(1,1),(GRIDNUM,GRIDNUM)]
access_dict, Grid_list = access_dict_maker(GRIDNUM)

#initially 20 and 80
max_step = 50 #time through which the game will be played
multiplier = 32
total_step = max_step*multiplier
bead_drop = 10
seeding = int(20)


#1 for add 0 for remove 2 for skip

# optimum action 
# manual_dosing = [1,1,2,2,1,0,2,2,2,2,1,2,2,2,0,2,2,1,2,2,2,1,2,2]

#sub optimum
# manual_dosing = [1,2,1,2,1,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2]

########  cell variables #################

conv_mean = 2#mean age every cell needs to have to convert, unit second 
conv_std = 0#standard deviation of the 
reg_mean = total_step*.35 #mean time where every cell will regenerate, unit second 
reg_std = 0#standard deviation of the regeneration time 
max_age_regenerate = total_step*.5 

upper_cut_potency = 0.8 #potency value above which a cell is  considered for calculating average potency


# Cell 1 - base case
convert_prob,natural_exhaustion,regenerate_prob,exhaustion_rate,assymmetric=0.9,1,.001,25,False

# Cell 2 - ex100_conv45
# convert_prob,natural_exhaustion,regenerate_prob,exhaustion_rate,assymmetric=0.45,1,.001,100,False

# Cell 3 - natex10regen.05
# convert_prob,natural_exhaustion,regenerate_prob,exhaustion_rate,assymmetric=0.9,10,.05,25,False


# Cell 4 - asymmetric
# convert_prob,natural_exhaustion,regenerate_prob,exhaustion_rate,assymmetric=0.9,10,.05,25,True


least_potency = 0.05

move_prob = 0.5
exhaust_potency = .2 #under which something is considered exhausted

factor = (20/max_step)

def reward_func(past_avg_potency,present_avg_potency,game_steps,sum_):

        if past_avg_potency > 0:
                ratio = present_avg_potency/past_avg_potency
        else:
                ratio = .01 

        if (game_steps >= (max_step-1) and sum_ >= 8):
                reward = 10*sum_
        elif ratio >= .90:
                reward = 5*factor
        elif .90 < ratio < .8:
                reward = 1*factor
        elif ratio < 0.5:
                reward = -5*factor
        else:
                reward = -1*factor

        return reward, ratio



            
