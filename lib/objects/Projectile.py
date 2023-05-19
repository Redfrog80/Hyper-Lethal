
from ..misc import *
from .GameObject import GameObject

from pygame import Vector2, image, surface, transform

import math

class Projectile(GameObject):
    def __init__(self, **kwargs):
        
        kwargs["texture_name"] = kwargs.get("texture_name") or "bullet1"
        
        super().__init__(**kwargs)
        
        self.damage = kwargs.get("damage") or 10
        self.velocity = kwargs.get("velocity") or 200
        self.life = kwargs.get("life") or 10
        self.total_life = self.life

    def traj(self, pos: Vector2, gun_velocity: Vector2, speed: float, rot: float, speed_amp: float):
        self.rot = rot
        self.set_pos(pos)
        self.vel = gun_velocity + Vector2(-speed * math.sin(math.radians(self.rot)) * speed_amp,
                                    -speed * math.cos(math.radians(self.rot)) * speed_amp)

    def collisionEffect(self, dt, obj):
        if (obj.tag == PLAYER_TAG and self.tag == ENEMY_PROJECTILE_TAG) or\
           (obj.tag == ENEMY_TAG and self.tag == PLAYER_PROJECTILE_TAG):
            self.spawn_particles_on_pos(10,(7,7),100,1,1)
            obj.damage(self.damage)
            self.destroy()

    def update(self, dt: float, **kwargs):
        super().update(dt, **kwargs)

        self.life -= dt
        if self.life < 0:
            self.destroy()

    def render(self):
        if self.collide_box(self.world.camera):  # render when object collide with camera view
            img0 = transform.rotate(self.texture, self.rot)
            img1 = transform.scale_by(img0, abs(self.life / self.total_life))
            dummy = Vector2(img1.get_size()) / 2
            self.world.screen.blit(img1, (self.pos - self.world.camera.topLeft - dummy).xy)
