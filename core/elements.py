import math

import pygame

import colors
from utils import rot_point
from vector import Vec2d


class Ship(pygame.sprite.Sprite):
    def __init__(self, init_pos, init_dir, color=colors.g, size=500):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.Surface((500, 500))
        self._image.fill((0, 0, 0))
        self._image.set_colorkey((0, 0, 0))
        self.ta = (250, 100)
        self.tb = (50, 300)
        self.tc = (450, 300)

        pygame.draw.polygon(
            self._image,
            color,
            [self.ta, self.tb, self.tc],
            40)

        if size:
            scale = 500. / size

            scaled_im = pygame.transform.smoothscale(self._image, (size, size))
            self._image = scaled_im

            self.ta = (250 / scale, 100 / scale)
            self.tb = (50 / scale, 300 / scale)
            self.tc = (450 / scale, 300 / scale)
            self.te = (250 / scale, 380 / scale)
            self.tt = (100 / scale, 200 / scale)

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
        self.rotate_points(self.heading.angle - 90)

    def rotate(self, byangle):
        self.heading.rotate(byangle)
        self.rotate_points(byangle)

    def rotate_points(self, byangle):
        imrect = self.image.get_rect()
        rotc = imrect.center
        a = -byangle
        self.ta = rot_point(self.ta, rotc, a)
        self.tb = rot_point(self.tb, rotc, a)
        self.tc = rot_point(self.tc, rotc, a)
        self.te = rot_point(self.te, rotc, a)
        self.tt = rot_point(self.tt, rotc, a)

    def render_rotation(self):
        orig_rect = self._image.get_rect()
        rot_image = pygame.transform.rotate(self._image, self.heading.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.image = rot_image.subsurface(rot_rect).copy()
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, time_passed):
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

    def triangle_points(self):
        ox = self.rect.x
        oy = self.rect.y
        return map(lambda (x, y): (x + ox, y + oy),
                   [self.ta, self.tb, self.tc])


class Particle(pygame.sprite.Sprite):
    cache = {}

    def __init__(self, init_pos, init_dir, color=colors.g, size=500):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.Surface((500, 500))
        self._image.fill((0, 0, 0))
        self._image.set_colorkey((0, 0, 0))
        self._image.set_alpha(66)
        self.ta = (250, 100)
        self.tb = (50, 300)
        self.tc = (450, 300)

        pygame.draw.polygon(
            self._image,
            color,
            [self.ta, self.tb, self.tc],
            40)

        if size:
            scale = 500. / size
            key = ""+str(color) + str(scale)
            if key in Particle.cache:
                scaled_im = Particle.cache[key]
            else:
                scaled_im = pygame.transform.smoothscale(self._image, (size, size))
                Particle.cache[key] = scaled_im

            self._image = scaled_im

        self.pos = Vec2d(init_pos)
        # movement direction
        self.dir = Vec2d(init_dir).normalized()
        # we are we heading
        self.heading = Vec2d(init_dir).normalized()

        self.speed = 0.1
        self.force = 0.1

        self.rect = self._image.get_rect()
        self.rect.center = init_pos

        self.render_rotation()

    def rotate(self, byangle):
        self.heading.rotate(byangle)

    def render_rotation(self):
        orig_rect = self._image.get_rect()
        rot_image = pygame.transform.rotate(self._image, self.heading.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.image = rot_image.subsurface(rot_rect).copy()
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, time_passed):
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

        self.speed = min(10, d.length)
        self.dir.angle = math.degrees(math.atan2(d.y, d.x))

        super(Particle, self).update()


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
        self.rect.x = - (self.rect.width * progress)

        super(Progress, self).update()


class Tile(pygame.sprite.Sprite):
    def __init__(self, rect, color=colors.t, border=2, margin=6):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(rect.size)
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        sub = rect.copy()
        sub.topleft = (0, 0)
        self.sub = sub.inflate(-margin, -margin)
        pygame.draw.rect(
            self.image,
            color,
            self.sub,
            border)
        self.rect = self.image.get_rect(topleft=rect.topleft)
        self.sub.topleft = self.rect.topleft
        # collision rect
        self.crect = self.rect.inflate(-2, -2)

    def update(self):
        super(Tile, self).update()
