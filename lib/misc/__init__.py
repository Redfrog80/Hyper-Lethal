# utility function
from math import *

from .tags import *

def lerp(a,b,t):
    return a + t*(b-a)

def sign(p):
    return 1 if (p>=0) else -1

def element_add(p:tuple, q:tuple):
        return tuple(px + qx for px, qx in zip(p, q))
    
def element_sub(p:tuple, q:tuple):
    return tuple(px - qx for px, qx in zip(p, q))

def element_mul(p:tuple, q:tuple):
    return tuple(px * qx for px, qx in zip(p, q))

def element_div(p:tuple, q:tuple):
    return tuple(px / qx for px, qx in zip(p, q))

def element_floor_div(p:tuple, q:tuple):
    return tuple(px // qx for px, qx in zip(p, q))

def element_int(p: tuple):
    return tuple(int(px) for px in p)

def element_inv(p: tuple):
    return tuple(1/px for px in p)

def magnitude(p: tuple):
    return dist((0,0),p)

def dot_product(p: tuple, q: tuple):
    return sum(px * qx for px, qx in zip(p, q))

def element_abs(p: tuple):
    return tuple(abs(px) for px in p)

def scalar_div(p:tuple, q:float):
    return tuple(px/q for px in p)

def scalar_floor_div(p:tuple, q:float):
    return tuple(px//q for px in p)

def scalar_mul(p:tuple,q:float):
    return tuple(px*q for px in p)

def unit_tuple1(p: tuple)->bool:
    mag = magnitude(p)
    if (mag):
        return scalar_div(p,mag)
    else:
        return (0,0)
    
def unit_tuple2(p: tuple, q: tuple)->bool:
    mag = dist(p, q)
    delta = element_sub(p, q)
    if (mag):
        return scalar_div(delta,mag)
    else:
        return (0,0)