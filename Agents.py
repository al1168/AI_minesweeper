import Node
import random
import time

#  object to mirror constraint problems
class Equation:
    def __init__(self, list, value):
        self.list = list
        self.value = value

    def getValue(self):
        return self.value

    def getlist(self):
        return self.list

#  basic agent that randomly selects a cell to query
def base_agent(game_grid, draw):
    safe_cell_lst = []
    revealed_dict = {}
    explored = []
    hidden_cells = []
    unopened_list = []
    currCell = game_grid[0][0]
    print(revealed_dict)
    unrevealed_lst = []
    revealed_bombs = []
    original_bombs = []
    for row in game_grid:
        for cell in row:
            unrevealed_lst.append(cell)
            unopened_list.append(cell)
            if cell.get_state() == Node.BOMB:
                original_bombs.append(cell)

    print("Pre Loop")
    print(len(unrevealed_lst))
    step = 1
    basic_agent_query(revealed_dict, currCell, draw, unrevealed_lst, revealed_bombs, unopened_list)

    while len(unrevealed_lst) != 0:
        randCell = random.choice(unopened_list)
        if randCell not in revealed_dict:
            print("Query number: "+str(step))
            basic_agent_query(revealed_dict, randCell, draw, unrevealed_lst, revealed_bombs, unopened_list)
            step += 1
            #time.sleep(1.5)
    print("Post Loop")
    print(len(unrevealed_lst))

    print(calc_score(game_grid, revealed_dict))

    red_cell = 0
    for row in game_grid:
        for cell in row:
            if cell.get_state() == Node.BOMB:
                red_cell += 1
    print("Safely Marked: " + str(red_cell))
    print(len(unopened_list))

