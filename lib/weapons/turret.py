import math
from pygame import transform, Vector2

from lib.Ai import matchRotBehavior, turretBehavior

from ..misc import *
from ..Ai import *
from .defaultWeapon import weapon
from ..objects.GameObject import GameObject

class turret(GameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.steeringBehavior = steeringBehavior(self,0,360)

        self.parent = kwargs.get("parent") or None
        self.weapon = kwargs.get("weapon") or weapon(turret = self)
        self.target = None
        self.distance = None
        self.angle_diff = None
        
        self.independent_targeting = False
    
    # Use this to attach the gun to something
    def attach_parent(self, other_object):
        self.parent = other_object
    
    def set_target(self, target = None, weight = 1):
        self.steeringBehavior.clear_steering_behaviors()
        if target:
            # indep targeting and manual
            self.steeringBehavior.add_steering_behavior(turretBehavior(weight), target)
        else:
            # manual
            self.steeringBehavior.add_steering_behavior(matchRotBehavior(50), self.parent)
        self.target = target
    
    def find_target(self, range):
        # Searches gameworld tile map for nearest object
        # self.world.tileMap
        # Need to do some kind of spiral search
        # minObj = None
        # minDistSqr = 0
        # topLeft = element_floor_div(element_sub(self.pos, (range,range)), self.world.__tiledim__)
        # bottomRight = element_floor_div(element_add(self.pos, (range,range)), self.world.__tiledim__)
        # for c in range(topLeft[0],bottomRight[0] + 1):
        #     for r in range(topLeft[1],bottomRight[1] + 1):
        #         for obj in self.world.tileMap.get((c,r), []):
        #             dist_sqr = sum([pow(i,2) for i in element_sub(self.pos, obj.pos)])
        return None
    
    def attach_weapon(self, weapon : weapon):
        self.weapon = weapon
        self.weapon.turret = self
    
    def collisionEffect(self, *args, **kwargs):
        pass

    def update(self, dt, **kwargs):
        self.steeringBehavior.update(dt)

        if self.parent is not None:
            self.set_pos(self.parent.pos)
            self.vel = self.parent.vel
        
        if self.independent_targeting:
            # continiously scan for new targets if the current target is dead or out of range
            if self.target.isDead() or self.distance > self.get_range():
                self.set_target(self.find_target(self.get_range()))
            # automatically fire at target
            if (self.independent_targeting and abs(self.angle_diff) < 5):
                self.fire(dt)

        self.rot += self.rotvel * dt
    
    def fire(self, dt, **kwargs):
        self.weapon.fire(dt, world = self.world, **kwargs)
        
    def get_range(self):
        return self.weapon.get_range()
    

    def render(self):
        if self.collide_box(self.world.camera):  # render when object collide with camera view
            img0 = transform.rotate(self.texture, self.rot)
            dummy = Vector2(img0.get_size()) / 2
            self.world.screen.blit(img0, (self.pos - self.world.camera.topLeft - dummy).xy)