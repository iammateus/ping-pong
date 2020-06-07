import os
import math
import pygame
import tkinter as tk
from random import randrange
from tkinter import messagebox
from screeninfo import get_monitors

black = (0,0,0)
white = (255, 255, 255)

circle = {
    'size': 30,
    'radius': 15,
    'x': 175,
    'y': 60
}

topRect = {
    'x': (350 - 60) // 2,
    'y': 0,
    'width': 60,
    'height': 20,
}

bottomRect = {
    'x': (350 - 60) // 2,
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

def getCenterBottomPlatformDistance():
    rectCenter = bottomRect['x'] + bottomRect['width'] / 2
    return rectCenter - circle['x']

def getCenterTopPlatformDistance():
    rectCenter = topRect['x'] + topRect['width'] / 2
    return rectCenter - circle['x']

def getCollidedIntoBottomPlataform():
    circlePoints = getCircleCoordinatesPoints()
    rectRight = bottomRect['x'] + bottomRect['width']
    for point in circlePoints:
        if point['x'] >= bottomRect['x'] and point['x'] <= rectRight and point['y'] > 480 and point['y'] < 490:
            return True

    return False

def getCollidedIntoTopPlataform():
    circlePoints = getCircleCoordinatesPoints()
    rectRight = topRect['x'] + topRect['width']
    for point in circlePoints:
        if point['x'] >= topRect['x'] and point['x'] <= rectRight and point['y'] <= 20 and point['y'] >= 10:
            return True

    return False

def listenToEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_LEFT]):
        if bottomRect['x'] > 0:
            bottomRect['x'] = bottomRect['x'] - 1
        
    if(keys[pygame.K_RIGHT]):
        if bottomRect['x'] +  bottomRect['width'] < 350:
            bottomRect['x'] = bottomRect['x'] + 1
    
    if(keys[pygame.K_a]):
        if topRect['x'] > 0:
            topRect['x'] = topRect['x'] - 1
        
    if(keys[pygame.K_d]):
        if topRect['x'] +  topRect['width'] < 350:
            topRect['x'] = topRect['x'] + 1

def updateWindow(window):
    redrawWindow(window)
    pygame.draw.circle(window, black, (circle['x'], circle['y']), circle['radius'], circle['radius'])
    pygame.draw.rect(window, black, (bottomRect['x'], bottomRect['y'], bottomRect['width'], bottomRect['height']))
    pygame.draw.rect(window, black, (topRect['x'], topRect['y'], topRect['width'], topRect['height']))
    pygame.display.update()

def getYDirection():
    if circle['y'] > 250:
        return -1
    return 1

def getXDirection(platform):
    if platform == "top":
        centerDistance = getCenterTopPlatformDistance()
    
    if platform == "bottom":
        centerDistance = getCenterBottomPlatformDistance()

    print(platform)
    print(centerDistance)

    if centerDistance < 0:
        return 1
    return -1

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
        clock.tick(300)
        counter += 1
        listenToEvents()

        if speed['y'] != 0 and counter % speed['y'] == 0:
            moveCircleY()
        
        if speed['x'] != 0 and counter % speed['x'] == 0:
            moveCircleX()

        updateWindow(window)

        collidedIntoBottomPlataform = getCollidedIntoBottomPlataform()
        collidedIntoTopPlataform = getCollidedIntoTopPlataform()
        if collidedIntoBottomPlataform or collidedIntoTopPlataform:
            if(collidedIntoBottomPlataform):
                centerDistance = getCenterBottomPlatformDistance()
                platform = "bottom"
            
            if(collidedIntoTopPlataform):
                centerDistance = getCenterTopPlatformDistance()
                platform = "top"

            direction['y'] = getYDirection()
            direction['x'] = getXDirection(platform)

            if centerDistance < 0:
                centerDistance *= -1

            if centerDistance > 0:
                if centerDistance > (bottomRect['width'] / 2 / 2 / 2):
                    speed['x'] = 3

                if centerDistance > (bottomRect['width'] / 2 / 2):
                    speed['x'] = 2

                if centerDistance > (bottomRect['width'] / 2):
                    speed['x'] = 1
            
            if centerDistance == 0:
                direction['x'] = 0
        
        if circle['x'] - circle['radius'] == 0:
            direction['x'] = 1

        if circle['x'] + circle['radius'] == width:
            direction['x'] = -1

        # print('direction x: ' + str(direction['x']))
        # print('speed x: ' + str(speed['x']))

main()