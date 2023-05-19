import pygame
from pygame.locals import *

from lib.world.GameWorld import GameWorld
from lib.objects import *
from lib.misc import *

class EventController:
    """
    use to handle player input and world event
    """
    def __init__(self, game_world: GameWorld) -> None:
        
        self.extraEventList = {}
        self.world = game_world
        self.player = game_world.get_player()
        self.run = True
        self.eventNumber = pygame.USEREVENT

    def update_events(self, dt):
        keys = pygame.key.get_pressed()
        if (keys[K_w] and keys[K_s]):
            self.player.stopAcc()
        elif (keys[K_w]):
            self.player.goForward()
        elif (keys[K_s]):
            self.player.goBack()
        else:
            self.player.stopAcc()

        if (keys[K_a] and keys[K_d]):
            self.player.stopRotVel()
        elif (keys[K_a]):
            self.player.rotateLeft()
        elif (keys[K_d]):
            self.player.rotateRight()
        else:
            self.player.stopRotVel()

        shoot = keys[K_SPACE]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in self.extraEventList:
                data = self.extraEventList[event.type]
                data[0](data[1], data[2], data[3], data[4])

        if shoot and self.player.liveflag:
            self.player.shoot(dt = dt)

        return True

    def addEventSpawn(self, time, chance, num_range, obj_class, tag):
        """
        :param time: time occur in s
        :param chance: probability of something happen 0 - 1
        :param num_range: tuple: lower and upper bound
        :param obj_class: which class to spawn
        :param tag: obj tag
        """
        newEvent = self.eventNumber
        self.eventNumber += 1
        pygame.time.set_timer(newEvent, time * 1000)
        self.extraEventList.update({newEvent: (self.world.spawnObj, chance, num_range, obj_class, tag)})
