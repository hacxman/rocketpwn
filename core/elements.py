import math

import pygame

import colors
from vector import Vec2d


class Ship(pygame.sprite.Sprite):
    def __init__(self, init_pos, init_dir, color=colors.g):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.Surface((50, 50))
        self._image.fill((0, 0, 0))
        self._image.set_colorkey((0, 0, 0))
        pygame.draw.polygon(
            self._image,
            color,
            [[25, 10], [5, 30], [45, 30]],
            5)

        self.pos = Vec2d(init_pos)
        # movement direction
        self.dir = Vec2d(init_dir).normalized()
        # we are we heading
        self.heading = Vec2d(init_dir).normalized()

        self.speed = 0.
        self.force = 0.

        self.rect = self._image.get_rect()
        self.rect.center = init_pos

        self.render_rotation()

    def render_rotation(self):
        self.image = pygame.transform.rotate(
            self._image, self.heading.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, time_passed, new_heading):
        if new_heading:
            self.heading = new_heading

        self.render_rotation()

        self.speed *= 0.999

        d = Vec2d(
            self.dir.x * self.speed,
            self.dir.y * self.speed)
            #-self.dir.x * self.speed * time_passed,
            #self.dir.y * self.speed * time_passed)

        self.pos.x += d.x
        self.pos.y -= d.y
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        a = math.radians(self.heading.angle)
        d.x += math.cos(a) * self.force
        d.y += math.sin(a) * self.force

        self.speed = min(3, d.length)
        self.dir.angle = math.degrees(math.atan2(d.y, d.x))

        super(Ship, self).update()


class Progress(pygame.sprite.Sprite):
    def __init__(self, init_pos, init_size, color=colors.g):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(init_size)
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(
            self.image,
            color,
            (0, 0, init_size[0], init_size[1]))
        self.rect = self.image.get_rect(topleft=init_pos)

    def update(self, progress):
        #self.rect.x = self.rect.x - (self.rect.centerx * progress)
        self.rect.x = - (self.rect.width * progress)
        #self.rect.centery = self.pos.y

        super(Progress, self).update()
