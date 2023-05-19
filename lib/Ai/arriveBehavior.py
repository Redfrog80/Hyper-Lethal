from .steering import *
from lib.misc import *
from lib.objects import Base

class arriveBehavior(steering):
    def __init__(self, weight, target_radius, slow_radius) -> None:
        super().__init__()
        self.weight = weight
        self.target = None
        self.target_radius = target_radius
        self.slow_radius = slow_radius
        
    def get_steering(self, steering_base: steeringBehavior, *args, **kwargs):
        steering = steering_data()
        
        if not self.target.liveflag:
            return steering
        
        direction = self.target.pos - self.obj.pos
        distance = direction.magnitude()
        
        targetSpeed = 0
        
        if (distance < self.target_radius) or not distance:
            return steering
        elif (distance < self.slow_radius):
            targetSpeed = steering_base.acc_max
        else:
            targetSpeed = steering_base.acc_max * (distance / self.slow_radius)
        
        targetVel = direction.normalize() * targetSpeed
        
        steering.acc = targetVel - self.obj.vel
        
        if steering.acc:
            steering.acc.clamp_magnitude_ip(steering_base.acc_max)

        steering.rot_vel = 0
        
        return steering