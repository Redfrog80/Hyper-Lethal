from random import random
from ..Ai import *
from ..objects import *
from ..misc import *
from ..hulls.defaultHull import hull
from ..thrusters import thruster

class Kamikaze(Enemy):
    def __init__(self, **kwargs):
        
        kwargs["name"] = kwargs.get("name") or "Kamikaze"
        kwargs["tag"] = kwargs.get("tag") or ENEMY_TAG
        kwargs["texture_size"] = kwargs.get("texture_size") or (24,24)
        kwargs["texture_name"] = kwargs.get("texture_name") or "enemy1"
        
        enemy_hull = hull(30, 0.03)
        enemy_thruster = thruster(600, 400, 360)
        
        self.steeringBehavior = steeringBehavior(self, 
                                                 enemy_thruster.get_acc(),
                                                 enemy_thruster.get_rot_vel())        
        
        super().__init__(hull = enemy_hull,
                         thruster = enemy_thruster,
                         **kwargs)
        
        self.thruster.attach_parent(self)

        
        self.coll_damage = 10
        self.suicide = True
    
    def setTarget(self, target):
        self.steeringBehavior.add_steering_behavior(pursueBehavior(1.5,2), target)
        self.steeringBehavior.add_steering_behavior(dragBehavior(1,.4))
        self.steeringBehavior.add_steering_behavior(faceVelBehavior(2), target)
        super().setTarget(target)
        