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
    'width': 60,
    'height': 20,
}

direction = {
    'x': 0,
    'y': 1
}

speed = {
    'x': 0,
    'y': 1
}

def setWindowPositionCentered(width, height):
    monitors = get_monitors()
    primaryMonitor = monitors[0]
    positionX = primaryMonitor.width / 2 - width / 2
    positionY = primaryMonitor.height / 2 - height / 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (positionX,positionY)
    os.environ['SDL_VIDEO_CENTERED'] = '0'

def getCircleCoordinatesPoints():
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

def moveCircleY():
    circle['y'] = circle['y'] + direction['y']

def moveCircleX():
    circle['x'] = circle['x'] + direction['x']

def redrawWindow(window):
    window.fill(white)

def getCenterDiference():
    rectCenter = rect['x'] + rect['width'] / 2
    return rectCenter - circle['x']

def collidedIntoPlataform():
    circlePoints = getCircleCoordinatesPoints()
    rectRight = rect['x'] + rect['width']
    for point in circlePoints:
        if point['x'] >= rect['x'] and point['x'] <= rectRight and point['y'] > 480 and point['y'] < 490:
            return True

    return False

def listenToEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_LEFT]):
        if rect['x'] > 0:
            rect['x'] = rect['x'] - 1
        
    if(keys[pygame.K_RIGHT]):
        if rect['x'] +  rect['width'] < 350:
            rect['x'] = rect['x'] + 1

def main():
    width = 350
    height = 500
    
    setWindowPositionCentered(width, height)
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ping Pong!")

    clock = pygame.time.Clock()
    counter = 0
    state = True
    while state:
        clock.tick(200)
        counter += 1
        listenToEvents()

        if speed['y'] != 0 and counter % speed['y'] == 0:
            moveCircleY()
        
        if speed['x'] != 0 and counter % speed['x'] == 0:
            moveCircleX()

        redrawWindow(window)
        pygame.draw.circle(window, black, (circle['x'], circle['y']), circle['radius'], circle['radius'])
        pygame.draw.rect(window, black, (rect['x'], rect['y'], rect['width'], rect['height']))
        pygame.display.update()

        if collidedIntoPlataform():

            print(getCenterDiference())

            direction['y'] = - 1

            if getCenterDiference() < 0:
                direction['x'] = 1
                
                if getCenterDiference() < -1 * (rect['width'] / 2 / 2 / 2):
                    speed['x'] = 3

                if getCenterDiference() < -1 * (rect['width'] / 2 / 2):
                    speed['x'] = 2

                if getCenterDiference() < -1 * (rect['width'] / 2):
                    speed['x'] = 1
                
            if getCenterDiference() > 0:
                direction['x'] = -1

                if getCenterDiference() > (rect['width'] / 2 / 2 / 2):
                    speed['x'] = 3

                if getCenterDiference() > (rect['width'] / 2 / 2):
                    speed['x'] = 2

                if getCenterDiference() > (rect['width'] / 2):
                    speed['x'] = 1
            
            if getCenterDiference() == 0:
                direction['x'] = 0
        
        print(speed['x'])
        
        if circle['x'] - circle['radius'] == 0:
            direction['x'] = 1

        if circle['x'] + circle['radius'] == width:
            direction['x'] = -1

        if circle['y'] - circle['radius'] == 0:
            direction['y'] = 1

main()