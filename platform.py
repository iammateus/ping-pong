import pygame

class Platform:
    width = 60
    height = 20
    color = (0,0,0)

    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y

    def redraw(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height))
    
    def goLeft(self):
        self.x -= 1

    def goRight(self):
        self.x += 1