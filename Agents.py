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
    explored = []
    hidden_cells = []
    currCell = game_grid[0][0]
    print(revealed_dict)
    unrevealed_lst = []
    revealed_bombs = []
    for row in game_grid:
        for cell in row:
            unrevealed_lst.append(cell)

    print("Pre Loop")
    print(len(unrevealed_lst))
    step = 1
    basic_agent_query(revealed_dict, currCell, draw, unrevealed_lst)
    while len(unrevealed_lst) != 0:
        randCell = random.choice(unrevealed_lst)
        if randCell not in revealed_dict:
            print("Query number: "+str(step))
            basic_agent_query(revealed_dict, randCell, draw, unrevealed_lst)
            step += 1
    print("Post Loop")
    print(len(unrevealed_lst))

    print(calc_score(game_grid, revealed_dict))
    # print(revealed_dict)
    # bomb_list
    #print("bomb list:")
    #print(revealed_bombs)


def basic_agent_query(revealed_dict, cell, draw , unrevealed_list):
    if not cell.is_safe():
        cell.flag_as_bomb()
        revealed_dict[cell] = 1
        if cell in unrevealed_list:
            unrevealed_list.remove(cell)
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
            draw()
    elif (clue - len(revealed_mine_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_bomb()
            revealed_dict[c] = 1
            if c in unrevealed_list:
                unrevealed_list.remove(c)
            draw()
    elif ((len(neighbors) - clue) - len(revealed_cleared_nei_lst)) == len(hidden_nei_lst):
        for c in hidden_nei_lst: #mark all neighbors as bomb
            c.flag_as_clear()
            revealed_dict[c] = 0
            if c in unrevealed_list:
                unrevealed_list.remove(c)
            draw()



def base_agent_query(revealed_dict, cell, draw, revealed_bombs, safe_cell_lst, explored, hidden_cells):
    if cell.get_state() == Node.BOMB:
        print("LANDED ON BOMB AT")
        printcell(cell)
        cell.flag_as_bomb()
        revealed_dict[cell] = 1
        revealed_bombs.append(cell)
        if cell.get_id() in hidden_cells:
            hidden_cells.remove(cell.get_id())
    if cell.get_state() == Node.CLEAR:
        print("Cell is safe")
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


def driver2(grid, total_bombs, dim, draw):
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
    assumptions = []
    cnt = 0
    # while total_bombs != len(revealed_bombs):
    while len(safe_cells) > 0:
        click_safe_cells(safe_cells, revealed_dict, revealed_bombs, equ_list, draw, explored, hidden_cells)
        update_equations(equ_list, revealed_dict, id_cell_dict)
        fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
        safe_cell_adder2(equ_list, safe_cells, id_cell_dict, revealed_dict,revealed_bombs,draw,explored,hidden_cells)
        cnt += 1
    update_equations(equ_list, revealed_dict, id_cell_dict)
    print("\n\n\n")
    fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
    update_equations(equ_list, revealed_dict, id_cell_dict)
    fact_scan(equ_list, revealed_dict, id_cell_dict, hidden_cells)
    safe_cell_adder2(equ_list, safe_cells, id_cell_dict, revealed_dict, revealed_bombs, draw, explored, hidden_cells)
    print("\n\n\n")
    printEQlst(equ_list)
    print("LENg OF EQ LIST after  " + str(len(equ_list)))
    print("\n\n\n")
    print(hidden_cells)
    #     infereencing portion:
    if len(equ_list) > 0:
        printEQlst(equ_list)
        least_involved_cell = query_least_involved(equ_list,hidden_cells)
        equ_list_copy = copy_equ_list(equ_list)
        print("seperation")
        printEQlst(equ_list_copy)
        print("This is your least involved")
        print(least_involved_cell)
        # assume it is bomb.
        assumptions.append(least_involved_cell)
        revealed_dict[least_involved_cell] = 1
        for equ in equ_list_copy:
            for var in equ.getlist():
                if var == least_involved_cell:
                    equ.getlist().remove(var)
                    equ.value -= 1
        printEQlst(equ_list_copy)
def check_equ_list(equ_list):
    for equ in equ_list:
        if equ.getValue() < 0:
            return False
    return True
def safe_cell_adder(equ_list, safe_cells, id_cell_dict, revealed_dict,revealed_bombs,draw,explored,hidden_cells):
    for equ in equ_list:
        if equ.getValue() == 0 and len(equ.getlist()) > 0:
            for var in equ.getlist():
                cell = id_cell_dict[var]
                if cell not in revealed_dict:
                    click_safe_cells(safe_cells, revealed_dict, revealed_bombs, equ_list, draw, explored, hidden_cells)
            equ_list.remove(equ)

def safe_cell_adder2(equ_list, safe_cells, id_cell_dict, revealed_dict,revealed_bombs,draw,explored,hidden_cells):
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


def copy_equ_list(equ_list):
    new_list = []
    for equ in equ_list:
        varlst = []
        for var in equ.getlist():
            varlst.append(var)
        new_list.append(Equation(varlst, equ.getValue()))
    return new_list


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


def query_least_involved(equ_list, hidden_cells):
    templst = []
    for equ in equ_list:
        for var in equ.getlist():
            if var in hidden_cells:
                templst.append(var)
    return min(templst, key=templst.count)

def printEQlst(equ_list):
    for eq in equ_list:
        print(len(eq.getlist()))
        printequation(eq)

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
