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
    currCell = game_grid[0][0]
    print(revealed_dict)
    unrevealed_lst = []
    revealed_bombs = []
    original_bombs = []
    for row in game_grid:
        for cell in row:
            unrevealed_lst.append(cell)
            if cell.get_state() == Node.BOMB:
                original_bombs.append(cell)

    print("Pre Loop")
    print(len(unrevealed_lst))
    step = 1
    basic_agent_query(revealed_dict, currCell, draw, unrevealed_lst, revealed_bombs)
    while len(unrevealed_lst) != 0:
        randCell = random.choice(unrevealed_lst)
        if randCell not in revealed_dict:
            print("Query number: "+str(step))
            basic_agent_query(revealed_dict, randCell, draw, unrevealed_lst, revealed_bombs)
            step += 1
    print("Post Loop")
    print(len(unrevealed_lst))

    print(calc_score(game_grid, revealed_dict))
    # print(revealed_dict)
    # bomb_list
    #print("bomb list:")
    #print(revealed_bombs)

# basic query function for basic agent, similar to how it was described on document
# revealed dict: stores current knowledge/facts agent knows
# cell: queried cell
# unreavealed_list : cells that have not been flagged
# revealed bombs: track number of bombs reveals so far
def basic_agent_query(revealed_dict, cell, draw , unrevealed_list, revealed_bombs):
    if not cell.is_safe():
        cell.flag_as_stepped()
        revealed_dict[cell] = 1
        if cell in unrevealed_list:
            unrevealed_list.remove(cell)
            revealed_bombs.append(cell)
        print("Stepped on bomb")
        draw()
    elif cell.is_safe():
        cell.flag_as_clear()
        revealed_dict[cell] = 0
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
            draw()
    elif (clue - len(revealed_mine_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_bomb()
            revealed_dict[c] = 1
            if c in unrevealed_list:
                unrevealed_list.remove(c)
                revealed_bombs.append(c)
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
    elif cell.safe == True:
        cell.flag_as_clear()
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
    # query 0 0 to start getting clues and safecells
    startcell = grid[0][0]
    base_agent_query(revealed_dict, startcell, draw, revealed_bombs, safe_cells, explored, hidden_cells)
    explored.add(startcell.get_id())
    assumptions = {}
    cnt = 0
    while len(hidden_cells) > 0:
        while len(safe_cells) > 0:
            click_safe_cells(safe_cells, revealed_dict, revealed_bombs, equ_list, draw, explored, hidden_cells)
            update_equations(equ_list, revealed_dict, id_cell_dict)
            fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
            safe_cell_adder3(equ_list, safe_cells, id_cell_dict, revealed_dict, revealed_bombs, draw, explored,
                             hidden_cells)
            cnt += 1
        update_equations(equ_list, revealed_dict, id_cell_dict)
        fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
        update_equations(equ_list, revealed_dict, id_cell_dict)
        fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
        safe_cell_adder3(equ_list, safe_cells, id_cell_dict, revealed_dict, revealed_bombs, draw, explored,
                         hidden_cells)
        #     contradiction portion:
        if len(equ_list) > 0 and len(hidden_cells) > 0:
            temp_query_list = query_least_involved2(equ_list, hidden_cells)
            while len(temp_query_list) > 0:
                equ_list_copy = copy_equ_list(equ_list)
                least_involved_cell = temp_query_list.pop()
                # assume it is bomb.
                assumptions[id_cell_dict[least_involved_cell]] = 1
                for equ in equ_list_copy:
                    for var in equ.getlist():
                        if var == least_involved_cell:
                            equ.getlist().remove(var)
                            equ.value -= 1

                x = safe_assume(equ_list_copy, assumptions, id_cell_dict)
                if not x:
                    safe_cells.append(id_cell_dict[least_involved_cell])
                    break

                if not check_equ_list(equ_list_copy):
                    safe_cells.append(id_cell_dict[least_involved_cell])
                    break
            #             else random
        if len(hidden_cells) > 0 and len(safe_cells) <= 0:
            randcell = id_cell_dict[hidden_cells[(random.randrange(len(hidden_cells)))]]
            base_agent_query(revealed_dict, randcell, draw, revealed_bombs, safe_cells, explored, hidden_cells)
            explored.add(randcell.id)
            randomcells.append(randcell.id)
    print(randomcells)
    print(len(randomcells))

    draw()
#     returns a least of least involved cells from greatest to least
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
def safe_cell_adder3(equ_list, safe_cells, id_cell_dict, revealed_dict, revealed_bombs, draw, explored, hidden_cells):
    for equ in equ_list:
        if equ.getValue() == 0 and len(equ.getlist()) > 0:
            for var in equ.getlist():
                cell = id_cell_dict[var]
                if cell not in revealed_dict:
                    base_agent_query(revealed_dict, cell, draw, revealed_bombs, safe_cells, explored, hidden_cells)
                    explored.add(cell.get_id())
            equ_list.remove(equ)

# add cells whose equation values  == 0 to safe cell list
def safe_cell_adder2(equ_list, safe_cells, id_cell_dict, revealed_dict, revealed_bombs, draw, explored, hidden_cells):
    for equ in equ_list:
        if equ.getValue() == 0 and len(equ.getlist()) > 0:
            for var in equ.getlist():
                cell = id_cell_dict[var]
                if cell not in revealed_dict:
                    safe_cells.append(cell)
            equ_list.remove(equ)
# adds safe cells to assumption dictionary based off the intial assumtion that a cell was a bomb:
# goal is to fine a contradiction
def safe_assume(equ_list, assumptions, id_cell_dict):
    for equ in equ_list:
        if equ.getValue() == 0 and len(equ.getlist()) > 0:
            for var in equ.getlist():
                cell = id_cell_dict[var]
                if cell in assumptions:
                    if equ.getValue() != assumptions[cell]:
                        return False
                assumptions[cell] = 0
            equ_list.remove(equ)
            update2(equ_list, assumptions, id_cell_dict)
        elif len(equ.getlist()) == 1:
            b = equ.getlist().pop()
            if id_cell_dict[b] in assumptions:
                if equ.getValue() != assumptions[id_cell_dict[b]]:
                    return False
            assumptions[id_cell_dict[b]] = equ.getValue()
            update2(equ_list, assumptions, id_cell_dict)
            equ_list.remove(equ)
    return True
# update equations for during inferencing
def update2(equ_list, assumptions, id_cell_dict):
    for equ in equ_list:
        for var in equ.getlist():
            if id_cell_dict[var] in assumptions:
                equ.getlist().remove(var)
                equ.value -= assumptions[id_cell_dict[var]]

#  iterate through safe cells and create equations for them
def click_safe_cells(safelist, revealed_dict, revealed_bombs, equ_list, draw, explored, hidden_cells):
    for cell in safelist:
        #         click cell
        base_agent_query(revealed_dict, cell, draw, revealed_bombs, safelist, explored, hidden_cells)
        explored.add(cell.get_id())
        equation_variable_ids = []
        for neighbor in cell.get_neighbors():
            equation_variable_ids.append(neighbor.id)

        eq = Equation(equation_variable_ids, cell.get_clue())
        equ_list.append(eq)
        safelist.remove(cell)

# find equations that have 1 variable and flag it based on the value as  well as add it to a fact knowledge base/dictionary
def fact_scan(equ_list, revealed_list, id_cell_dict, hidden_cells):
    for equ in equ_list:
        if len(equ.getlist()) == 1:
            var = equ.getlist().pop()
            cell = id_cell_dict[var]
            clue = equ.getValue()
            if cell not in revealed_list:
                revealed_list[cell] = clue
            if var in hidden_cells:
                if clue == 1:
                    cell.flag_as_bomb()
                if clue == 0:
                    cell.flag_as_clear()
                hidden_cells.remove(var)
            equ_list.remove(equ)


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

#  update equations based on facts known from revealed dictionary
def update_equations(equ_list, revealed_dict, id_cell_dict):
    for equ in equ_list:
        newequ = equ.getlist()
        for var in newequ:
            cell = id_cell_dict[var]
            if cell in revealed_dict:
                equ.value -= revealed_dict[cell]
                equ.list.remove(var)
        if len(equ.getlist()) <= 0 and equ.getValue() == 0:
            equ_list.remove(equ)
            continue

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

