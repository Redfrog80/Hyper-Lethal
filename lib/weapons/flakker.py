from .defaultWeapon import weapon
from lib.misc import *
from random import random, uniform
from lib.objects import Projectile

class flakker(weapon):
    def __init__(self, projectile_texture_name, projectile_tag, image_dict, sound_dict, **kwargs) -> None:
        super().__init__(image_dict = image_dict, sound_dict = sound_dict, **kwargs)
        self.set_projectile_weapon()
        
        self.damage_base = self.damage_base or 14
        self.firerate_base = self.firerate_base or .6
        self.range_base = self.range_base or 300
        self.sound_name = self.sound_name or "flakker"
        
        self.projectile_velocity_base = kwargs.get("projectile_velocity") or 700
        self.projectile_count = kwargs.get("projectile_count") or 15
        self.projectile_firing_angle = kwargs.get("projectile_firing_angle") or 30
        self.projectile_size = kwargs.get("projectile_size") or (50,50)
        self.projectile_texture_name = projectile_texture_name or "bullet1"
        self.projectile_tag = projectile_tag
        
        self.update_projectile_stats()

    def fire(self, dt,**kwargs ):
        return self.fire_projectile(dt,**kwargs)
    
    def fire_projectile(self, dt, world, **kwargs):
        if self.cooldown < 0:
            self.sound_dict.get_sound(self.sound_name).play()
            self.cooldown = self.firerate_real
            for i in range(self.projectile_count):
                bullet_rot = self.turret.rot + lerp(-self.projectile_firing_angle/2, self.projectile_firing_angle/2, (i+1)/(self.projectile_count+1))
                bullet = Projectile(tag = self.projectile_tag,
                                    damage = self.damage_real,
                                    life = self.projectile_life,
                                    texture_size = self.projectile_size,
                                    texture_name = self.projectile_texture_name,
                                    image_dict = self.image_dict)
                bullet.traj(self.turret.pos, self.turret.vel, self.projectile_velocity_real*(uniform(.6,1)), bullet_rot + uniform(-10,10), 1)
                world.__addlist__.append(bullet)
        self.cooldown -= dt
    