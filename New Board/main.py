import Node
import Agents
import sys
import pygame
import random
import copy

pygame.display.set_caption("CS440 Proj2")
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Mine Sweeper")
#pygame.init()

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
            print(templst)


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

def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Node.Cell(i, j, gap, rows)
            grid[i].append(cell)
    return grid

def generate_game_grid(grid, dim, totalbombs):
    curr_num_bomb = 0
    while curr_num_bomb < totalbombs:
        x = random.randrange(dim)
        y = random.randrange(dim)
        cell = grid[x][y]
        if cell.get_state() == Node.BOMB or cell == grid[0][0]:
            continue
        cell.set_bomb()
        curr_num_bomb += 1
        #update_bomb_clues(grid,cell)

def start_game_grid(game_grid):
    for row in game_grid:
        for cell in row:
            cell.set_hidden()
    return game_grid

def main(win, width, dimension, num_bombs):
    dim = dimension
    actual_grid = create_grid(dim,width)

    #printgrid(grid,len(grid))
    generate_game_grid(actual_grid, dim, num_bombs)
    calc_clues(actual_grid)
    printgrid(actual_grid,len(actual_grid))

    game_grid = actual_grid
    run = True
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
                    #print("actual_grid: ")
                    #print(actual_grid[0][0].get_neighbors())
                    Agents.base_agent(game_grid)

    pygame.quit()

if __name__ == '__main__':
    dimension = int(sys.argv[1])
    num_bombs = float(sys.argv[2])
    if num_bombs > dimension * dimension:
        print("Too many bombs")
        exit()
    main(WIN, WIDTH, dimension, num_bombs)