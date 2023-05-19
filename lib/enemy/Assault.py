import math

from pygame import Vector2
from ..Ai import *
from ..misc import *
from ..hulls.defaultHull import hull
from ..thrusters import thruster
from ..weapons import turret, bolter, flakker

from lib.objects import *


class Assault(Enemy):
    def __init__(self, **kwargs):
        
        kwargs["name"] = kwargs.get("name") or "Assault"
        kwargs["tag"] = kwargs.get("tag") or ENEMY_TAG
        kwargs["texture_size"] = kwargs.get("texture_size") or (64,64)
        kwargs["texture_name"] = kwargs.get("texture_name") or "enemy2"
        
        enemy_hull = hull(50, 0.02, 0.005)
        enemy_thruster = thruster(500, 400, 360)
        
        self.steeringBehavior = steeringBehavior(self, 
                                                 enemy_thruster.get_acc(),
                                                 enemy_thruster.get_rot_vel())
        
        super().__init__(hull = enemy_hull,
                         thruster = enemy_thruster,
                         **kwargs)

        weapon = flakker(projectile_tag = ENEMY_PROJECTILE_TAG,
                        projectile_texture_name = "bullet6",
                        image_dict = self.image_dict,
                        sound_dict = self.sound_dict,
                        damage = 4,
                        firerate = 2,
                        projectile_count = 10,
                        projectile_firing_angle = 15)
        
        self.turret = turret(name = "turret",
                             tag="turret",
                             texture_size = self.texture_size,
                             texture_name = "aiming",
                             image_dict = self.image_dict,
                             sound_dict = self.sound_dict)

        self.turret.attach_parent(self)
        self.turret.attach_weapon(weapon)
        
        self.thruster.attach_parent(self)

    def shoot(self, dt,  **kwargs):
        self.turret.fire(dt, **kwargs)

    def setTarget(self, target):
        self.steeringBehavior.add_steering_behavior(arriveBehavior(1, 50, 300), target)
        self.steeringBehavior.add_steering_behavior(evadeBehavior(.6,2), target)
        self.steeringBehavior.add_steering_behavior(faceAccBehavior(1), target)
        self.turret.set_target(target)
        super().setTarget(target)
    
    def set_world(self, world):
        super().set_world(world)
        self.world.add_game_object(self.turret)
    
    def destroy(self):
        super().destroy()
        self.turret.destroy()
    
    def update(self, dt: float, **kwargs):
        super().update(dt, **kwargs)
        
        target_rot = None
        
        diff = self.pos - self.target.pos
        mag = diff.magnitude()
        
        if mag:
            target_rot = degrees(math.atan2(*(diff/mag).xy))
        
        difference = self.turret.rot-target_rot
        while (abs(difference) > 180):
                    difference -= 360*sign(difference)
        
        if (abs(difference) < 5 and mag < self.turret.get_range()):
            self.shoot(dt)

        self.turret.target_rot = target_rot
