import pygame
import math

from entidade.defesas.TorreBase import TorreBase
from config import ORANGE

class TorreVaga(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=25,
            cooldown=-1,
            dano=0,
            custo=0,
            cor=ORANGE,
            nome=""
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self._cor, (self.x - 15, self.y - 15, 30, 30))
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        screen.blit(surface, (0, 0))