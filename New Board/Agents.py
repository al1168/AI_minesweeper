import Node
import random
import time

def base_agent(game_grid):
    revealed_dict = dict()
    currCell = game_grid[0][0]
    cell_lst = []
    for row in game_grid:
        for cell in row:
            cell_lst.append(cell)

    '''
    base_agent_query(revealed_dict, currCell)
    cell_lst.remove(currCell)

    while len(cell_lst) != 0:
        randCell = random.choice(cell_lst)
        if randCell not in revealed_dict:
            cell_lst.remove(randCell)
            base_agent_query(revealed_dict, randCell)
            #print(len(revealed_dict))
            print(randCell)
            print(len(cell_lst))
            print(randCell.get_pos())

    '''
    base_agent_query(revealed_dict, currCell)
    step = 0
    for row in game_grid:
        for cell in row:
            if cell not in revealed_dict or revealed_dict[cell] == 0:
                step += 1
                base_agent_query(revealed_dict, cell)
                time.sleep(.3000)
                print(step)
                #print(cell.get_pos())

                #print("step count: "+str(step))
    #print(calc_score(game_grid, revealed_dict))

    #print("revealed dict")
    #print(revealed_dict)

def base_agent_query(revealed_dict, cell):
    if not cell.is_safe():
        cell.flag_as_bomb()
        revealed_dict[cell] = 1
    elif cell.is_safe():
        cell.flag_as_clear()
        revealed_dict[cell] = 0

    clue = cell.get_clue()
    neighbors = cell.get_neighbors()
    revealed_cleared_nei_lst = []
    hidden_nei_lst = []
    revealed_mine_nei_lst = []
    for c in neighbors:
        if c in revealed_dict:
            if revealed_dict[c] == 0:
                revealed_cleared_nei_lst.append(c)
            elif revealed_dict[c] == 1:
                revealed_mine_nei_lst.append(c)

        else:
            hidden_nei_lst.append(c)

    #base checks given by document
    if clue == 0:
        for neighbor in hidden_nei_lst: #mark all neighbors as clear
            neighbor.flag_as_clear()
            revealed_dict[neighbor] = 0
    elif clue == len(neighbors):
        for neighbor in hidden_nei_lst: #mark all neighbors as bomb
            neighbor.flag_as_bomb()
            revealed_dict[neighbor] = 1
    elif (clue - len(revealed_mine_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_bomb()
            revealed_dict[c] = 1
    elif ((len(neighbors) - clue) - len(revealed_cleared_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_clear()
            revealed_dict[c] = 0

    #print(neighbors)
    #print(revealed_cleared_nei_lst)
    #print(hidden_nei_lst)
    #print(revealed_mine_nei_lst)


def calc_score(grid, dict):

    total = len(dict)
    score = 0
    for row in grid:
        for cell in row:
            if cell.is_safe() and dict[cell] == 0:
                score += 1
            if not cell.is_safe() and dict[cell] == 1:
                score += 1
    return (score // total) * 100
