import pygame

FIRE = (255, 0, 0)
TARGET = (0, 255, 0)
START = (0, 255, 0)
AGENT = (255, 255, 0)
OPEN = (255, 255, 255)
BLOCKED = (0, 0, 0)
PATH = (128, 0, 128)
EXPLORED = (255, 165, 0)
GREY = (128, 128, 128)


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.state = OPEN
        self.is_closed = False
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.danger_value = 0
    def get_danger_neighbor(self):
        return self.danger_value, self
    def get_danger_value(self):
        return self.danger_value

    def get_pos(self):
        return self.row, self.col

    def get_state(self):
        return self.state

    def is_blocked(self):
        return self.state == BLOCKED

    def is_start(self):
        return self.state == START

    def is_target(self):
        return self.state == TARGET

    def is_on_fire(self):
        return self.state == FIRE

    def is_closed(self):
        return self.is_closed == True

    def set_danger_value(self, x):
        self.danger_value = x

    def set_closed(self):
        self.is_closed = True

    def set_start(self):
        self.state = START

    def set_blocked(self):
        self.state = BLOCKED

    def set_target(self):
        self.state = TARGET

    def set_path(self):
        self.state = PATH

    def set_on_fire(self):
        self.state = FIRE

    def set_as_agent(self):
        self.state = AGENT

    def set_explored(self):
        self.state = EXPLORED

    def draw(self, win):
        pygame.draw.rect(win, self.state, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_blocked():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_blocked():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_blocked():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_blocked():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

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