# basic query function for basic agent, similar to how it was described on document
# revealed dict: stores current knowledge/facts agent knows
# cell: queried cell
# unreavealed_list : cells that have not been flagged
# revealed bombs: track number of bombs reveals so far
def basic_agent_query(revealed_dict, cell, draw , unrevealed_list, revealed_bombs, unopened_list):
    if not cell.is_safe():
        cell.flag_as_stepped()
        revealed_dict[cell] = 1
        if cell in unopened_list:
            unopened_list.remove(cell)
        if cell in unrevealed_list:
            unrevealed_list.remove(cell)
            revealed_bombs.append(cell)
        print("Stepped on bomb")
        draw()
    elif cell.is_safe():
        cell.flag_as_clear()
        revealed_dict[cell] = 0
        if cell in unopened_list:
            unopened_list.remove(cell)
        if cell in unrevealed_list:
            unrevealed_list.remove(cell)
        draw()

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
            if neighbor in unrevealed_list:
                unrevealed_list.remove(neighbor)
            draw()
    elif clue == len(neighbors):
        for neighbor in hidden_nei_lst: #mark all neighbors as bomb
            neighbor.flag_as_bomb()
            revealed_dict[neighbor] = 1
            if neighbor in unrevealed_list:
                unrevealed_list.remove(neighbor)
                revealed_bombs.append(neighbor)
            if neighbor in unopened_list:
                unopened_list.remove(neighbor)
            draw()
    elif (clue - len(revealed_mine_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_bomb()
            revealed_dict[c] = 1
            if c in unrevealed_list:
                unrevealed_list.remove(c)
                revealed_bombs.append(c)
            if c in unopened_list:
                unopened_list.remove(c)
            draw()
    elif ((len(neighbors) - clue) - len(revealed_cleared_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_clear()
            revealed_dict[c] = 0
            if c in unrevealed_list:
                unrevealed_list.remove(c)
            draw()


# revealed dict: stores current knowledge/facts agent knows
# cell: queried cell
# revealed bombs: track number of bombs reveals so far
# safe_cell_lst: list of cells that are safe to query
# explored : list of queried cells
# hidden_cells:  list of unflagged cells

def base_agent_query(revealed_dict, cell, draw, revealed_bombs, safe_cell_lst, explored, hidden_cells):
    if cell.id in hidden_cells:
        hidden_cells.remove(cell.get_id())
    if cell.safe == False:
        printcell(cell)
        cell.flag_as_stepped()
        revealed_dict[cell] = 1
        revealed_bombs.append(cell)
        explored.add(cell.id)
    elif cell.safe == True:
        cell.flag_as_clear()
        revealed_dict[cell] = 0
        explored.add(cell.id)
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
    # base checks given by document
    if clue == 0:
        for neighbor in neighbors:  # mark all neighbors as clear
            neighbor.flag_as_clear()
            if neighbor.get_id() in hidden_cells:
                hidden_cells.remove(neighbor.get_id())
            revealed_dict[neighbor] = 0
            if neighbor not in safe_cell_lst and neighbor.get_id() not in explored:
                safe_cell_lst.append(neighbor)
            draw()
    elif clue == len(neighbors):
        for neighbor in neighbors:  # mark all neighbors as bomb
            neighbor.flag_as_bomb()
            if neighbor.get_id() in hidden_cells:

                hidden_cells.remove(neighbor.get_id())
            revealed_dict[neighbor] = 1
            draw()

    elif (clue - len(revealed_mine_lit)) == len(hidden_nei_lst):
        for cell in hidden_nei_lst:  # mark all neighbors as bomb
            cell.flag_as_bomb()
            if cell.get_id() in hidden_cells:

                hidden_cells.remove(cell.get_id())

            revealed_dict[cell] = 1
            draw()
    elif (len(neighbors) - clue) - len(cleared_nei_lst) == len(hidden_nei_lst):
        for cell in hidden_nei_lst:  # mark all neighbors as bomb
            cell.flag_as_clear()
            revealed_dict[cell] = 0
            if cell not in safe_cell_lst and cell.get_id() not in explored:
                safe_cell_lst.append(cell)
            if cell.get_id() in hidden_cells:
                hidden_cells.remove(cell.get_id())
            draw()

#  prints cells
def printcell(cell):
    print('[' + str(cell.row) + '] [' + str(cell.col) + ']')
# improved agent
# initially, query cell[0][0]
"""
 initially, query cell[0][0]
 if we get information from that, we can determine potential safe cells and keep clicking all the safecells until there are none left.
 Then we do an inference by contradiction. 
 we assume that a cell is a bomb, and if a contradiction arrives, we will assume it is a safe cell and add it back into the safe cells list
 else we will guess at random for that iteration
 and this will loop until all hidden cells are flagged 
"""
def driver2(grid, total_bombs, dim, draw):
    randomcells = []
    explored = set()
    revealed_bombs = []
    safe_cells = []
    revealed_dict = {}
    equ_list = []
    hidden_cells = list(range(0, dim ** 2))
    id_cell_dict = equ_list_dict(grid)
    startcell = grid[0][0]
    base_agent_query(revealed_dict, startcell, draw, revealed_bombs, safe_cells, explored, hidden_cells)
    equ_list.append(generate_equ(startcell))
    explored.add(startcell.get_id())

    lstofall = []
    while len(hidden_cells) > 0:
        while len(safe_cells) > 0:
            poppedcell = safe_cells.pop()
            base_agent_query(revealed_dict,poppedcell,draw,revealed_bombs,safe_cells,explored,hidden_cells)
            gen_equ = generate_equ(poppedcell)
            equ_list.append(gen_equ)
            lstofall.append(copy_equ(gen_equ))
            for equ in equ_list:
                elst = equ.list
                for id in elst:
                    if id_cell_dict[id] in revealed_dict.keys():
                        value = revealed_dict[id_cell_dict[id]]
                        equ.value -= value
                        elst.remove(id)
                if len(elst) == 1 and equ.value == 1:
                    single = elst.pop()
                    singlecell = id_cell_dict[single]
                    revealed_dict[singlecell] = 1
                    singlecell.flag_as_bomb()
                    print("THIS IS SINGE"+ str(single))
                    if single in hidden_cells:
                        hidden_cells.remove(single)
                    print("Flagged cell: "+str(single)+" as bomb")
                    equ_list.remove(equ)
            for equ in equ_list:
                if equ.getValue() == 0:
                    for id in equ.getlist():
                        if id not in explored:
                            safe_cells.append(id_cell_dict[id])
                    equ_list.remove(equ)
        if len(equ_list) > 0 and len(hidden_cells) > 0:
            temp_query_list = query_least_involved2(equ_list, hidden_cells)
            indi = 0
            while len(temp_query_list) > 0:
                    #  store id as keys not ACTUAL CELL
                assumptions = {}
                least_involved_cell = temp_query_list.pop()
                # print('THIS IS LEAST INVOLVED: '+str(least_involved_cell))
                copy_lstofall = copy_equ_list(lstofall)
                assumptions[least_involved_cell] = 1
                for equ in copy_lstofall:
                    elst = equ.list
                    if least_involved_cell in elst:
                        equ.value -= assumptions[least_involved_cell]
                        elst.remove(least_involved_cell)
            #       assuming hype train
            #     search for known assumptions and replaces them in equation
                ticker = 1
                while ticker > 0:
                    ticker = 0
                    for equ in copy_lstofall:
                        elst = equ.list
                        for id in elst:
                            if id in assumptions.keys():
                                equ.value -= assumptions[id]
                                elst.remove(id)
                        if equ.getValue() == 1 and len(elst) == 1:
                            single = elst.pop()
                            assumptions[single] = 1
                            ticker +=1
                            copy_lstofall.remove(equ)
                        if equ.getValue() == 0 and len(elst) > 0:
                            for id in elst:
                                assumptions[id] = 0
                                ticker += 1
                                elst.remove(id)
                            copy_lstofall.remove(equ)

                        # check for consistency between assumptions and revealed dict
                        # print(assumptions)
                        # printdict(revealed_dict)
                    for ids in assumptions.keys():
                        cell = id_cell_dict[ids]
                        if cell in revealed_dict.keys():
                            if revealed_dict[cell] != assumptions[ids]:
                                # print("Contradiction at: "+str(least_involved_cell))
                                indi = 1
                                break
                    if indi == 1:
                        print("Contradiction at c0: " + str(least_involved_cell))
                        safe_cells.append(id_cell_dict[least_involved_cell])
                        ticker = 0
                        indi = 0
                    else:
                        for equ in copy_lstofall:
                            if len(equ.getlist()) >= 0 and equ.getValue() < 0:
                                indi = 1
                                break
                            if len(equ_list) < equ.getValue():
                                indi = 1
                                break
                        if indi == 1:
                            print("Contradiction c1 at: " + str(least_involved_cell))
                            safe_cells.append(id_cell_dict[least_involved_cell])
                            ticker =\
                                0
                            indi = 0
        if len(hidden_cells) > 0 and len(safe_cells) <= 0:
            randcell = id_cell_dict[hidden_cells[(random.randrange(len(hidden_cells)))]]
            # base_agent_query(revealed_dict, randcell, draw, revealed_bombs, safe_cells, explored, hidden_cells)
            # explored.add(randcell.id)
            safe_cells.append(randcell)
            randomcells.append(randcell.id)
        # if len(hidden_cells) > 0 and len(safe_cells) <= 0:
        #     time.sleep(0.2)
        #     randcell = id_cell_dict[hidden_cells[(random.randrange(len(hidden_cells)))]]
        #     # base_agent_query(revealed_dict, randcell, draw, revealed_bombs, safe_cells, explored, hidden_cells)
        #     # explored.add(randcell.id)
        #     safe_cells.append(randcell)


    print("end ")
    print(safe_cells)
    # printEQlst(equ_list)
    return
def verify_revealed(revealed_dict,id_cell_dict,id,assumptions):
    if id_cell_dict[id] in revealed_dict.keys():
        if assumptions[id] != revealed_dict[id_cell_dict[id]]:
            return False
    return True
#             if assumptions[id] != revealed_dict[id_cell_dict[id]]:
def copy_equ(equ):
    lst = []
    for id in equ.getlist():
        lst.append(id)
    newEQU = Equation(lst,equ.value)
    return  newEQU
#     returns a least of least involved cells from greatest to least
def generate_equ(cell):
    temptlst = []
    for neighbor in cell.get_neighbors():
        temptlst.append(neighbor.get_id())
    equValue = cell.get_clue()
    tempEqu = Equation(temptlst,equValue)
    # printequation(tempEqu)
    return tempEqu
def query_least_involved2(equ_list, hidden_cells):
    templst = []
    for equ in equ_list:
        for var in equ.getlist():
            if var in hidden_cells and var not in templst:
                templst.append(var)
    templst.sort(key=templst.count, reverse=True)
    return templst

# print dictionaries
def printdict(dict):
    for key in dict:
        print(str(key.id) + ' ' + str(dict[key]))

# check if the equations are abnormal, IE CELL 1 = 3 bombs, No Cells = 2 bombs
# Cell 1 = -2 bombs
def check_equ_list(equ_list):
    for equ in equ_list:
        if equ.getValue() < 0:
            return False
        if len(equ.getlist()) <= 0 and equ.getValue() >= 1:
            return False
        if len(equ.getlist()) < equ.getValue():
            return False
    return True

# query cells whose equation values  == 0


# a dictionary that stores each cell with a corresponding cell ID
def equ_list_dict(grid):
    diction = {}
    for row in grid:
        for cell in row:
            id = cell.get_id()
            diction[id] = cell
    return diction

#  returns a copy of equations list
def copy_equ_list(equ_list):
    new_list = []
    for equ in equ_list:
        varlst = []
        for var in equ.getlist():
            varlst.append(var)
        new_list.append(Equation(varlst, equ.getValue()))
    return new_list

# print equations
def printequation(equation):
    b = ''
    for variable in equation.getlist():
        b += ' ' + str(variable) + ' '
        # print('THIS THE VARIABLE ' + str(variable))
    b += '= ' + str(equation.getValue())
    print(b + '\n')

# print a list
def printlist(list):
    b = ''
    for variable in list:
        b += ' ' + str(variable) + ' '
        # print('THIS THE VARIABLE ' + str(variable))
    print(b)

#
# def query_least_involved(equ_list, hidden_cells):
#     templst = []
#     for equ in equ_list:
#         for var in equ.getlist():
#             if var in hidden_cells:
#                 templst.append(var)
#     return min(templst, key=templst.count)

#print entire list of equations
def printEQlst(equ_list):
    for eq in equ_list:
        # print(len(eq.getlist()))
        printequation(eq)

#  calculates the score
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

