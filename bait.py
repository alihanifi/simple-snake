import pygame
import random
import game


class Bait:
    def __init__(self, game_w, surface, name):
        self.game = game_w
        self.surface = surface
        self.name = name
        self.current_life = 0
        self.position = (0, 0)
        self.bait_type = ''
        self.award = 0
        self.life = 0
        self.block = 0
        self.score = 0
        self.redefine()

    def redefine(self):
        self.current_life = 0
        r = random.random()
        if 0 < r < 0.1:
            self.bait_type = 'bird'
        elif 0.1 <= r < 0.7:
            self.bait_type = 'apple'
        elif r >= 0.7:
            self.bait_type = 'mouse'

        if self.bait_type == 'apple':
            self.award = 1
            self.score = 3
            self.life = 6
            self.block = pygame.image.load("resources/bait_1.png")
        elif self.bait_type == 'mouse':
            self.award = 2
            self.score = 12
            self.life = 4
            self.block = pygame.image.load("resources/bait_2.png")
        elif self.bait_type == 'bird':
            self.award = 3
            self.score = 36
            self.life = 3
            self.block = pygame.image.load("resources/bait_3.png")
        elif self.bait_type == '':
            self.award = 0
            self.life = 0
            self.block = 0

    def draw(self, life_progress, snake_body):
        self.current_life += life_progress
        if self.bait_type != '':
            if self.current_life > self.life:
                self.redefine()
                self.clear()
                self.position = (random.randint(0, 17), random.randint(0, 31))
                while self.position in snake_body:
                    self.position = (random.randint(0, 17), random.randint(0, 31))
                print('new bait position {0}'.format(self.position))
                xy = self.game.locate_xy(self.position)
                self.surface.blit(self.block, (xy[0], xy[1]))
        pygame.display.flip()

    def clear(self):
        xy = self.game.locate_xy(self.position)
        pygame.draw.rect(self.surface, game.TILE_COLOR, pygame.Rect(xy[0], xy[1], 20, 20))
        self.position = (-1, -1)
