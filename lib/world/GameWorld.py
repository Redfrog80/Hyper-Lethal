import pygame
from pygame import Vector2, Surface, Rect

import random
import threading

from lib.misc import *
from lib.managers import *
from lib.objects import *

def check_out_of_bound(boundary, obj):
    b = boundary
    return (obj.top < b.top,
            obj.left < b.left,
            obj.bottom > b.bottom,
            obj.right > b.right)

def chance(c):
    """in percentage"""
    return random.randint(0, 100) < c

def randist(center, d_range, world_dim):
    """
    :param center: tuple of obj pos
    :param d_range: min and max dis from obj
    :param world_dim: tuple of world dimension
    :return: tuple x and y of new pos
    """
    while True:
        out = random.randint(0, world_dim[0]), random.randint(0, world_dim[1])
        if d_range[0] <= magnitude(element_sub(center, out)) <= d_range[1]:
            return out


class GameWorld:
    
    def __init__(self, **kwargs) -> None:
        self.__dim__ = kwargs.get("dimensions") or Rect((0,0),(500,500))
        self.__tiledim__ = kwargs.get("tile_dim") or (60, 60)
        self.__game_objects__ = {}
        self.__mouse_area__ = kwargs.get("mouse_area")
        self.__addlist__ = []
        self.__garbage__ = []
        self.__collided_pairs__ = {}
        
        self.__no_collide_tags__ =[PARTICLE_TAG, CAMERA_TAG, TURRET_TAG, CURSOR_TAG]
        self.__no_self_collide_tags__ = [ENEMY_TAG, PLAYER_PROJECTILE_TAG, ENEMY_PROJECTILE_TAG]
        self.__max_count__ = {ENEMY_TAG: 1000,
                              PLAYER_PROJECTILE_TAG: 1000,
                              ENEMY_PROJECTILE_TAG: 300,
                              PARTICLE_TAG: 200} 
        
        self.image_dict = kwargs.get("image_dict") or imageDict("resources/images/")
        self.sound_dict = kwargs.get("sound_dictionary") or soundDict("resources/sounds/")
        
        self.screen = kwargs.get("screen")
        self.player = kwargs.get("player") or Player(pos = Vector2(self.__dim__.center),
                                                     image_dict = self.image_dict,
                                                     sound_dict = self.sound_dict)

        self.camera = kwargs.get("camera") or Camera(name = "camera",
                                                     tag = CAMERA_TAG,
                                                     world = self,
                                                     screen_dim = self.screen.get_size(),
                                                     image_dict = self.image_dict)
        
        self.cursor = cursor(world = self)
        
        self.set_player(self.player)
        self.set_tracked_object(self.player, 40)
        
        self.tileMap = {}
        self.display_tile_map = kwargs.get("debug") or False
        
        self.border_behavior = self.border_default

    def __update_tile_map__(self):
        self.tileMap.clear()
            
        def process_tag(tag):
            if tag not in self.__no_collide_tags__:
                for obj in self.__game_objects__[tag]:
                    topLeft, bottomRight = [element_floor_div(i, self.__tiledim__) for i in
                                            [obj.topLeft, obj.bottomRight]]
                    for tup in [(i, j) for i in range(topLeft[0], bottomRight[0] + 1) for j in
                                range(topLeft[1], bottomRight[1] + 1)]:
                        self.tileMap[tup] = self.tileMap.get(tup,[])
                        self.tileMap[tup].append(obj)
        
        threads = []
        for tag in self.__game_objects__:
            threads.append(threading.Thread(target=process_tag, args=(tag,)).run())
        for thread in threads:
            if thread:
                thread.join()
    

    def __get_collided_pairs__(self):
        self.__collided_pairs__.clear()
        
        def process_coll_pairs_fine(tile):
            for other_object in self.tileMap[tile]:
                if obj.tag != other_object.tag or obj.tag not in self.__no_self_collide_tags__:
                    if obj != other_object and obj.collide_circle(other_object):
                        if not self.__collided_pairs__.get(other_object):
                            self.__collided_pairs__[obj] = [obj, other_object]
        def process_coll_pairs_lazy(tile):
                for other_object in self.tileMap[tile]:
                    if obj.tag != other_object.tag or obj.tag not in self.__no_self_collide_tags__:
                        if obj != other_object and obj.collide_box(other_object):
                            if not self.__collided_pairs__.get(other_object):
                                self.__collided_pairs__[obj] = [obj, other_object]
        
        threads = []
        for tile in self.tileMap:
            size = len(self.tileMap[tile])
            lazy = size > 20
            crammed = size > 50
            if not crammed:
                target = process_coll_pairs_lazy if lazy else process_coll_pairs_fine
                for obj in self.tileMap[tile]:
                    threads.append(threading.Thread(target=target, args=(tile,)).run())
        for thread in threads:
            if thread:
                thread.join()

    def __garbage_collection__(self):
        while len(self.__garbage__):
            obj = self.__garbage__.pop()
            if self.__game_objects__.get(obj.tag, {}).get(obj):
                del self.__game_objects__[obj.tag][obj]

    def get_scaled_mouse_pos(self):
        return element_mul(self.screen.get_size(), element_div(pygame.mouse.get_pos(), self.__mouse_area__))
    
    def get_player(self):
        return self.player
    
    def border_default(self, dt, obj: GameObject):
        if obj.tag in (PLAYER_PROJECTILE_TAG, ENEMY_PROJECTILE_TAG):
            # remove bullet when leave game world
            bb = self.__dim__.copy()
            bounds = check_out_of_bound(bb, obj)
            if True in bounds:
                obj.destroy()
        elif obj.tag == "camera":
            b = self.__dim__
            bounds = check_out_of_bound(b, obj)
            if bounds[0]:
                obj.set_pos(obj.pos + Vector2(0,b.top - obj.top))
            if bounds[1]:
                obj.set_pos(obj.pos + Vector2(b.left - obj.left,0))
            if bounds[2]:
                obj.set_pos(obj.pos + Vector2(0,b.bottom - obj.bottom))
            if bounds[3]:
                obj.set_pos(obj.pos + Vector2(b.right - obj.right,0))
        else:
            b = self.__dim__
            bounds = check_out_of_bound(b, obj)

            if bounds[0]:
                obj.set_pos(obj.pos + Vector2(0,b.top - obj.top))
                obj.vel = Vector2(obj.vel.x, -obj.vel.y)
            if bounds[1]:
                obj.set_pos(obj.pos + Vector2(b.left - obj.left,0))
                obj.vel = Vector2(-obj.vel.x, obj.vel.y)
            if bounds[2]:
                obj.set_pos(obj.pos + (0,b.bottom - obj.bottom))
                obj.vel = Vector2(obj.vel.x, -obj.vel.y)
            if bounds[3]:
                obj.set_pos(obj.pos + Vector2(b.right - obj.right,0))
                obj.vel = Vector2(-obj.vel.x, obj.vel.y)

    def set_player(self, player):
        self.player = player
        self.add_game_object(player)

    def add_game_object(self, obj: GameObject):
        max = self.__max_count__.get(obj.tag)
        if self.__game_objects__.get(obj.tag):
            if not max or len(self.__game_objects__[obj.tag]) < max:
                self.__game_objects__[obj.tag][obj] = obj.name
                obj.set_world(self)
        else:
                self.__game_objects__[obj.tag] = {obj : obj.name}
                obj.set_world(self)

    def __add_from_addlist__(self):
        while len(self.__addlist__):
            self.add_game_object(self.__addlist__.pop())

    def delete_game_object(self, obj: GameObject):
        self.__garbage__.append(obj)

    def delete_if_dead(self, obj):
        if obj and not obj.liveflag:
            self.delete_game_object(obj)

    def set_tracked_object(self, obj, follow_distance):
        self.camera.follow_config(obj, follow_distance)
    
    def set_tile_dim(self, tile_dim: tuple):
        self.__tiledim__ = tile_dim

    # args will be functions which we want to apply to every obj, but we don't want in our obj classes
    def update(self, dt: float, *args):
        
        self.__add_from_addlist__()

        def process_tag(obj):
            for obj in self.__game_objects__[tag]:
                obj.update(dt=dt)
                self.border_behavior(dt, obj)
                self.delete_if_dead(obj)

        threads = []
        for tag in self.__game_objects__:
            threads.append(threading.Thread(target=process_tag, args=(tag,)).run())
        for thread in threads:
            if thread:
                thread.join()            
        
        self.camera.update(dt)
        self.cursor.update(dt)
        
        self.__garbage_collection__()
        self.__update_tile_map__()
        self.__get_collided_pairs__()

        for pair in self.__collided_pairs__:
            obj_a, obj_b = self.__collided_pairs__[pair]
            obj_a.collisionEffect(dt, obj_b)
            obj_b.collisionEffect(dt, obj_a)

    def render(self, **kwargs):
        if self.display_tile_map:
            self.render_tile_map()
        
        self.cursor.render()
        
        for key in self.__game_objects__:
            for obj in self.__game_objects__[key]:
                obj.render()
    
    def render_tile_map(self):
        for tile in self.tileMap:
            self.screen.fill((tile[0] * 4 % 200 + 55, 55, tile[1] * 4 % 200 + 55),
                                 Rect(element_sub(element_mul(tile, self.__tiledim__), self.camera.topLeft), self.__tiledim__))

    def spawnObj(self, prop, num_range, obj_class, tag):
        """
        build on top of adding obj but allow number and probability and random location spawn
        """
        if chance(prop):
            for _ in range(random.randint(*num_range)):
                new_obj = obj_class(name = ENEMY_TAG + tag,
                                    tag = tag,
                                    pos= Vector2(randist(self.player.pos, (600, 1200), self.__dim__.size)),
                                    image_dict = self.image_dict,
                                    sound_dict = self.sound_dict,
                                    world = self)
                if new_obj.tag == ENEMY_TAG:
                    new_obj.setTarget(self.player)
                self.__addlist__.append(new_obj)
                
