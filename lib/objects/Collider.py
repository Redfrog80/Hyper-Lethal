from math import dist
from lib.misc import *
from pygame import Vector2

class Collider:
    def __init__(self, **kwargs):
        
        self.pos = kwargs.get("pos") or Vector2()
        self.radius = kwargs.get("radius") or 1
        self.shape = kwargs.get("shape") or Vector2(1,1)
        self.__update__()

    def dist(self, other):
        return self.pos.distance_to(other.pos)
    
    def set_pos(self, pos : Vector2):
        self.pos = pos
        self.__update__()
    
    def __update__(self):
        self.top = int(self.pos.y - self.radius*self.shape.y)
        self.bottom = int(self.pos.y + self.radius*self.shape.y)
        self.left = int(self.pos.x - self.radius*self.shape.x)
        self.right = int(self.pos.x + self.radius*self.shape.x)
        self.topLeft = element_int(self.pos + Vector2(-self.radius*self.shape.x,-self.radius*self.shape.y))
        self.topRight = element_int(self.pos + Vector2(self.radius*self.shape.x,-self.radius*self.shape.y))
        self.bottomLeft = element_int(self.pos + Vector2(-self.radius*self.shape.x,self.radius*self.shape.y))
        self.bottomRight = element_int(self.pos +  Vector2(self.radius*self.shape.x,self.radius*self.shape.y))

    def collide_circle(self, other)->bool:
        mag = self.pos.distance_to(other.pos)
        dif = self.pos - other.pos
        if (mag):
            unit = dif/mag
            a = self.radius*self.shape.x if (self.shape.x==self.shape.y) else (unit*self.radius*self.shape).magnitude()
            b = other.radius*other.shape.x if (other.shape.x==other.shape.y) else (unit*other.radius*other.shape).magnitude()
            return (mag <= (a+b))
        else:
            return True

    def collide_box(self, other)->bool:
        return (self.top <= other.bottom and
                self.bottom >= other.top or
                self.left <= other.right and
                self.right >= other.left)

    def collide_point(self,point: tuple):
        return (dist(self.pos, point) <= self.radius)
    
    def resolve_circle_overlap(self,other):
        mag = self.pos.distance_to(other.pos)
        dif = self.pos - other.pos
        if (mag):
            unit = dif/mag
            a = self.radius*self.shape.x if (self.shape.x==self.shape.y) else (unit*self.radius*self.shape).magnitude()
            b = other.radius*other.shape.x if (other.shape.x==other.shape.y) else (unit*other.radius*other.shape).magnitude()
            self.set_pos(self.pos + unit*((a+b)-mag)/2)
            other.set_pos(other.pos + unit*(-(a+b)+mag)/2)
    
    
    def get_direction(self, other)->bool:
        mag = self.pos.distance_to(other.pos)
        dif = self.pos - other.pos
        if (mag):
            return dif/mag
        else:
            return Vector2(0,0)