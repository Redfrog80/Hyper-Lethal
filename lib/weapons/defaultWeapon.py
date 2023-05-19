from lib.misc import *
from lib.objects import Projectile



class weapon:
    """The weapon base class is a template to build special weapon types. This is not a functional class!
    """
    def __init__(self, **kwargs) -> None:
        self.damage_real = None
        self.damage_base = kwargs.get("damage")
        self.damage_multiplier = 1
        
        self.firerate_real = None
        self.firerate_base = kwargs.get("firerate")
        self.firerate_multiplier = 1
        
        self.range_real = None
        self.range_base = kwargs.get("range")
        self.range_multiplier = 1
        
        self.is_projectile_weapon = False
        self.is_beam_weapon = False
        
        self.turret = kwargs.get("turret")

        self.sound_name = kwargs.get("sound_name")
        self.image_dict = kwargs.get("image_dict")
        self.sound_dict = kwargs.get("sound_dict")
        self.cooldown = 0
    
    def set_projectile_weapon(self):
        self.projectile_velocity_real = None
        self.projectile_velocity_base = None
        self.projectile_velocity_multiplier = 1
        self.projectile_life = None
        self.projectile_texture_name = None
        self.projectile_size = None
        self.projectile_count = 1
        self.projectile_firing_angle = None
        
        self.is_projectile_weapon = True
        self.is_beam_weapon = False
    
    # Need to get a collider set up for this weapon variant!
    # def set_beam_weapon(self):
    #     self.beam_range = None
    #     self.beam_width = None
    #     self.beam_texture = None
    #     self.beam_life = None
    #     self.beam_damaging_life = None
        
    #     self.is_projectile_weapon = False
    #     self.is_beam_weapon = True
    
    def update_stats(self):
        pass
    
    def fire(self, **kwargs ):
        pass

    def fire_projectile(self, dt, world,**kwargs):
        pass
    
    def update_projectile_stats(self):
        self.damage_real = self.damage_base * self.damage_multiplier
        self.firerate_real = self.firerate_base * self.firerate_multiplier
        self.range_real = self.range_base * self.range_multiplier
        self.projectile_velocity_real = self.projectile_velocity_base * self.projectile_velocity_multiplier
        self.projectile_life = self.range_real/self.projectile_velocity_real
        
    #TODO ADD REMAINING GETTERS
    def get_range(self):
        return self.range_real