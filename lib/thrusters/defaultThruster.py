from pygame import Vector2
from ..misc import *


class thruster():
    def __init__(self,
                 vel_max = 100,
                 acc = 10,
                 rot_vel = 45,
                 drag = 0.1,
                 **kwargs) -> None:
        
        self.vel_max_real = None
        self.vel_max_base = vel_max
        self.vel_max_multiplier = 1
        
        self.acc_real = None
        self.acc_base = acc
        self.acc_multiplier = 1

        self.rot_vel_real = None
        self.rot_vel_base = rot_vel
        self.rot_vel_multiplier = 1
        
        self.drag_real = None
        self.drag_base = drag
        self.drag_multiplier = 1
        
        self.parent = kwargs.get("parent") or None
        
        self.update_stats()

    def update_stats(self):
        self.vel_max_real = self.vel_max_base * self.vel_max_multiplier
        self.acc_real = self.acc_base * self.acc_multiplier
        self.rot_vel_real = self.rot_vel_base * self.rot_vel_multiplier
        self.drag_real = self.drag_base * self.drag_multiplier
        
    def attach_parent(self, other_object):
        self.parent = other_object
    
    def get_vel_max(self):
        return self.vel_max_real
    def get_acc(self):
        return self.acc_real
    def get_rot_vel(self):
        return self.rot_vel_real

    def update(self, dt, **kwargs):
        if (self.parent and self.parent.vel):
            self.parent.vel.clamp_magnitude_ip(self.vel_max_real)
            self.parent.acc += self.parent.vel * (-self.drag_real)