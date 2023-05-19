from pygame import draw
from random import random
from lib.Ai import *
from .Playable import Playable
from .Projectile import Projectile
from lib.misc import *
import math


class Enemy(Playable):
    """
    Generic Enemy Class. Will need simple weapon and AI class
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.steeringBehavior = steeringBehavior(self, 400, 360)
        self.target = None
        
        self.coll_damage = 10
        self.suicide = False

    def setTarget(self, target):
        self.target = target

    def collisionEffect(self, dt, obj): 
        if obj.tag == ENEMY_PROJECTILE_TAG:
            return
        if obj.tag != PLAYER_PROJECTILE_TAG:
            if (self.suicide):
                self.destroy()
            Playable.collisionEffect(self, dt, obj)
        
        if self.liveflag:
            if obj.tag != ENEMY_TAG:
                self.spawn_particles_on_pos(5,(5,5),200,3,1.1)
        else:
            self.spawn_particles_on_pos(5,(13,13),100,3,2)

    def gotHit(self, damage):
        self.damage(damage)
        if self.isDead():
            self.destroy()

    def destroy(self):
        self.liveflag = 0
        sound = self.sound_dict.get_sound("enemy_death" + str(1+int(3*random())))
        if sound:
            sound.set_volume(0.3)
            sound.fadeout(int(sound.get_length()*1000))
            sound.play()

    def render(self):
        # # Debugging - renders acc and vel vectors.
        # dummy = element_sub(self.pos, self.world.camera.topLeft)
        # draw.line(self.world.screen,(0,200,0), dummy, element_add(dummy, self.vel), 2)
        # draw.line(self.world.screen,(200,0,0), dummy, element_add(dummy, self.acc), 2)

        super().render()

    def update(self, dt: float, **kwargs):
        self.steeringBehavior.update(dt)
        # self.thruster.update(dt)
        super().update(dt, **kwargs)
        

