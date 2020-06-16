import pygame
import math
from Utils.colors import Colors

class Ball:
    radius = 15
    size = 30

    def __init__(self, window):
        self.x = 175
        self.y = 60
        self.speedX = 0
        self.speedY = 1
        self.directionX = 0
        self.directionY = 1
        self.moveCounter = 0
        self.window = window

    def move(self):
        if (self.speedY != 0) and (self.moveCounter % self.speedY == 0):
            self.y = self.y + self.directionY
        
        if (self.speedX != 0) and (self.moveCounter % self.speedX == 0):
            self.x = self.x + self.directionX 

        self.moveCounter += 1   

    def redraw(self):
        pygame.draw.circle(self.window, Colors.black, (self.x, self.y), self.radius, self.radius)

    def getCoordinatesPoints(self):
        points = []
        for degree in range(360):
            radians = degree * math.pi/180;
            x = self.x + self.radius * math.cos(radians);
            y = self.y + self.radius * math.sin(radians);
            points.append({
                'x': x,
                'y': y
            })

        return points