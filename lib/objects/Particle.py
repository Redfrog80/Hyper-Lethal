
from ..objects import Camera
from ..misc import *
from .Base import Base

import pygame
from pygame import Rect, Surface, Vector2
import math
import random

class ParticleSimple(Base):
    def __init__(self, **kwargs):
        """
        Just a simple particle object
        """
        super().__init__(**kwargs)

        self.tag = self.tag or PARTICLE_TAG

        self.totallife = 0
        self.life = 0
        self.drag = 1
        self.color = (255,255,255)

    def set_random(self, velMax: int, lifeMax: float, drag: int):
        self.vel = Vector2(random.uniform(-1,1),random.uniform(-1,1))*random.random()*velMax
        self.totallife = random.random()*lifeMax
        self.life = self.totallife
        self.drag = drag

    def collisionEffect(self, dt, object):
        pass

    def update(self, dt: float, **kwargs):
        self.set_pos(self.pos + self.vel * dt)
        self.vel = (self.vel + self.acc * dt) / (1+dt*self.drag)
        
        self.life -= dt
        if (self.life < 0):
            self.destroy()

    def render(self):
        if self.collide_box(self.world.camera):  # render when object collide with camera view
            pygame.draw.ellipse(self.world.screen, self.color, Rect((self.pos - self.world.camera.topLeft).xy, (self.shape * (self.life/self.totallife)).xy))