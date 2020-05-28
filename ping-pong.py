import os
import pygame
import tkinter as tk
from random import randrange
from tkinter import messagebox
from screeninfo import get_monitors
import math

white = (255, 255, 255)
black = (0,0,0)

circle = {
    'size': 30,
    'radius': 15,
    'x': 175,
    'y': 20
}

rect = {
    'x': 110,
    'y': 480,
    'xSize': 60,
    'ySize': 20,
}

def setWindowPositionCentered(width, height):
    monitors = get_monitors()
    primaryMonitor = monitors[0]
    positionX = primaryMonitor.width / 2 - width / 2
    positionY = primaryMonitor.height / 2 - height / 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (positionX,positionY)
    os.environ['SDL_VIDEO_CENTERED'] = '0'

def getCirclePoints():
    
    points = []
    
    for degree in range(360):
        
        radians = degree * math.pi/180;
        
        positionX = circle['x'] + circle['radius'] * math.cos(radians);
        positionY = circle['y'] + circle['radius'] * math.sin(radians);
        
        points.append({
            'x': positionX,
            'y': positionY
        })
    
    return points

def redrawWindow(window):
    window.fill(white)

def getCenterDiference():
    rectCenter = rect['x'] + rect['xSize'] / 2
    return rectCenter - circle['x']

def getCollision():
    
    circlePoints = getCirclePoints()
    
    if circle['y'] + circle['radius'] < 480:
        return False

    rectRight = rect['x'] + rect['xSize']

    for point in circlePoints:
        if point['x'] >= rect['x'] and point['x'] <= rectRight and point['y'] > 480:
            return True

    return False

def main():
    sizeY = 350
    sizeX = 500
    
    setWindowPositionCentered(sizeY, sizeX)
    window = pygame.display.set_mode((sizeY, sizeX))
    pygame.display.set_caption("Ping Pong!")

    clock = pygame.time.Clock()

    state = True
    while state:

        clock.tick(50)

        redrawWindow(window)
        pygame.draw.circle(window, black, (circle['x'], circle['y']), circle['radius'], circle['radius'])
        
        circle['y'] = circle['y'] + 1

        pygame.draw.rect(window, black, (rect['x'], rect['y'], rect['xSize'], rect['ySize']))

        pygame.display.update()

        if getCollision():
            print('Hit')
            print(getCenterDiference())
            while True:
                pass

main()