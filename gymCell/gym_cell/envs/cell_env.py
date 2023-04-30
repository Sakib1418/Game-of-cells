from enum import Enum
import time
import random
from typing import Optional, Union


################################################################################

#########################  Display purpose only ##############################

################################################################################





from gym_cell.envs.cell import variables
from gym_cell.envs.cell.variables import RED,attached_size, TILESIZE,GRIDNUM, max_cell, LIGHTGREY, DARKGREY
from gym_cell.envs.cell.variables import access_dict_maker, max_step, WIDTH, HEIGHT

import gym
# import pygame
from gym import spaces

from gym_cell.envs.cell.helper import *
# from gym_cell.envs.cell.helper import _get_obs
from gym_cell.envs.cell.cell import Cell, Bead

from gym_cell.envs.cell.variables import Grid_list
from gym_cell.envs.cell.variables import FPS


from gym import error, spaces, utils


class CellEnv(gym.Env):

    def __init__(self,render_mode: Optional[str] = None):



        self.max_cell = max_cell
        self.max_step = max_step
        self.bead_num = 0
        self.cell_number = variables.seeding
        self.game_steps = 0
        self.bead_num = 0
        self.score = 0
        self.game_steps = 0
        self.action = 0 #random.randint(-50,50)
        self.state=None


        self.total_cell_list = [Cell(
        drop_zone(self.cell_number, variables.position_points)[i],# random.choices(Grid_list, k = self.cell_number)[i],
        RED, 
        attached_size, 
        random.gauss(variables.reg_mean, variables.reg_std),
        random.gauss(variables.conv_mean,variables.conv_std)) for i in range(self.cell_number)]

        self.naive_cell= [redcell for redcell in self.total_cell_list if redcell.colour == variables.RED]
        self.activated_cell = [bluecell for bluecell in self.total_cell_list if bluecell.colour != RED]
        self.exhausted_cell = [yellowcell for yellowcell in self.activated_cell if (0 < yellowcell.potency <= variables.exhaust_potency)]

        self.low = np.array([0,0,0,0,0,0,0,0],dtype=np.float32)
        self.high = np.array([
            GRIDNUM,
            GRIDNUM,
            1,
            1,
            1,
            GRIDNUM,
            1,
            2
            ],dtype=np.float32)
        self.observation_space = spaces.Box(self.low, self.high, (8,),dtype=np.float32)

        self.action_space = spaces.Discrete(3)





    def reset(self):
 

        self.total_cell_list = [Cell(
        drop_zone(self.cell_number, variables.position_points)[i],# random.choices(Grid_list, k = self.cell_number)[i],
        RED, 
        attached_size, 
        random.gauss(variables.reg_mean, variables.reg_std),
        random.gauss(variables.conv_mean,variables.conv_std)) for i in range(self.cell_number)]

        tag = 0
        for cell in self.total_cell_list:
            tag += 1
            cell.tag = tag

        self.hist_act = []
        self.score_history = []
        self.dose_history = []
        self.census = []
        self.bead_num = 0
        position_list = [cell.position for cell in self.total_cell_list]

        points_bead = drop_zone(self.bead_num,[(1,1),(variables.GRIDNUM,variables.GRIDNUM)])

        self.beads = []
        
        self.global_access_dict = position_dict_maker(Grid_list,position_list)
        self.bead_position_dict = position_dict_maker(variables.Grid_list,[])

        points_bead = drop_zone(self.bead_num,[(1,1),(variables.GRIDNUM,variables.GRIDNUM)])

        for i in points_bead:

            new_bead = Bead(i,(0,0,0))
            self.beads.append(new_bead)
            self.bead_position_dict.update({i:1,})

        
        self.score = 0
        self.game_steps = 0
        self.free_space = []

        self.present_avg_potency = float(sum([cell.potency for cell in self.total_cell_list if (cell.potency > variables.upper_cut_potency and cell.colour != variables.RED)]))/len(self.total_cell_list)

        self.observation_space = self._get_obs()

        return self.observation_space

    def draw_text(self,text,font,text_col, x,y):
        img = font.render(text,True,text_col)
        self.game_display.blit(img,(x,y))



    def bead_dosing(self, bead_list, bead_access_dict):
        new_beadlist = bead_list.copy()
        new_bead_access_dict = bead_access_dict.copy()

        if self.action == 1:
            
            points_bead = drop_zone(variables.bead_drop,[(1,1),(variables.GRIDNUM,variables.GRIDNUM)])

            for i in points_bead:
                new_bead = Bead(i,(0,0,0))
                new_beadlist.append(new_bead)
                new_bead_access_dict.update({i:1,})

        elif self.action == 0:

            # beads_removed = new_beadlist
            # 
            new_beadlist = []   
            new_bead_access_dict = position_dict_maker(variables.Grid_list,[])
        elif self.action == 2:
            pass  
            # for i in beads_removed:
            #     if i in new_beadlist:
            #         new_beadlist.remove(i)
            #         new_bead_access_dict.update({i.position:0,})


        bead_list = new_beadlist
        bead_access_dict = new_bead_access_dict
        # print("after operation",len(new_beadlist))


        return bead_list, bead_access_dict



    def step(self, action):

        game_over = False
        self.action = action
        self.game_steps += 1


        self.score_history.append(self.score)
        self.dose_history.append(len(self.beads))
        self.census.append(len(self.total_cell_list))
        cell_list = self.total_cell_list.copy()

        
        self.past_avg_potency = float(sum([cell.potency for cell in self.total_cell_list if (cell.potency > variables.upper_cut_potency and cell.colour != variables.RED)]))/len(self.total_cell_list)

        self.beads, self.bead_position_dict = self.bead_dosing(
            self.beads,
            self.bead_position_dict)


        self.bead_num = len(self.beads)


        for i in range(variables.multiplier):
            for cell in cell_list:
                cell.position, self.global_access_dict = cell.move(variables.access_dict,self.global_access_dict)
                self.total_cell_list, self.global_access_dict = cell.regenerate(self.total_cell_list,self.global_access_dict)
                cell.colour = cell.exhaust(self.bead_position_dict)
                cell.colour, cell.converted = cell.convert(self.bead_position_dict)


            # if(int(i) % (variables.multiplier//FPS)) == 0:
            #     self._update_ui()
            #     self.clock.tick(FPS)

        self.observation_space = self._get_obs()

        self.naive_cell= [redcell for redcell in self.total_cell_list if redcell.colour == variables.RED]
        self.activated_cell = [bluecell for bluecell in self.total_cell_list if bluecell.colour != variables.RED]
        self.exhausted_cell = [yellowcell for yellowcell in self.activated_cell if (0 < yellowcell.potency <= .1)]

        sum_ = sum([cell.potency for cell in self.total_cell_list if (cell.potency > variables.upper_cut_potency and cell.colour != variables.RED)])

        self.present_avg_potency = float(sum([cell.potency for cell in self.activated_cell if (cell.potency > variables.upper_cut_potency and cell.colour != variables.RED)]))/len(self.total_cell_list)


        reward, ratio = variables.reward_func(self.past_avg_potency,self.present_avg_potency,self.game_steps,sum_)
       
 

        game_over = game_over_condition(self.total_cell_list,
            self.census, 
            variables.max_cell,
            self.score,
            self.naive_cell,
            self.activated_cell,
            self.game_steps,
            variables.max_step,
            False,
            )

        # print("present action: ", self.manual_action[self.game_steps], " ratio:",ratio,"  reward:", reward, " bead number:", self.bead_num, "sum potency: ", sum_ )

        return self.observation_space, reward, game_over, {}


    def _get_obs(self):

        naive = len(self.naive_cell)
        active = len(self.activated_cell)
        frac_naive = naive/(naive+active)
        frac_active = active/(naive+active)    
        s_core = self.present_avg_potency
        bead_num_ = self.bead_num
        step_covered = self.game_steps/max_step #reverse this 
        action_ = self.action

        wallahi = [naive,active,frac_naive,frac_active,s_core,bead_num_,step_covered,action_]
        list_ = np.array(wallahi, dtype=np.float32)




        return list_       