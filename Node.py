import pygame

pygame.init()
'''
font=pygame.font.SysFont('arial', 40)
text=font.render('0', True, (0, 0, 0))
'''
number_font = pygame.font.SysFont( None, 32 )
CLEAR = (255, 255, 255)
BOMB = (255, 0, 0)
HIDDEN = (67, 70, 75)
FREE = (255, 165, 0)
EXPLORED = (255, 165, 0)
BOMB_MARK = (255, 165, 0)
GREY = (128, 128, 128)
CLICKED = (0, 255, 0)

#HIDDEN = (67, 70, 75)
#CLEAR = (0, 255, 0)
#AGENT = (255, 255, 0)
#HIDDEN = (67, 70, 75)
#EXPLORED = (255, 165, 0)
#FREE = (255, 165, 0)
GREY = (128,128,128)

class Cell:
    def __init__(self, row, col, width, total_rows):
        self.id = total_rows * row + col
        self.value = 0


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.id = total_rows*row + col
        self.clue = 0
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.neighbors = []
        self.width = width
        self.state = CLEAR
        self.safe = True
        self.total_rows = total_rows
        self.reset = 0
    def set_reset(self):
        self.reset = 1
    def get_id(self):
        return self.id

    def is_safe(self):
        return self.safe

    def get_state(self):
        return self.state

    def set_bomb(self):
        self.state = BOMB
        self.safe = False

    def flag_as_bomb(self):
        self.state = BOMB

    def flag_as_clear(self):
        self.state = CLEAR

    def get_pos(self):
        return self.row, self.col

    def set_clear(self):
        self.state = CLEAR

    # def set_explored(self):
    #   self.state = EXPLORED

    def set_explored(self):
        self.state = EXPLORED

    def incr_value(self):
        self.clue += 1

    def set_clue(self, val):
        self.clue = val

    def get_clue(self):
        return self.clue

    def set_hidden(self):
        self.state = HIDDEN

    # calculate the clue for the cell
    def calc_clue(self):
        nei = self.get_neighbors()
        c = 0
        for cell in nei:
            if cell.get_state() == BOMB:
                c += 1
        self.clue = c

    def draw(self, win):
        pygame.draw.rect(win, self.state, (self.x, self.y, self.width, self.width))
        number_text = str(self.clue)
        number_image = number_font.render(number_text, True, (0, 0, 0), (255, 255, 255))
        # centre the image in the cell by calculating the margin-distance
        margin_x = (self.width - 1 - number_image.get_width()) // 2
        margin_y = (self.width - 1 - number_image.get_height()) // 2
        # Draw the number image
        win.blit(number_image, (self.x + 2 + margin_x, self.y + 2 + margin_y))

    def draw2(self, win):
        if self.get_state() == HIDDEN:
            pygame.draw.rect(win, HIDDEN, (self.x, self.y, self.width, self.width))
        elif self.get_state() == CLICKED:
            pygame.draw.rect(win, CLICKED, (self.x, self.y, self.width, self.width))
            number_text = str(self.clue)
            number_image = number_font.render(number_text, True, (0,0,0), (255,255,255))
            # centre the image in the cell by calculating the margin-distance
            margin_x = (self.width - 1 - number_image.get_width()) // 2
            margin_y = (self.width - 1 - number_image.get_height()) // 2
            # Draw the number image
            win.blit(number_image, (self.x + 2 + margin_x, self.y + 2 + margin_y))
        elif self.get_state() == BOMB:
            pygame.draw.rect(win, BOMB, (self.x, self.y, self.width, self.width))
        elif self.get_state() == CLEAR:
            pygame.draw.rect(win, CLEAR, (self.x, self.y, self.width, self.width))


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

        if self.row < self.total_rows - 1 and self.col > 0:  # bottom left
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row > 0 and self.col < self.total_rows - 1:  # top right
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1:  # bottom right
            self.neighbors.append(grid[self.row + 1][self.col + 1])

    def get_neighbors(self):
        return self.neighbors

    def set_neighbors(self, lst):
        self.neighbors = lst

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

    def setlist(self, newlist):
        self.list = newlist

