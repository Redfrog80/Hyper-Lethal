from lib.hulls import hull
from ..thrusters import thruster
from .GameObject import GameObject


class Playable(GameObject):
    """Generic class for both player and enemy"""
    def __init__(self, hull: hull = hull(), thruster = thruster(), **kwargs):
        super().__init__(**kwargs)

        self.hull = hull
        self.thruster = thruster
        
        self.thruster.attach_parent(self)

    def set_world(self, world):
        super().set_world(world)

    def isDead(self):
        return self.hull.is_broken()

    def damage(self, value: float):
        return self.hull.damage(value)

    def gotHit(self, damage):
        if self.damage(damage):
            self.destroy()
    
    def update(self, dt, **kwargs):
        self.thruster.update(dt)
        super().update(dt, **kwargs)
        self.hull.update(dt)

        if self.isDead():
            self.destroy()
        

