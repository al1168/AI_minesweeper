import Node
import random
import time



class Equation:
    def __init__(self, list, value):
        self.list = list
        self.value = value

    def getValue(self):
        return self.value

    def getlist(self):
        return self.list


def base_agent(game_grid, draw):
    safe_cell_lst = []
    revealed_dict = {}
    currCell = game_grid[0][0]
    print(revealed_dict)
    unrevealed_lst = []
    revealed_bombs = []
    for row in game_grid:
        for cell in row:
            unrevealed_lst.append(cell)

    count = 5
    while count != 0:
        base_agent_query(revealed_dict, currCell, draw, revealed_bombs, safe_cell_lst)
        base_agent_query(revealed_dict, currCell, draw, revealed_bombs, safe_cell_lst)
        for item in unrevealed_lst:
            if item in revealed_dict:
                unrevealed_lst.remove(item)
        if unrevealed_lst == []:
            break
        randCell = random.choice(unrevealed_lst)
        currCell = randCell
        count -= 1

    # print(revealed_dict)
    # bomb_list
    print("bomb list:")
    print(revealed_bombs)


def base_agent_query(revealed_dict, cell, draw, revealed_bombs, safe_cell_lst, explored, hidden_cells):
    if cell.get_state() == Node.BOMB:
        print("LANDED ON BOMB AT")
        printcell(cell)
        cell.flag_as_bomb()
        revealed_dict[cell] = 1
        revealed_bombs.append(cell)
        if cell.get_id() in hidden_cells:
            hidden_cells.remove(cell.get_id())
    elif cell.get_state() == Node.CLEAR:
        cell.flag_as_clear()
        revealed_dict[cell] = 0
        if cell.get_id() in hidden_cells:
            hidden_cells.remove(cell.get_id())
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


def printcell(cell):
    print('[' + str(cell.row) + '] [' + str(cell.col) + ']')


# def query(cell):
#     if cell.get_state() == Node.BOMB:
#         cell.flag_as_bomb()


def driver(grid, total_bombs, dim, draw):
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
    # hidden_cells.remove(0)
    cnt = 0
    # while total_bombs != len(revealed_bombs):
    while len(safe_cells) > 0:
        click_safe_cells(safe_cells, revealed_dict, revealed_bombs, equ_list, draw, explored, hidden_cells)
        update_equations(equ_list, revealed_dict, id_cell_dict)
        fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
        # for equ in equ_list:
        #     if equ.getValue() == 0 and len(equ.getlist()) > 0:
        #         for var in equ.getlist():
        #             cell = id_cell_dict[var]
        #             if cell not in revealed_dict:
        #
        #                 safe_cells.append(cell)
        #         equ_list.remove(equ)
        safe_cell_adder(equ_list,safe_cells,id_cell_dict,revealed_dict)
        cnt += 1
    update_equations(equ_list, revealed_dict, id_cell_dict)
    print("\n\n\n")
    fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)

    fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
    update_equations(equ_list, revealed_dict, id_cell_dict)
    fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
    print("\n\n\n")
    for eq in equ_list:
        print(len(eq.getlist()))
        printequation(eq)
    print("LENg OF EQ LIST after  " + str(len(equ_list)))
    print("\n\n\n")
    print(hidden_cells)


def safe_cell_adder(equ_list,safe_cells,id_cell_dict,revealed_dict):
    for equ in equ_list:
        if equ.getValue() == 0 and len(equ.getlist()) > 0:
            for var in equ.getlist():
                cell = id_cell_dict[var]
                if cell not in revealed_dict:
                    safe_cells.append(cell)
            equ_list.remove(equ)

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


def fact_scan(equ_list, revealed_list, id_cell_dict, hidden_cells):
    for equ in equ_list:
        if len(equ.getlist()) == 1:
            printlist(equ.getlist())
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
            for equation in equ_list:
                printequation(equation)
            equ_list.remove(equ)
    print("stop here")

def removeall(equ_list):
    print('\n\n\n')
    for equ in equ_list:
        if len(equ.getlist()) <= 1:
            equ_list.remove(equ)
    for eq in equ_list:
        print(len(eq.getlist()))
        printequation(eq)
    print("LENg OF EQ LIST after REMOVE " + str(len(equ_list)))
def equ_list_dict(grid):
    diction = {}
    for row in grid:
        for cell in row:
            id = cell.get_id()
            diction[id] = cell
    return diction


def update_equations(equ_list, revealed_dict, id_cell_dict):
    for equ in equ_list:
        if len(equ.getlist()) <= 0:
            equ_list.remove(equ)
            continue
        newequ = equ.getlist()
        for var in newequ:
            cell = id_cell_dict[var]
            if cell in revealed_dict:
                equ.value -= revealed_dict[cell]
                equ.list.remove(var)
        if len(equ.getlist()) <= 0:
            equ_list.remove(equ)
            continue


def printequation(equation):
    b = ''
    for variable in equation.getlist():
        b += ' ' + str(variable) + ' '
        # print('THIS THE VARIABLE ' + str(variable))
    b += '= ' + str(equation.getValue())
    print(b)

def printlist(list):
    b = ''
    for variable in list:
        b += ' ' + str(variable) + ' '
        # print('THIS THE VARIABLE ' + str(variable))
    print(b)
def query_least_involved(equ_list):
    
    pass
