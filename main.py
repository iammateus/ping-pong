import pygame
import tkinter as tk
from ball import Ball
from random import randrange
from tkinter import messagebox
from Utils.windowconfig import setWindowPositionCentered

class Main:
    width = 350
    height = 500

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

    def __init__(self):
        setWindowPositionCentered(self.width, self.height)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ping Pong!")
        pygame.font.init()
        self.ball = Ball(self.window)

    def redrawWindow(self):
        self.window.fill(self.white)

    def getCenterBottomPlatformDistance(self):
        rectCenter = self.bottomRect['x'] + self.bottomRect['width'] / 2
        return rectCenter - self.ball.x

    def getCenterTopPlatformDistance(self):
        rectCenter = self.topRect['x'] + self.topRect['width'] / 2
        return rectCenter - self.ball.x

    def getCollidedIntoBottomPlataform(self):
        circlePoints = self.ball.getCoordinatesPoints()
        rectRight = self.bottomRect['x'] + self.bottomRect['width']
        for point in circlePoints:
            if point['x'] >= self.bottomRect['x'] and point['x'] <= rectRight and point['y'] > 480 and point['y'] < 490:
                return True

        return False

    def getCollidedIntoTopPlataform(self):
        circlePoints = self.ball.getCoordinatesPoints()
        rectRight = self.topRect['x'] + self.topRect['width']
        for point in circlePoints:
            if point['x'] >= self.topRect['x'] and point['x'] <= rectRight and point['y'] <= 20 and point['y'] >= 10:
                return True

        return False

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        keys = pygame.key.get_pressed()

        if(keys[pygame.K_LEFT]):
            if self.bottomRect['x'] > 0:
                self.bottomRect['x'] = self.bottomRect['x'] - 1
            
        if(keys[pygame.K_RIGHT]):
            if self.bottomRect['x'] +  self.bottomRect['width'] < 350:
                self.bottomRect['x'] = self.bottomRect['x'] + 1
        
        if(keys[pygame.K_a]):
            if self.topRect['x'] > 0:
                self.topRect['x'] = self.topRect['x'] - 1
            
        if(keys[pygame.K_d]):
            if self.topRect['x'] +  self.topRect['width'] < 350:
                self.topRect['x'] = self.topRect['x'] + 1

    def updateWindow(self):
        self.redrawWindow()
        self.ball.redraw()
        pygame.draw.rect(self.window, self.black, (self.bottomRect['x'], self.bottomRect['y'], self.bottomRect['width'], self.bottomRect['height']))
        pygame.draw.rect(self.window, self.black, (self.topRect['x'], self.topRect['y'], self.topRect['width'], self.topRect['height']))
        self.drawScore()
        pygame.display.update()

    def drawScore(self):
        scoreFont = pygame.font.SysFont("monospace", 16, 400)
        scoreText = "Top: " +  str(self.score["top"]) + " x Bottom: " + str(self.score["bottom"])
        scoreLabel =   scoreFont.render(scoreText, 1, self.black)
        self.window.blit(scoreLabel, (10, 40))

    def getYDirection(self):
        if self.ball.y > 250:
            return -1
        return 1

    def getXDirection(self, platform):
        if platform == "top":
            centerDistance = self.getCenterTopPlatformDistance()
        
        if platform == "bottom":
            centerDistance = self.getCenterBottomPlatformDistance()

        if centerDistance < 0:
            return 1
        return -1

    def getTopScored(self):
        return self.ball.y - self.ball.radius == 500

    def getBottomScored(self):
        return self.ball.y +  self.ball.radius == 0

    def run(self):
        clock = pygame.time.Clock()
        state = True
        while state:
            clock.tick(300)
            
            self.handleEvents()
            self.ball.move()
            self.updateWindow()

            collidedIntoBottomPlataform = self.getCollidedIntoBottomPlataform()
            collidedIntoTopPlataform = self.getCollidedIntoTopPlataform()
            if collidedIntoBottomPlataform or collidedIntoTopPlataform:
                if(collidedIntoBottomPlataform):
                    centerDistance = self.getCenterBottomPlatformDistance()
                    platform = "bottom"
                
                if(collidedIntoTopPlataform):
                    centerDistance = self.getCenterTopPlatformDistance()
                    platform = "top"

                self.ball.directionY = self.getYDirection()
                self.ball.directionX = self.getXDirection(platform)

                if centerDistance < 0:
                    centerDistance *= -1

                self.ball.speedX = 0

                if centerDistance > 0:
                    if centerDistance > (self.bottomRect['width'] / 2 / 2 / 2):
                        self.ball.speedX = 3

                    if centerDistance > (self.bottomRect['width'] / 2 / 2):
                        self.ball.speedX = 2

                    if centerDistance > (self.bottomRect['width'] / 2):
                        self.ball.speedX = 1
                
                if centerDistance == 0:
                    self.ball.directionX = 0
            
            if self.ball.x - self.ball.radius == 0:
                self.ball.directionX = 1

            if self.ball.x + self.ball.radius == self.width:
                self.ball.directionX = -1

            if self.getTopScored():
                self.score['top'] += 1
                self.ball.y = 500 - 60
                self.ball.x = 175
                self.ball.directionX = 0
                self.ball.directionY = -1
                self.updateWindow()
                pygame.time.wait(500)

            if self.getBottomScored():
                self.score['bottom'] += 1
                self.ball.y = 60
                self.ball.x = 175
                self.ball.directionX = 0
                self.ball.directionY = 1
                self.updateWindow()
                pygame.time.wait(500)

            # print('direction x: ' + str(direction['x']))
            # print('speed x: ' + str(speed['x']))

main = Main()
main.run()