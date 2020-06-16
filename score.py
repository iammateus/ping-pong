import pygame
from Utils.colors import Colors
class Score:
    def __init__(self, window):
        self.top = 0
        self.bottom = 0
        self.window = window
        self.font = pygame.font.SysFont("monospace", 16, 400)

    def addTop(self):
        self.top += 1
    
    def addBottom(self):
        self.bottom += 1

    def redraw(self):
        text = "Top: " +  str(self.top) + " x Bottom: " + str(self.bottom)
        label =   self.font.render(text, 1, Colors.black)
        self.window.blit(label, (10, 40))
