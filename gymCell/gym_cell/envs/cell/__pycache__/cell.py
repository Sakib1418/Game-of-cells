#writing down to import from variables
# editing version: final 

import random
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from math import pow
from enum import Enum
import math
# from pyprobs import Probability as pr
from gym_cell.envs.cell.helper import * 

from gym_cell.envs.cell.variables import *
from gym_cell.envs.cell import helper

class Direction(Enum): #dosage 
    RIGHT = 0
    LEFT = 1

class Bead:
    def __init__(self,position,colour):
        self.colour = WHITE
        self.position = position
        self.size = (TILESIZE-2)//2 

class Cell():
    def __init__(self,position,
        colour, size, regenerate_step, convert_time):

        self.colour = colour
        self.size = size
        self.regenerate_step = regenerate_step
        self.converted = False
        self.convert_time = convert_time
        self.dead = False
        self.potency = 0
        self.cell_step = 0
        self.tag = 0
        self.age = 0
        self.ancestors = []
        self.kids = []
        self.free_space = []
        self.position = position



    def move(self,access_dict,global_access_dict): #movement of cell, currently not affecting any RL decisions

        choice_ = random.choice(access_dict[tuple(self.position)]) #access dict gives available positions

        if (global_access_dict[tuple(choice_)] == 0) and (prob(move_prob)): #if the available positions are vacant move if probablity satisfies
            global_access_dict[tuple(self.position)] = 0
            self.position = choice_
            global_access_dict[tuple(self.position)] = 1
        else:
            pass

        self.cell_step += 1
        self.age += 1

        return self.position, global_access_dict




    def regenerate(self, cell__list,global_access_dict): #determines how regeneration will take place 
        
        rand = random.uniform(0,1)
        choice = random.choice(list(access_dict[tuple(self.position)]))

        a = (global_access_dict[tuple(choice)] == 0)
        b = (rand < regenerate_prob)
        c = (self.colour != RED)
        d = (self.regenerate_step <= self.cell_step <= max_age_regenerate)
        if self.potency > 0.05:
            e = prob(self.potency)


        if  a and b and c and d and e:
            # print("regenerated!!!!")
            new_cell = Cell(choice,
                color_potency_converted(self.colour,self.potency,assymmetric)[0], 
                self.size, 
                random.gauss(reg_mean, reg_std),
                random.gauss(conv_mean, conv_std),
            )
            global_access_dict[tuple(choice)] = 1

            new_cell.converted = color_potency_converted(self.colour,self.potency,assymmetric)[2] # daughter cell is the same color as the mother cell
            new_cell.potency = color_potency_converted(self.colour,self.potency,assymmetric)[1] # daughter cell have same potency as mother cell, atleast this is assumed now
            new_cell.cell_step = 0
            self.cell_step = 0
            self.regenerate_step = random.gauss(reg_mean, reg_std) #new regenerate time and convert time for parent cell
            self.convert_time = random.gauss(conv_mean, conv_std) #as each mother cell starts its new journey
            new_cell.tag = max([cell.tag for cell in cell__list])+1
            cell__list.append(new_cell)

        return cell__list, global_access_dict


    def convert(self,bead_position_dict): #calculates probablity of conversion 

        if (bead_position_dict[self.position] == 1) and (self.colour == RED) and (prob(convert_prob)):
            self.colour = BLUE
            self.converted = True
            self.potency = 1                    #after conversion potency becomes one
        return self.colour, self.converted


    def exhaust(self,bead_position_dict):      #how cells will be exhausted over time, should be some polynomial function of convert probablity

        if (bead_position_dict[self.position] == 1) and (self.colour != RED) and self.potency > least_potency:
            self.potency -=  (1/exhaustion_rate)
            self.colour = color_change(self.colour, self.potency)
        elif (self.colour != RED) and self.potency > least_potency:
            self.potency -= (natural_exhaustion/(max_step*multiplier*exhaustion_rate)) #exhaust anyway but with small amount

        return self.colour