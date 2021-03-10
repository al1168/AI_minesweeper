import pygame

FLAG = (255, 0, 0)
SAFE = (0, 255, 0)
AGENT = (255, 255, 0)
HIDDEN = (67, 70, 75)
EXPLORED = (255, 165, 0)
BOMB = (255, 165, 0)
GREY = (128, 128, 128)


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.id = total_rows*row + col
        self.value = 0
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.neighbors = []
        self.width = width
        self.state = HIDDEN
        self.total_rows = total_rows

    def set_bomb(self):
        self.state = BOMB

    def get_pos(self):
        return self.row, self.col

    def set_as_agent(self):
        self.state = AGENT

    def set_explored(self):
        self.state = EXPLORED

    def incr_value(self):
        self.value += 1

    def draw(self, win):
        pygame.draw.rect(win, self.state, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.row > 0 and self.col > 0:  # topLeft Diagonal
            self.neighbors.append(grid[self.row - 1][self.col - 1])

        if self.row < self.total_rows - 1 and self.col > 0:  # botleft
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row > 0 and self.col < self.total_row - 1:  # top right
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1:  # bottom right
            self.neighbors.append(grid[self.row + 1][self.col + 1])

    def get_neighbors(self):
        return self.neighbors

    def __lt__(self, other):
        return False


class Agent:
    def __init__(self, pos, row, col):
        self.pos = pos
        self.row = row
        self.col = col

    def get_pos(self):
        return self.pos

    def set_pos(self, position):
        self.pos = position


class Equation:
    def __init__(self, list, value):
        self.list = list
        self.value = value

    def getValue(self):
        return self.value

    def getlist(self):
        return self.list
