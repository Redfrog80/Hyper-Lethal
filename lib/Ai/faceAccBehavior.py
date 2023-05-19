from pygame import Vector2
from .steering import *
from lib.misc import *
from lib.objects import Base

class faceAccBehavior(steering):
    def __init__(self, weight) -> None:
        super().__init__()
        self.weight = weight
        self.target = None
        
    def get_steering(self, steering_base: steeringBehavior, *args, **kwargs):
        steering = steering_data()
        
        if not self.target.liveflag:
            return steering
        
        direction = 0
        
        if self.obj.acc:
            direction = degrees(atan2(*self.obj.acc.xy))

        difference = direction - self.obj.rot + 180
        
        while (abs(difference) > 180):
            difference -= 360*sign(difference)

        steering.rot_vel = difference
        steering.acc = Vector2(0,0)
        return steering