import pygame
import tkinter as tk
from ball import Ball
from platform import Platform
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

    def __init__(self):
        setWindowPositionCentered(self.width, self.height)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ping Pong!")
        pygame.font.init()
        
        # Instantiates components
        self.ball = Ball(self.window)
        platformsX = (350 - 60) // 2
        self.topPlatform = Platform(self.window, platformsX, 0)
        self.bottomPlatform = Platform(self.window, platformsX, 480)

    def quit(self):
        pygame.quit()
        exit()

    def redrawWindow(self):
        self.window.fill(self.white)

    def getPlatformCenterDistanceToBall(self, platform):
        platformCenter = platform.x + platform.width / 2
        return platformCenter - self.ball.x

    def getCollidedIntoBottomPlataform(self):
        circlePoints = self.ball.getCoordinatesPoints()
        platformRight = self.bottomPlatform.x + self.bottomPlatform.width
        for point in circlePoints:
            if point['x'] >= self.bottomPlatform.x and point['x'] <= platformRight and point['y'] > 480 and point['y'] < 490:
                return True

        return False

    def getCollidedIntoTopPlataform(self):
        circlePoints = self.ball.getCoordinatesPoints()
        platformRight = self.topPlatform.x + self.topPlatform.width
        for point in circlePoints:
            if point['x'] >= self.topPlatform.x and point['x'] <= platformRight and point['y'] <= 20 and point['y'] >= 10:
                return True

        return False

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.bottomPlatform.x > 0:
                self.bottomPlatform.goLeft()
            
        if keys[pygame.K_RIGHT]:
            if (self.bottomPlatform.x +  self.bottomPlatform.width) < self.width:
                self.bottomPlatform.goRight()
        
        if keys[pygame.K_a]:
            if self.topPlatform.x > 0:
                self.topPlatform.goLeft()
            
        if keys[pygame.K_d]:
            if (self.topPlatform.x +  self.topPlatform.width) < self.width:
                self.topPlatform.goRight()
        
        if keys[pygame.K_ESCAPE]:
            self.quit()

    def updateWindow(self):
        self.redrawWindow()
        self.ball.redraw()
        self.topPlatform.redraw()
        self.bottomPlatform.redraw()
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
        centerDistance = self.getPlatformCenterDistanceToBall(platform)

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
            clock.tick(500)
            
            self.handleEvents()
            self.ball.move()
            self.updateWindow()

            collidedIntoBottomPlataform = self.getCollidedIntoBottomPlataform()
            collidedIntoTopPlataform = self.getCollidedIntoTopPlataform()
            if collidedIntoBottomPlataform or collidedIntoTopPlataform:
                if collidedIntoBottomPlataform:
                    centerDistance = self.getPlatformCenterDistanceToBall(self.bottomPlatform)
                    platform = self.bottomPlatform
                
                if collidedIntoTopPlataform:
                    centerDistance = self.getPlatformCenterDistanceToBall(self.topPlatform)
                    platform = self.topPlatform

                self.ball.directionY = self.getYDirection()
                self.ball.directionX = self.getXDirection(platform)

                if centerDistance < 0:
                    centerDistance *= -1

                self.ball.speedX = 0

                if centerDistance > 0:
                    if centerDistance > (Platform.width / 2 / 2 / 2):
                        self.ball.speedX = 3

                    if centerDistance > (Platform.width / 2 / 2):
                        self.ball.speedX = 2

                    if centerDistance > (Platform.width / 2):
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