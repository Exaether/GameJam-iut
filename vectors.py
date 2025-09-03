# !/usr/bin/env python
# -*- coding:utf-8 -*-

from math import sqrt

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def len(self):
        return sqrt((self.x**2) + (self.y**2))
    
    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y)
    
    def __radd__(self, v):
        return self.__add__(v)
    
    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y)
    
    def __rsub__(self, v):
        return self.__sub__(v)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __mul__(self, v):
        return Vector(self.x*v, self.y*v)
    
    def __rmul__(self, v):
        return self.__mul__(v)
    
    def __truediv__(self, v):
        return Vector(self.x/v, self.y/v)
    
    def __str__(self):
        return f"({self.x}, {self.y})"

