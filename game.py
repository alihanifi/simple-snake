from math import floor

import pygame
from pygame.locals import *
import time

from bait import Bait
from snake import Snake

game_height = 611
game_width = 914

BLOCK_SIZE = 23
TILE_COLOR = (195, 207, 161)
BG_COLOR = (64, 64, 64)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Classic Snake Game")
        self.surface = pygame.display.set_mode((game_width, game_height))
        self.pause_tile = pygame.image.load("resources\pause.png")
        self.lost_img = pygame.image.load("resources\game_lost.png")
        self.pause_sound = pygame.mixer.Sound("resources\sound_03.mp3")
        self.lost_sound = pygame.mixer.Sound("resources\sound_04.mp3")
        self.bg_img = pygame.image.load("resources\game_bg.png")
        self.numbers = [pygame.image.load("resources\z_0.png"), pygame.image.load("resources\z_1.png"),
                        pygame.image.load("resources\z_2.png"), pygame.image.load("resources\z_3.png"),
                        pygame.image.load("resources\z_4.png"), pygame.image.load("resources\z_5.png"),
                        pygame.image.load("resources\z_6.png"), pygame.image.load("resources\z_7.png"),
                        pygame.image.load("resources\z_8.png"), pygame.image.load("resources\z_9.png")]
        self.numbers_red = [pygame.image.load("resources\zz_0.png"), pygame.image.load("resources\zz_1.png"),
                            pygame.image.load("resources\zz_2.png"), pygame.image.load("resources\zz_3.png"),
                            pygame.image.load("resources\zz_4.png"), pygame.image.load("resources\zz_5.png"),
                            pygame.image.load("resources\zz_6.png"), pygame.image.load("resources\zz_7.png"),
                            pygame.image.load("resources\zz_8.png"), pygame.image.load("resources\zz_9.png")]

        # build places
        self.tiles = [[(0, 0) for x in range(18)] for y in range(32)]

        for i in range(18):
            for j in range(32):
                x = 90 + (j * 20) + (3 * j)
                y = 122 + (i * 20) + (3 * i)
                self.tiles[j][i] = (x, y)

        self.reset_game()

        # classes and variables
        self.snake = Snake(self, self.surface, 5)
        self.snake.draw()
        self.bait_1 = Bait(self, self.surface, 'bait_1')
        self.bait_2 = Bait(self, self.surface, 'bait_2')
        self.is_running = True
        self.game_status = ''
        self.score = 0
        self.level = 1
        self.speed = 0.3

    def reset_game(self):
        # build surface - draw background
        self.draw_background(self.surface)
        self.reset_board()

        # update display
        pygame.display.flip()

        self.snake = Snake(self, self.surface, 5)
        self.snake.draw()
        self.bait_1 = Bait(self, self.surface, 'bait_1')
        self.bait_2 = Bait(self, self.surface, 'bait_2')
        self.is_running = True
        self.game_status = ''
        self.score = 0
        self.level = 1
        self.speed = 0.3

    def locate_xy(self, part):
        xy = self.tiles[part[1]][part[0]]
        return xy

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        if self.game_status != 'lost':
                            pygame.mixer.Sound.play(self.pause_sound)
                            pause = not pause
                        else:
                            self.reset_game()
                            pause = False

                    if not pause and event.key == K_LEFT:
                        self.snake.move('left')

                    if not pause and event.key == K_RIGHT:
                        self.snake.move('right')

                    if not pause and event.key == K_UP:
                        self.snake.move('up')

                    if not pause and event.key == K_DOWN:
                        self.snake.move('down')

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
                    self.update_score_level()
                    time.sleep(self.speed - self.level * 0.00253)
                elif pause:
                    if self.game_status == '':
                        self.surface.blit(self.pause_tile, (834, 12))
                        pygame.display.flip()
                        time.sleep(1)
                        pygame.draw.rect(self.surface, BG_COLOR, pygame.Rect(832, 10, 50, 50))
                        pygame.display.flip()
                        time.sleep(1)
            except Exception as e:
                self.game_status = 'lost'
                pygame.mixer.Sound.play(self.lost_sound)
                rect = self.lost_img.get_rect()
                self.surface.blit(self.lost_img, (game_width / 2 - rect.width / 2, game_height / 2 - rect.height / 2))
                pygame.display.flip()
                pause = True

    def play(self):
        self.snake.walk()
        # draw elements
        snake_body = []
        for i in self.snake.body:
            snake_body.append(i)

        self.bait_1.draw(0.1, snake_body)
        snake_body.append(self.bait_1.position)
        self.bait_2.draw(0.2, snake_body)

        # check snake collision
        if self.snake.body_hit():
            raise "Collision Occurred"

        # check bait hit 1
        if self.snake.bait_hit(self.bait_1.position):
            print("snake ate {0} - from bait_1".format(self.bait_1.bait_type))
            self.bait_1.redefine()
            self.bait_1.clear()
            self.snake.increase_length(self.bait_1)
            self.score += self.bait_1.score

        # check bait hit 2
        if self.snake.bait_hit(self.bait_2.position):
            self.bait_2.redefine()
            self.bait_2.clear()
            print("snake ate {0} - from bait_2".format(self.bait_2.bait_type))
            self.snake.increase_length(self.bait_2)
            self.score += self.bait_2.score

    def update_score_level(self):
        is_red = False
        # calculate level
        self.level = int(self.score / 10)

        if self.level > 99:
            self.level = 99
            is_red = True

        # fix background
        pygame.draw.rect(self.surface, BG_COLOR, pygame.Rect(266, 18, 120, 50))
        pygame.draw.rect(self.surface, BG_COLOR, pygame.Rect(570, 18, 120, 50))
        self.surface.blit(self.bg_img, (250, 20), (230, 0, 500, 51))

        # calculate numbers
        hu = floor(self.score / 100)
        te = floor(self.score / 10) - hu * 10
        on = self.score - hu * 100 - te * 10

        if self.score < 999:
            score_hundred = self.numbers[hu]
            score_ten = self.numbers[te]
            score_one = self.numbers[on]
        else:
            score_hundred = self.numbers_red[9]
            score_ten = self.numbers_red[9]
            score_one = self.numbers_red[9]

        lte = floor(self.level / 10)
        lon = self.level - lte * 10

        if not is_red:
            level_ten = self.numbers[lte]
            level_one = self.numbers[lon]
        else:
            level_ten = self.numbers_red[lte]
            level_one = self.numbers_red[lon]

        # blit numbers on screen
        self.surface.blit(score_hundred, (266, 18))
        self.surface.blit(score_ten, (266 + 36, 18))
        self.surface.blit(score_one, (266 + 36 + 36, 18))

        self.surface.blit(level_ten, (586, 18))
        self.surface.blit(level_one, (586 + 36, 18))

        pygame.display.flip()

    def draw_background(self, surface):
        surface.fill(BG_COLOR)
        surface.blit(self.bg_img, (20, 20))

    def reset_board(self):
        for j in range(len(self.tiles)):
            for i in range(len(self.tiles[j])):
                xy = self.tiles[j][i]
                pygame.draw.rect(self.surface, TILE_COLOR, pygame.Rect(xy[0], xy[1], 20, 20))
