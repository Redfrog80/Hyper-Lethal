from .steering import *
from lib.misc import *
from lib.objects import Base

class pursueBehavior(steering):
    def __init__(self, weight, max_prediction) -> None:
        super().__init__()
        self.weight = weight
        self.max_prediction = max_prediction
        self.target = None
        
    def get_steering(self, steering_base: steeringBehavior, *args, **kwargs):
        steering = steering_data()
        
        if not self.target.liveflag:
            return steering
        
        diff = (self.target.pos - self.obj.pos)
        distance = diff.magnitude()
        speed = self.target.vel.magnitude()
        
        prediction = 0
        if (speed <= (distance / self.max_prediction)):
            prediction = self.max_prediction
        else:
            prediction = distance / speed
        
        predictedPos = self.target.pos + self.target.vel * prediction
        
        steering.acc = (predictedPos - self.obj.pos).normalize()
        steering.acc = steering.acc * steering_base.acc_max
        steering.rot_vel = 0
        return steering