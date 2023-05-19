import pygame
from pygame import transform, Vector2
from random import random

from ..misc import *
from ..managers import *
from .Base import Base
from .Particle import ParticleSimple
from ..misc import *

class cursor(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.texture_name = kwargs.get("texture_name") or "cursor2"
        self.image_dict = kwargs.get("image_dict") or imageDict()
        self.sound_dict = kwargs.get("sound_dict") or soundDict()
        
        self.texture = self.image_dict.get_image(self.texture_name) or self.image_dict.load_image("resources/images/" + self.texture_name + ".png")
        
        self.texture_size = kwargs.get("texture_size") or Vector2(16,16)
        self.shape = self.texture_size/4
        self.setTextureSize(self.texture_size.xy)
        

    def setTextureSize(self, size: tuple):
        self.texture = transform.scale(self.texture, size)

    def render(self):
        if self.collide_box(self.world.camera):  # render when object collide with camera view
            dummy = Vector2(self.texture.get_size()) / 2
            self.world.screen.blit(self.texture, (self.pos - self.world.camera.topLeft - dummy).xy)

    def update(self, dt, **kwargs):
        self.set_pos(Vector2(self.world.get_scaled_mouse_pos()) + self.world.camera.topLeft)