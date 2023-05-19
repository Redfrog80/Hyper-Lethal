from .steering import *
from lib.misc import *
from lib.objects import Base

class faceBehavior(steering):
    def __init__(self, weight) -> None:
        super().__init__()
        self.weight = weight
        self.target = None
        
    def get_steering(self, steering_base: steeringBehavior, *args, **kwargs):
        steering = steering_data()
        
        if not self.target.liveflag:
            return steering
        diff = self.target.pos - self.obj.pos
        
        direction = 0
        
        if diff:
            direction = degrees(atan2(*(diff).xy))
        
        difference = direction - self.obj.rot + 180
        print(direction, self.obj.rot)
        
        while (abs(difference) > 180):
            difference -= 360*sign(difference)

        print(difference)
        steering.rot_vel = difference

        return steering