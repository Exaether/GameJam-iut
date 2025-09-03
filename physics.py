# !/usr/bin/env python
# -*- coding:utf-8 -*-

from vectors import Vector

G = Vector(0, 10)

def air_frixions(v):
    return v - v/30

def air_and_g(v, weight):
    return air_frixions(v) + G*weight
