from pygame import Vector2
from lib.misc import *
from lib.objects.Collider import Collider

class Base(Collider):
    """
    Base class for all game object
    """

    def __init__(self, **kwargs) -> None:
        
        super().__init__(**kwargs)
        
        # This can be set manually, but should be set by the gameWorld as the object is added.
        self.world = kwargs.get("world")

        self.name = kwargs.get("name") or "unnamed_object"
        self.tag = kwargs.get("tag") or ""
        self.vel = kwargs.get("vel") or Vector2(0,0)
        self.acc = kwargs.get("acc") or Vector2(0,0)
        self.rot = kwargs.get("rot") or 0
        self.rotvel = kwargs.get("rotvel") or 0
        self.liveflag = 1  # use in GameWorld to check if object should be destroyed (go out of bound, died, etc.)

    def set_world(self, world):
        self.world = world

    def destroy(self):
        self.liveflag = 0

    def objAlive(self):
        return bool(self.liveflag)
    
    def update(self, dt, **kwargs):
        self.set_pos(self.pos + self.vel * dt)
        self.vel = self.vel + self.acc * dt
        
        self.rot += self.rotvel*dt
        while (abs(self.rot) > 180):
                self.rot -= 360*sign(self.rot) 
