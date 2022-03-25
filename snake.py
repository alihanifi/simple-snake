import pygame

import game


class Snake:
    def __init__(self, game_w, surface, length):
        self.game = game_w
        self.surface = surface
        self.length = length
        self.length_add = 0
        self.direction = 'right'

        # get resources
        self.body_block = pygame.image.load("resources/tile.png")
        self.head_block = pygame.image.load("resources/tile_head.png")
        self.move_sound = pygame.mixer.Sound("resources/sound_01.mp3")
        self.eat_sound = pygame.mixer.Sound("resources/sound_02.mp3")

        # build body by length
        self.body = []
        for i in range(self.length):
            self.body.append((0, i))

    def move(self, where):
        if where == 'right':
            if self.direction != 'left':
                self.direction = 'right'
        elif where == 'left':
            if self.direction != 'right':
                self.direction = 'left'
        elif where == 'up':
            if self.direction != 'down':
                self.direction = 'up'
        elif where == 'down':
            if self.direction != 'up':
                self.direction = 'down'

    def walk(self):
        # update body
        body_pop = self.body.pop(0)
        if self.length_add > 0:
            self.length_add -= 1
            self.body.insert(0, body_pop)
        else:
            body_pos = self.game.locate_xy(body_pop)
            pygame.draw.rect(self.surface, game.TILE_COLOR, pygame.Rect(body_pos[0], body_pos[1], 20, 20))

        # update head
        head_p = self.body[len(self.body) - 1]
        # print('head is {0}'.format(head_p))
        # print(self.body)
        head_x = head_p[1]
        head_y = head_p[0]
        if self.direction == 'left':
            head_x -= 1
        if self.direction == 'right':
            head_x += 1
        if self.direction == 'up':
            head_y -= 1
        if self.direction == 'down':
            head_y += 1

        # check for out of bounds
        if head_x > 31:
            head_x = 0
        elif head_x < 0:
            head_x = 31

        if head_y > 17:
            head_y = 0
        elif head_y < 0:
            head_y = 17

        # add new part and draw
        self.body.append((head_y, head_x))
        self.draw()
        pygame.mixer.Sound.play(self.move_sound)

    def draw(self):
        for i in range(len(self.body)):
            body_p = self.body[i]
            xy = self.game.locate_xy(body_p)

            # only for head
            if i == len(self.body) - 1:
                if self.direction == 'down':
                    blit_rotate_center(self.surface, self.head_block, (xy[0], xy[1]), 90)
                elif self.direction == 'up':
                    blit_rotate_center(self.surface, self.head_block, (xy[0], xy[1]), -90)
                elif self.direction == 'right':
                    blit_rotate_center(self.surface, self.head_block, (xy[0], xy[1]), 180)
                elif self.direction == 'left':
                    self.surface.blit(self.head_block, (xy[0], xy[1]))

            # rest of the body
            else:
                self.surface.blit(self.body_block, (xy[0], xy[1]))
        pygame.display.flip()

    def increase_length(self, bait):
        pygame.mixer.Sound.play(self.eat_sound)
        self.length += bait.award
        self.length_add = bait.award

    def bait_hit(self, bait_position):
        if bait_position in self.body:
            return True
        else:
            return False

    def body_hit(self):
        if len(self.body) != len(set(self.body)):
            return True
        else:
            return False


def blit_rotate_center(surf, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    surf.blit(rotated_image, new_rect)
