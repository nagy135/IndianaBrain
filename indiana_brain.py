import numpy as np
import time
import pygame
import math
import random

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
WIDTH = 1000
HEIGHT = 1000
BLOCK_WIDTH = 50

class Game(object):
    def __init__(self, recording=False):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('NeuroBalancer')
        self.clock = pygame.time.Clock()
        self.player = [19,2]
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
                    [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
                    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
                    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 3, 1],
                    [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    ]
        self.map = np.array(self.map)

    def draw(self):
        self.draw_map()
        # pygame.draw.circle(self.gameDisplay, black, (int(self.head_x),int(self.head_y)), BALANCER_HEAD_RADIUS)
        # pygame.draw.circle(self.gameDisplay, red, (int(self.ball_x),int(self.ball_y)), BALL_RADIUS)
        # pygame.draw.line(self.gameDisplay, black, (self.ball_x-pri, self.ball_y+pro),(self.ball_x, self.ball_y), 5)
    def draw_treasure(self, x, y):
        pygame.draw.circle(self.gameDisplay, red, (x*BLOCK_WIDTH+BLOCK_WIDTH//2, y*BLOCK_WIDTH+BLOCK_WIDTH//2), BLOCK_WIDTH//2)

    def draw_end(self, x, y):
        pygame.draw.circle(self.gameDisplay, black, (x*BLOCK_WIDTH+BLOCK_WIDTH//2, y*BLOCK_WIDTH+BLOCK_WIDTH//2), BLOCK_WIDTH//2)

    def draw_player(self, x, y):
        pygame.draw.circle(self.gameDisplay, black, (x*BLOCK_WIDTH+BLOCK_WIDTH//2, y*BLOCK_WIDTH+BLOCK_WIDTH//2), BLOCK_WIDTH//2)
        pygame.draw.circle(self.gameDisplay, green, (x*BLOCK_WIDTH+BLOCK_WIDTH//2, y*BLOCK_WIDTH+BLOCK_WIDTH//2), BLOCK_WIDTH//4)

    def draw_map(self):
        for y,row in enumerate(self.map):
            for x,block in enumerate(row):
                if block == 1:
                    pygame.draw.rect(self.gameDisplay, black,(x*BLOCK_WIDTH,y*BLOCK_WIDTH, BLOCK_WIDTH,BLOCK_WIDTH) )
                elif block == 2:
                    self.draw_player(x, y)
                elif block == 3:
                    self.draw_treasure(x, y)
                elif block == 4:
                    self.draw_end(x, y)

    def move_player(self, dy, dx):
        try:
            if self.map[self.player[0] + dy][self.player[1] + dx] == 1:
                return False
        except IndexError:
            return False
        self.map[self.player[0]][self.player[1]] = 0
        self.player[0] += dy
        self.player[1] += dx
        self.map[self.player[0]][self.player[1]] = 2

    def start(self):
        end = False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                    if event.key == pygame.K_q:
                        end = True
                    if event.key == pygame.K_w:
                        self.move_player(-1, 0)
                    if event.key == pygame.K_a:
                        self.move_player(0, -1)
                    if event.key == pygame.K_s:
                        self.move_player(1, 0)
                    if event.key == pygame.K_d:
                        self.move_player(0, 1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                if event.type == pygame.QUIT:
                    end = True
            self.gameDisplay.fill(white)
            self.draw()
            pygame.display.update()
            self.clock.tick(30)
a = Game()
a.start()
