import pygame
import tkinter as tk
from ball import Ball
from random import randrange
from tkinter import messagebox
from Utils.windowconfig import setWindowPositionCentered

black = (0,0,0)
white = (255, 255, 255)

score = {
    'top': 0,
    'bottom': 0 
}

topRect = {
    'x': (350 - 60) // 2,
    'y': 0,
    'width': 60,
    'height': 20
}

bottomRect = {
    'x': (350 - 60) // 2,
    'y': 480,
    'width': 60,
    'height': 20
}

def redrawWindow(window):
    window.fill(white)

def getCenterBottomPlatformDistance(ball):
    rectCenter = bottomRect['x'] + bottomRect['width'] / 2
    return rectCenter - ball.x

def getCenterTopPlatformDistance(ball):
    rectCenter = topRect['x'] + topRect['width'] / 2
    return rectCenter - ball.x

def getCollidedIntoBottomPlataform(ball):
    circlePoints = ball.getCoordinatesPoints()
    rectRight = bottomRect['x'] + bottomRect['width']
    for point in circlePoints:
        if point['x'] >= bottomRect['x'] and point['x'] <= rectRight and point['y'] > 480 and point['y'] < 490:
            return True

    return False

def getCollidedIntoTopPlataform(ball):
    circlePoints = ball.getCoordinatesPoints()
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

def updateWindow(ball, window):
    redrawWindow(window)
    ball.redraw()
    pygame.draw.rect(window, black, (bottomRect['x'], bottomRect['y'], bottomRect['width'], bottomRect['height']))
    pygame.draw.rect(window, black, (topRect['x'], topRect['y'], topRect['width'], topRect['height']))
    drawScore(window)
    pygame.display.update()

def drawScore(window):
    scoreFont = pygame.font.SysFont("monospace", 16, 400)
    scoreText = "Top: " +  str(score["top"]) + " x Bottom: " + str(score["bottom"])
    scoreLabel =   scoreFont.render(scoreText, 1, (0,0,0))
    window.blit(scoreLabel, (10, 40))

def getYDirection(ball):
    if ball.y > 250:
        return -1
    return 1

def getXDirection(platform, ball):
    if platform == "top":
        centerDistance = getCenterTopPlatformDistance(ball)
    
    if platform == "bottom":
        centerDistance = getCenterBottomPlatformDistance(ball)

    if centerDistance < 0:
        return 1
    return -1

def getTopScored(ball):
    return ball.y - ball.radius == 500

def getBottomScored(ball):
    return ball.y +  ball.radius == 0

def main():
    width = 350
    height = 500
    
    setWindowPositionCentered(width, height)
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ping Pong!")
    pygame.font.init()

    clock = pygame.time.Clock()
    state = True
    ball = Ball(window)
    while state:
        clock.tick(300)
        listenToEvents()

        ball.move()

        updateWindow(ball, window)

        collidedIntoBottomPlataform = getCollidedIntoBottomPlataform(ball)
        collidedIntoTopPlataform = getCollidedIntoTopPlataform(ball)
        if collidedIntoBottomPlataform or collidedIntoTopPlataform:
            if(collidedIntoBottomPlataform):
                centerDistance = getCenterBottomPlatformDistance(ball)
                platform = "bottom"
            
            if(collidedIntoTopPlataform):
                centerDistance = getCenterTopPlatformDistance(ball)
                platform = "top"

            ball.directionY = getYDirection(ball)
            ball.directionX = getXDirection(platform, ball)

            if centerDistance < 0:
                centerDistance *= -1

            ball.speedX = 0

            if centerDistance > 0:
                if centerDistance > (bottomRect['width'] / 2 / 2 / 2):
                    ball.speedX = 3

                if centerDistance > (bottomRect['width'] / 2 / 2):
                    ball.speedX = 2

                if centerDistance > (bottomRect['width'] / 2):
                    ball.speedX = 1
            
            if centerDistance == 0:
                ball.directionX = 0
        
        if ball.x - ball.radius == 0:
            ball.directionX = 1

        if ball.x + ball.radius == width:
            ball.directionX = -1

        if getTopScored(ball):
            score['top'] += 1
            ball.y = 500 - 60
            ball.x = 175
            ball.directionX = 0
            ball.directionY = -1
            updateWindow(ball, window)
            pygame.time.wait(500)

        if getBottomScored(ball):
            score['bottom'] += 1
            ball.y = 60
            ball.x = 175
            ball.directionX = 0
            ball.directionY = 1
            updateWindow(ball, window)
            pygame.time.wait(500)

        # print('direction x: ' + str(direction['x']))
        # print('speed x: ' + str(speed['x']))

main()