import Node
import Agents
import sys
import pygame
import random


pygame.display.set_caption("CS440 Proj2")
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Mine Sweeper")
#pygame.init()

#print grid
def printcell(cell):
    print('[' + str(cell.row) + '] [' + str(cell.col) + ']')

#calculate clues for each cecll
def calc_clues(grid):
    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)
    for row in grid:
        for cell in row:
            cell.calc_clue()
            lst = cell.get_neighbors()
            templst = []
            for c in lst:
                templst.append(c.get_pos())
            # print(templst)

#update clues on cell
def update_bomb_clues(grid,bomb_cell):
    if bomb_cell.row < bomb_cell.total_rows - 1:  # DOWN
        grid[bomb_cell.row + 1][bomb_cell.col].incr_value()

    if bomb_cell.row > 0:  # UP
        grid[bomb_cell.row - 1][bomb_cell.col].incr_value()

    if bomb_cell.col < bomb_cell.total_rows - 1:  # RIGHT
        grid[bomb_cell.row][bomb_cell.col+1].incr_value()

    if bomb_cell.col > 0:  # LEFT
        grid[bomb_cell.row][bomb_cell.col-1].incr_value()

    if bomb_cell.row > 0 and bomb_cell.col > 0:  # topLeft Diagonal
        grid[bomb_cell.row -1][bomb_cell.col-1].incr_value()

    if bomb_cell.row < bomb_cell.total_rows - 1 and bomb_cell.col > 0:  # botleft
        grid[bomb_cell.row + 1][bomb_cell.col-1].incr_value()

    if bomb_cell.row > 0 and bomb_cell.col < bomb_cell.total_rows - 1:  # top right
        grid[bomb_cell.row -1][bomb_cell.col+1].incr_value()

    if bomb_cell.row < bomb_cell.total_rows - 1 and bomb_cell.col < bomb_cell.total_rows - 1:  # bottom right
        grid[bomb_cell.row + 1][bomb_cell.col+1].incr_value()

#pygaem draw grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Node.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Node.GREY, (j * gap, 0), (j * gap, width))

# draw the colors on py game
def draw(win, grid, rows, width):
    win.fill(Node.CLEAR)
    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def printgrid(grid, rows):
    for i in range(rows):
        for j in range(rows):
            cell = grid[i][j]
            print('[' + str(cell.row) + ']' + ' [' + str(cell.col) + ']' + 'VALUE\t'+str(cell.clue))
            # print(str(cell.color))

#create grid
def create_grid(rows, width):
    grid = []
    gap = width // rows
    dim = rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Node.Cell(i, j, gap, rows)
            grid[i].append(cell)
    return grid

#create minesweeper game grid with bombs
def generate_game_grid(grid, dim, totalbombs):
    curr_num_bomb = 0
    while curr_num_bomb < totalbombs:
        x = random.randrange(dim)
        y = random.randrange(dim)
        cell = grid[x][y]
        if cell.get_state() == Node.BOMB or cell == grid[0][0]:
            continue
        cell.set_bomb()
        cell.set_reset()
        curr_num_bomb += 1
        #update_bomb_clues(grid,cell)
#start the game grid
#hide all cells
def start_game_grid(game_grid):
    for row in game_grid:
        for cell in row:
            cell.set_hidden()
    return game_grid

#reset grid
def reset(grid):
    for row in grid:
        for cell in row:
            if cell.reset != 0:
                cell.set_bomb()
                continue
            cell.state = Node.CLEAR

#main function for running the program
def main(win, width, dimension, num_bombs):
    dim = dimension
    actual_grid = create_grid(dim,width)
    generate_game_grid(actual_grid, dim, num_bombs)
    calc_clues(actual_grid)

    game_grid = actual_grid
    run = True
    # Agents.driver(game_grid, num_bombs, dim, lambda: draw(win, actual_grid, dim, width))

    while run:
        draw(win, actual_grid, dim, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_grid = start_game_grid(actual_grid)

                #keyboard 'a' to start query using the basic agent
                if event.key == ord('a'):
                    Agents.driver2(game_grid, num_bombs, dim, lambda: draw(win, actual_grid, dim, width))
                if event.key == ord('b'):
                    Agents.base_agent(game_grid,lambda: draw(win, actual_grid, dim, width))
                if event.key == pygame.K_RETURN:
                    reset(game_grid)
    pygame.quit()

if __name__ == '__main__':
    dimension = int(sys.argv[1])
    num_bombs = float(sys.argv[2])

    #dimension = 10
    #num_bombs = 70
    if num_bombs > dimension * dimension:
        print("Too many bombs")
        exit()
    main(WIN, WIDTH, dimension, num_bombs)


