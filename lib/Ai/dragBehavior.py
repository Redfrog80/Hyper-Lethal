from .steering import *
from lib.misc import *
from lib.objects import Base

class dragBehavior(steering):
    def __init__(self, weight, drag) -> None:
        super().__init__()
        self.weight = weight
        self.drag = drag
        
    def get_steering(self, steering_base: steeringBehavior, *args, **kwargs):
        steering = steering_data()
        steering.acc = self.obj.vel*(-self.drag)
        steering.rot_vel = 0
        
        return steering