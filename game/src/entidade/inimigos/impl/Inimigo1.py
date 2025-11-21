import pygame
import sys
from..InimigoBase import *
ENTITY_COLOR1 = (200, 200, 255)
class inimigo1(Enemy):
    def __init__(self, x, y, speed=3):
        super().vida = 100
        super().armor = 10
        self.speed = speed


        self.color = ENTITY_COLOR1
