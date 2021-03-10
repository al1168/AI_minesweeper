import Node
import sys
import pygame
import random
pygame.display.set_caption("CS440 Proj2")
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")
# draw lines on pygame application
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
    win.fill(Node.HIDDEN)
    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()
def printgrid(grid, rows):
    for i in range(rows):
        for j in range(rows):
            cell = grid[i][j]
            print('[' + str(cell.row) + ']' + ' [' + str(cell.col) + ']' + 'VALUE\t'+str(cell.value))
            # print(str(cell.color))

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

def generate_maze(grid, dim, totalbombs):
    curr_num_bomb = 0
    while curr_num_bomb < totalbombs:
        x = random.randrange(dim)
        y = random.randrange(dim)
        cell = grid[x][y]
        cell.set_bomb()
        curr_num_bomb += 1
        update_bomb_clues(grid,cell)

def main(win, width, dimension, num_bombs):
    dim = dimension
    grid = create_grid(dim,width)
    printgrid(grid,len(grid))
    generate_maze(grid, dim, num_bombs)
    printgrid(grid,len(grid))
    run = True
    while run:
        draw(win, grid, dim, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    return

if __name__ == '__main__':
    dimension = int(sys.argv[1])
    num_bombs = float(sys.argv[2])
    main(WIN, WIDTH, dimension, num_bombs)

def logic(cell):
#     cell = cell we want to determine if safe or naw

def click_safe_cells(safelist):
    for cell in safelist:
#         click cell
#         generate equations
#       add into equations_list
        pass
def query_least_involved():

    pass