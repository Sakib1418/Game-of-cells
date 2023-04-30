from audioop import reverse
import matplotlib.pyplot as plt
from IPython import display
import random
import math
import numpy as np
from PIL import Image
from datetime import datetime
# from gymCell.gym_cell.envs.cell import variables
from gym import error, spaces, utils
# from .variables import RED,BLUE

plt.ion()

def plot_avg(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    # plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.tight_layout()


    name = 'images/fig' +'.jpg'

    plt.savefig(name, format = 'JPG')
    plt.pause(.001)


def disp_activator(u):

    plt.clf()    
    display.clear_output(wait=True)
    display.display(plt.gcf())  
    u = np.flipud(u)
    u = np.fliplr(u)
    u = np.transpose(u)
    u = np.fliplr(u)

    # im = plt.imshow(u.copy(), cmap=plt.get_cmap('jet'), vmin=275,vmax=300)
    # im = plt.imshow(u.copy(), cmap=plt.get_cmap('jet'), vmin=min(list(u.flatten())),vmax=max(list(u.flatten())))
    # im = plt.imshow(u.copy(), cmap=plt.get_cmap('jet'), vmin=0,vmax=max(list(u.flatten())))
    im = plt.imshow(u.copy(), cmap=plt.get_cmap('jet'), vmin=0,vmax=300)


    plt.xticks([i for i in range(len(u))],list([str(i+1) for i in range(len(u))]))
    plt.yticks([i for i in range(len(u))],list([str(len(u)-i) for i in range(len(u))]))
    plt.colorbar(im)
    # plt.close()
    plt.pause(.01)

def plot_mm(num_stat):

    positions = [str(i+1) for i in range(len(num_stat))]
    reds = np.array([i[0] for i in num_stat])
    blues = np.array([i[1] for i in num_stat])
    yellow = np.array([i[2] for i in num_stat])
    convert_factor = np.array([i[3] for i in num_stat])
    conv_dir = np.array([i[4] for i in num_stat])
  

    plt.clf()    
    display.clear_output(wait=True)
    display.display(plt.gcf()) 

    plt.ylim([-10,sum([i[-1] for i in [reds,blues,yellow]])+10])

    fig, ax = plt.subplots()
    y =  [-sum([max(i) for i in [reds,blues,yellow]])/10 for i in range(len(positions))]


    ax.bar(positions,reds,color = 'red', edgecolor="black", label = 'naive cells') 
    ax.bar(positions,blues, bottom = reds, color = 'blue', edgecolor="black", label = 'activated cellls')
    ax.bar(positions,yellow, bottom = blues+reds, color = 'yellow', edgecolor="black", label = 'exhausted cells')
    for xp, yp, m in zip(positions, y, conv_dir):
        if m == '^':
            ax.scatter(xp, yp, marker=m, s = 40, color = 'k')
        else:
            ax.scatter(xp, yp, marker=m, s = 4, color = 'w')   
    # ax.scatter(positions, [-sum([max(i) for i in [reds,blues,yellow]])/10 for i in range(len(positions))], marker = conv_dir)
    ax.set_ylabel('Number of cells --->')
    # ax.set_ylim([-10,sum([i[-1] for i in [reds,blues,yellow]])+10])


    ax2=ax.twinx()

    ax2.plot(positions, convert_factor, linewidth = 1, markersize = 2, marker = 'o')
    

    ax2.set_ylim([-.3,1.1])



    # ax.set_ylim([-10,0])


    ax.set_ylabel('convert factor')

    plt.legend()

    
    plt.xlabel('Game Steps --->')

    plt.title('Growth of cells')
    plt.tight_layout()
    # print(positions)
    # print(reds)
    # print(blues)

    plt.savefig('growth_chart.png', format = 'png')
    # print("num of cells: ",num_stat)
    plt.close()
    plt.pause(.01)
    # plt.clf()

def diffuse(u,u0):

    dx = dy = 1
    D = 1
    dx2, dy2 = dx*dx, dy*dy
    dt = dx2 * dy2 / (2 * D * (dx2 + dy2))
    
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
        (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
        + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )
    
    
    u0 = u.copy()

    return u0,u


def grid_maker(Grid_list, access_dict = {}):

    for block in Grid_list:
        access_list = []

        for i in list([block[0]-1,block[0],block[0]+1]):
            for j in list(([block[1]-1,block[1],block[1]+1])):
                if (i,j) in Grid_list:
                    if (i,j) != block:
                        access_list.append((i,j))

        access_list = tuple(access_list)
        access_dict.update({(block[0],block[1]):access_list})

    return access_dict



def color_change(initial_colour, potency):

    list_colour = list(initial_colour)
    num = (250-30)
    reduction = round(num*(1-potency),0)
    # print("potency is: ", potency)
    # print("reduction is: ", reduction )
    
    if 20 <= list_colour[0] <= 250:
        list_colour[0] = 30 + reduction
    else:
        list_colour[0] = list_colour[0]

    if 20 <= list_colour[1] <= 250:
        list_colour[1] = 30 + reduction
    else:
        list_colour[1] = list_colour[1]
    
    if 20 <= list_colour[2] <= 250: 
        list_colour[2] = 250 - reduction
    else:
        list_colour[2] = list_colour[2]

    final_colour = tuple(list_colour)
    # print("final color is: ", final_colour)

    return final_colour

def game_over_condition(
    n_total_cells,
    census,
    max_blob,
    score,
    red_cells_list,
    blue_cells_list,
    steps_passed,
    max_step,
    manual_quit):
    game_over = False
    if manual_quit:
        print('pressed quit')
        # print('current score: ', score)
        # print('number of red blob: ',len(red_cells_list))
        # print('number of blue blob: ',len(blue_cells_list))
        game_over = True

    if len(n_total_cells) > max_blob:
        print('Maximum blob reached :O ')
        # print('current score: ', score)
        # print('number of red blob: ',len(red_cells_list))
        # print('number of blue blob: ',len(blue_cells_list))
        game_over = True

    if len(n_total_cells) < 10 and steps_passed> max_step:
        print('Something messed up, never mind, probably I shut off reproduction')
        # print('current score: ', score)
        # print('number of red blob: ',len(red_cells_list))
        # print('number of blue blob: ',len(blue_cells_list))
        game_over = True

    if len(n_total_cells) <1:
        print('All blob died :( ')
        print('number of red blob: ',len(red_cells_list))
        print('number of blue blob: ',len(blue_cells_list))
        game_over = True

    if steps_passed >= max_step:
        # print('time out!!!')
        # print('score is: ', score)
        # print('number of red blob: ',len(red_cells_list))
        # print('number of blue blob: ',len(blue_cells_list))
        game_over = True
    # if len(red_cells_list) <= 0:
    #     print('all differentiated!!!')
    #     print('score is: ', score)
    #     print('number of red blob: ',len(red_cells_list))
    #     print('number of blue blob: ',len(blue_cells_list))
    #     game_over = True

    if (len(census) > max_step) and last_same(census,6):
        print("Growth finished")
        game_over = True



    return game_over


def calc_velocity(step_size,position,x_boundary,y_boundary):
    move_x = random.randrange(-step_size,step_size)
    move_y = random.randrange(-step_size,step_size)

    velocity = move_x, move_y

    if position[0] < 2*step_size:
        velocity = abs(move_x), move_y
        return velocity
    elif position[0] > x_boundary-2*step_size:
        velocity = -abs(move_x), move_y
        return velocity
    if position[1] < 2*step_size:
        velocity = move_x, abs(move_y)
        return velocity
    elif position[1] > y_boundary-2*step_size:
        velocity = move_x, -abs(move_y)
        return velocity
    else:
        velocity = move_x, move_y

        
    return velocity

def free_space_finder(position,access_dict,free_spaces):
    free_space_around = access_dict[position]
    for i in access_dict[position]:
        if i not in free_spaces:
            free_space_around.remove(i)
    return free_space_around

def gaussian(x,mean,std):
    inside_exp = -.5*math.pow(((x-mean)/std),2)

    y = (1/(std*math.sqrt(2*math.pi)))*(math.exp(inside_exp))
    return y

def get_numbers(game):
    red_num = len(game.naive_cell)
    blue_num = len(game.activated_cell)
    yellow_num = len(game.exhausted_cell)
    bead_num = game.bead_num
    conv_direction = game.hist_act
    return [red_num,blue_num-yellow_num, yellow_num, bead_num, conv_direction]


def diff_grid(gridnum):
    w = h = gridnum
    dx = dy = 1
    Thot = 300 
    nx, ny = int(w/dx), int(h/dy)
    u0 = Thot * np.ones((nx, ny))
    u = u0.copy()



    return u


def projection_grid(gridnum, cell_list, frame_number, bead_list):

    # plt.clf()    
    # display.clear_output(wait=True)
    # display.display(plt.gcf()) 

    projection = np.random.rand(gridnum,gridnum,3)*0   
    for cell in cell_list:
        # print("location: ", ((cell.position[0]),cell.position[1]))
        projection[(cell.position[1]-1),cell.position[0]-1,:] = list(cell.colour)

    for bead in bead_list:
        # print("location: ", ((cell.position[0]),cell.position[1]))
        projection[(bead.position[1]-1),bead.position[0]-1,:] = list(bead.colour)

    # u = Image.fromarray(projection.astype('uint8')).convert('RGBA')
    projection = projection.astype('uint8')
    projection = np.einsum('ijk->kij', projection)



    # u = np.flipud(u)
    # u = np.fliplr(u)
    # u = np.transpose(u)
    # u = np.fliplr(u)


    # u0 = u.copy()
    # print("shape of data: ",projection.shape, "type of data: ", type(projection))
    # img = Image.fromarray(projection, 'RGB')
    # name = str(frame_number)
    # print("frame number is: ", name)
    # plt.imshow(u0,origin='lower')
    # plt.title("frame number is: "+ str(frame_number))
    # location = 'images/'+name 
    # img.save(location)
    
    # np.save(location,projection)
    # plt.savefig(location)
    # plt.pause(.0000001)

    return projection



def projection_grid_grey(gridnum, cell_list, frame_number):

    plt.clf()    
    display.clear_output(wait=True)
    display.display(plt.gcf()) 

    projection = np.random.rand(gridnum,gridnum,1)*0   
    for cell in cell_list:
    #     print("location: ", ((cell.position[0]),cell.position[1]))
        projection[(cell.position[1]-1),cell.position[0]-1,:] = cell.potency
        
        # print("projection value at that cell: ",projection[(cell.position[1]-1),cell.position[0]-1])



    # u = Image.fromarray(projection.astype('uint8')).convert('RGBA')

    # u = np.flipud(u)
    # u = np.fliplr(u)
    # u = np.transpose(u)
    # u = np.fliplr(u)

    projection0 = projection.copy()
    # u0 = u.copy()
    # print("shape of data: ",projection.shape, "type of data: ", type(projection))
    # img = Image.fromarray(projection, 'RGB')
    plt.gray()
    name = str(frame_number)
    # print("frame number is: ", name)
    plt.imshow(projection0,origin='lower')
    location = 'images/'+name 
    # img.save(location)
    
    np.save(location,projection0)
    # plt.savefig(location)
    plt.pause(.1)


def access_dict_maker(gridnum):
    Grid_X = gridnum
    Grid_Y = gridnum
    Grid_list = []

    for i in range(1,Grid_X+1):
        for j in range(1,Grid_Y+1):
            Grid_list.append((i,j))

    access_dict = {}

    for block in Grid_list:
        access_list = []
        # print("block is: ",block)

        for i in list([block[0]-1,block[0],block[0]+1]):
            if i == 0:
                i = gridnum
            if i == gridnum+1:
                i = 1

            for j in list([block[1]-1,block[1],block[1]+1]):
                if j == 0:
                    j = gridnum
                if j == gridnum+1:
                    j = 1

                if (i,j) != block:
                    access_list.append((i,j))
                    # print("not matched: ", (i,j))

        access_list = tuple(access_list)
        access_dict.update({(block[0],block[1]):access_list})

    return access_dict, Grid_list

def grid_dose(grid,co_tuple, radius):

    r2 = radius
    x_co = co_tuple[0]
    y_co = co_tuple[1]
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            p2 = (i-x_co)**2 + (j-y_co)**2
            if p2 <= r2:
                grid[i,j] = grid[i,j] + 300

    return grid

def drop_zone(seeding_number, position_points):

    x_list = [i for i in range(position_points[0][0],position_points[1][0])]
    y_list = [i for i in range(position_points[0][1],position_points[1][1])]
    # print(x_list)
    # print(y_list)

    select_x = random.choices(x_list,k = int(seeding_number))
    select_y = random.choices(y_list,k = int(seeding_number))

    dropzone = []
    for i in range(len(select_x)):
        dropzone.append((select_x[i],select_y[i]))

    return dropzone


def dataframe_process(dataframe):
    columns_ = ['census','score_history', 'dose_history']#,'activator_history']
    for column in columns_:
        line_store = []
        for line in dataframe[column]:
            processed = [float(i) for i in line.strip('][').split(', ') if type(i) != float]
            line_store.append(processed)
        print(line_store)
        dataframe[column] = line_store
    return dataframe

def last_same(list_,same):
    decision = True
    common = list_[-same]
    for i in list_[-same:]:
        if common != i:
            decision = False
        else:
            common = i
    return decision

def position_dict_maker(Grid_list,positions):
    dict_ = {}
    # positions = [bead.position for bead in beads]
    for i in Grid_list.copy():
        if i in positions:
            # print("                                                  i found!!!!")
            dict_.update({i:1})
        else:
            dict_.update({i:0})
    # print(dict_)
    return dict_


def noise(naive, active, score, level):

    level_list = [[3,.5],
             [6,2],
             [8,4]]
    
    naive = naive + random.randint(-level_list[level][0],level_list[level][0])
    active = active + random.randint(-level_list[level][0],level_list[level][0])
    
    score = score + random.uniform(-level_list[level][1],level_list[level][1])

    if naive <= 0:
        naive = 0
    if active <= 0:
        active = 0
    if score <=0:
        score = 0



    return naive, active, score




def color_potency_converted(color,potency,assym=False):
    color = color 
    potency = potency
    if assym == False:
        # print('assym false')
        return list([color,potency,True])
    else:
        # print('this is assym')

        color = random.choice([(250,30,30),color])

        if color == (250,30,30):
            print('not converted!!')

            converted = False
        else:
            print('converted!!')
            converted = True


        return list([color,potency,converted])