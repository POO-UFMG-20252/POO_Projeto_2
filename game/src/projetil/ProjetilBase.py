import pygame
import math
from entidade import EntidadeBase
from config import BULLET_SPEED, YELLOW

class ProjetilBase(EntidadeBase):
    def __init__(self, x, y, target, dano):
        super().__init__(x, y)
        self.__target = target
        self.__speed = BULLET_SPEED
        self.__dano = dano  
        self.__cor = YELLOW

    def update(self):
        if not self.__target.esta_ativo():
            self._ativo = False
            return

        dx = self.__target._x - self._x
        dy = self.__target._y - self._y
        dist = math.hypot(dx, dy)

        if dist < self.__speed:
            self.__target.tomar_dano(self.__dano)
            self._ativo = False
        else:
            self._x += (dx / dist) * self.__speed
            self._y += (dy / dist) * self.__speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.__cor, (int(self._x), int(self._y)), 5)