import pygame
import math
from entidade import Entidade
from mapa import BULLET_SPEED, YELLOW

class ProjetilBase(Entidade):
    def __init__(self, x, y, target, dano):
        super().__init__(x, y)
        self.target = target
        self.speed = BULLET_SPEED
        self.dano = dano  
        self.cor = YELLOW

    def update(self):
        if not self.target.esta_ativo():
            self.ativo = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.target.tomar_dano(self.dano)
            self.ativo = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), 5)