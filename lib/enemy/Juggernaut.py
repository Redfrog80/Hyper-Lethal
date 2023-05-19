import math
from lib.misc import *
from lib.objects import *
from ..Ai import *
from ..misc import *
from ..hulls.defaultHull import hull
from ..thrusters import thruster
from ..weapons import turret, bolter, flakker


class Juggernaut(Enemy):
    def __init__(self, **kwargs):
        
        kwargs["name"] = kwargs.get("name") or "Juggernaut"
        kwargs["tag"] = kwargs.get("tag") or ENEMY_TAG
        kwargs["texture_size"] = kwargs.get("texture_size") or (128,128)
        kwargs["texture_name"] = kwargs.get("texture_name") or "Emperor1"
        

        enemy_hull = hull(200, 0.01, 0.02)
        enemy_thruster = thruster(100, 40, 180)
        
        self.steeringBehavior = steeringBehavior(self, 
                                                 enemy_thruster.get_acc(),
                                                 enemy_thruster.get_rot_vel())
        
        super().__init__(hull = enemy_hull,
                         thruster = enemy_thruster,
                         **kwargs)

        weapon = bolter(projectile_tag = ENEMY_PROJECTILE_TAG,
                        projectile_texture_name = "bullet5",
                        image_dict = self.image_dict,
                        sound_dict = self.sound_dict,
                        damage = 20,
                        firerate = 2,
                        range = 600,
                        projectile_velocity = 800,
                        projectile_size = (100,100))
        
        self.turret = turret(name = "turret",
                             tag="turret",
                             min_rot_vel = 45,
                             max_rot_vel = 180,
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
        self.steeringBehavior.add_steering_behavior(arriveBehavior(1, 400, 600), target)
        self.steeringBehavior.add_steering_behavior(fleeBehavior(.2), target)
        self.steeringBehavior.add_steering_behavior(faceBehavior(1), target)
        self.turret.set_target()

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
        
        diff = self.pos-self.target.pos
        mag = diff.magnitude()
        
        if mag:
            target_rot = degrees(math.atan2(*(diff/mag).xy))
        
        difference = self.turret.rot-target_rot
        while (abs(difference) > 180):
                    difference -= 360*sign(difference)
        
        if (abs(difference) < 5 and mag < self.turret.get_range()):
            self.shoot(dt)
        self.turret.target_rot = target_rot
