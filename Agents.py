import Node
import random

def base_agent(game_grid):
    revealed_dict = {}
    currCell = game_grid[0][0]
    print(revealed_dict)
    unrevealed_lst = []
    for row in game_grid:
        for cell in row:
            unrevealed_lst.append(cell)


    while len(unrevealed_lst) != len(revealed_dict):
        base_agent_query(revealed_dict, currCell)
        base_agent_query(revealed_dict, currCell)
        for item in unrevealed_lst:
            if item in revealed_dict:
                unrevealed_lst.remove(item)
        if unrevealed_lst == []:
            break
        randCell = random.choice(unrevealed_lst)
        currCell = randCell



def base_agent_query(revealed_dict, cell):
    cell.set_clear()
    if cell.get_state() == Node.BOMB:
        revealed_dict[cell] = 1
    elif cell.get_state() == Node.CLEAR:
        revealed_dict[cell] = 0


    clue = cell.get_clue()
    neighbors = cell.get_neighbors()
    cleared_nei_lst = []
    hidden_nei_lst = []
    revealed_mine_lit = []
    for cell in neighbors:
        if cell in revealed_dict and revealed_dict[cell] == 0:
            cleared_nei_lst.append(cell)
    for cell in neighbors:
        if cell in revealed_dict and revealed_dict[cell] == 1:
                revealed_mine_lit.append(cell)
    for cell in neighbors:
        if cell not in revealed_dict:
            hidden_nei_lst.append(cell)
    #base checks given by document
    if clue == 0:
        for neighbor in neighbors: #mark all neighbors as clear
            neighbor.flag_as_clear()
            revealed_dict[neighbor] = 0
    elif clue == len(neighbors):
        for neighbor in neighbors: #mark all neighbors as bomb
            neighbor.flag_as_bomb()
            revealed_dict[neighbor] = 1

    elif (clue - len(revealed_mine_lit)) == len(hidden_nei_lst):
        for cell in hidden_nei_lst: #mark all neighbors as bomb
            cell.flag_as_bomb()
            revealed_dict[cell] = 1
    elif (len(neighbors) - clue) - len(cleared_nei_lst) == len(hidden_nei_lst):
        for cell in hidden_nei_lst: #mark all neighbors as bomb
            cell.flag_as_clear()
            revealed_dict[cell] = 0

