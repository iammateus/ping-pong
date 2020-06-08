import pygame
import tkinter as tk
from ball import Ball
from random import randrange
from tkinter import messagebox
from Utils.windowconfig import setWindowPositionCentered

class Main:
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

    def redrawWindow(self, window):
        window.fill(self.white)

    def getCenterBottomPlatformDistance(self, ball):
        rectCenter = self.bottomRect['x'] + self.bottomRect['width'] / 2
        return rectCenter - ball.x

    def getCenterTopPlatformDistance(self, ball):
        rectCenter = self.topRect['x'] + self.topRect['width'] / 2
        return rectCenter - ball.x

    def getCollidedIntoBottomPlataform(self, ball):
        circlePoints = ball.getCoordinatesPoints()
        rectRight = self.bottomRect['x'] + self.bottomRect['width']
        for point in circlePoints:
            if point['x'] >= self.bottomRect['x'] and point['x'] <= rectRight and point['y'] > 480 and point['y'] < 490:
                return True

        return False

    def getCollidedIntoTopPlataform(self, ball):
        circlePoints = ball.getCoordinatesPoints()
        rectRight = self.topRect['x'] + self.topRect['width']
        for point in circlePoints:
            if point['x'] >= self.topRect['x'] and point['x'] <= rectRight and point['y'] <= 20 and point['y'] >= 10:
                return True

        return False

    def listenToEvents(self):
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

    def updateWindow(self, ball, window):
        self.redrawWindow(window)
        ball.redraw()
        pygame.draw.rect(window, self.black, (self.bottomRect['x'], self.bottomRect['y'], self.bottomRect['width'], self.bottomRect['height']))
        pygame.draw.rect(window, self.black, (self.topRect['x'], self.topRect['y'], self.topRect['width'], self.topRect['height']))
        self.drawScore(window)
        pygame.display.update()

    def drawScore(self, window):
        scoreFont = pygame.font.SysFont("monospace", 16, 400)
        scoreText = "Top: " +  str(self.score["top"]) + " x Bottom: " + str(self.score["bottom"])
        scoreLabel =   scoreFont.render(scoreText, 1, self.black)
        window.blit(scoreLabel, (10, 40))

    def getYDirection(self, ball):
        if ball.y > 250:
            return -1
        return 1

    def getXDirection(self, platform, ball):
        if platform == "top":
            centerDistance = self.getCenterTopPlatformDistance(ball)
        
        if platform == "bottom":
            centerDistance = self.getCenterBottomPlatformDistance(ball)

        if centerDistance < 0:
            return 1
        return -1

    def getTopScored(self, ball):
        return ball.y - ball.radius == 500

    def getBottomScored(self, ball):
        return ball.y +  ball.radius == 0

    def run(self):
        width = 350
        height = 500
        
        setWindowPositionCentered(width, height)
        window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ping Pong!")
        pygame.font.init()

        clock = pygame.time.Clock()
        ball = Ball(window)
        state = True
        while state:
            clock.tick(300)
            self.listenToEvents()

            ball.move()

            self.updateWindow(ball, window)

            collidedIntoBottomPlataform = self.getCollidedIntoBottomPlataform(ball)
            collidedIntoTopPlataform = self.getCollidedIntoTopPlataform(ball)
            if collidedIntoBottomPlataform or collidedIntoTopPlataform:
                if(collidedIntoBottomPlataform):
                    centerDistance = self.getCenterBottomPlatformDistance(ball)
                    platform = "bottom"
                
                if(collidedIntoTopPlataform):
                    centerDistance = self.getCenterTopPlatformDistance(ball)
                    platform = "top"

                ball.directionY = self.getYDirection(ball)
                ball.directionX = self.getXDirection(platform, ball)

                if centerDistance < 0:
                    centerDistance *= -1

                ball.speedX = 0

                if centerDistance > 0:
                    if centerDistance > (self.bottomRect['width'] / 2 / 2 / 2):
                        ball.speedX = 3

                    if centerDistance > (self.bottomRect['width'] / 2 / 2):
                        ball.speedX = 2

                    if centerDistance > (self.bottomRect['width'] / 2):
                        ball.speedX = 1
                
                if centerDistance == 0:
                    ball.directionX = 0
            
            if ball.x - ball.radius == 0:
                ball.directionX = 1

            if ball.x + ball.radius == width:
                ball.directionX = -1

            if self.getTopScored(ball):
                self.score['top'] += 1
                ball.y = 500 - 60
                ball.x = 175
                ball.directionX = 0
                ball.directionY = -1
                self.updateWindow(ball, window)
                pygame.time.wait(500)

            if self.getBottomScored(ball):
                self.score['bottom'] += 1
                ball.y = 60
                ball.x = 175
                ball.directionX = 0
                ball.directionY = 1
                self.updateWindow(ball, window)
                pygame.time.wait(500)

            # print('direction x: ' + str(direction['x']))
            # print('speed x: ' + str(speed['x']))

main = Main()
main.run()