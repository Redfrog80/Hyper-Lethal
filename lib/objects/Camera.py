from pygame import Vector2
from lib.misc import *
from .Base import Base

class Camera(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.follow_distance = 0
        self.world = kwargs.get("world")
        self.target = kwargs.get("target") or None
        self.shape = Vector2(kwargs.get("screen_dim")) / 2

    def set_world(self, world):
        self.world = world

    def follow_config(self, target, follow_distance):
        self.follow_distance = follow_distance
        self.target = target
        self.set_pos(target.pos)

    def trackTarget(self, dt):
        if bool(self.target):
            length = self.dist(self.target)
            unit = self.get_direction(self.target)
            if length > self.follow_distance:
                self.set_pos(self.pos + unit * (self.follow_distance-length))

    def update(self, dt: float, **kwargs):
        if self.world and self.target:
            self.trackTarget(dt)
            self.world.border_default(0, self)
                