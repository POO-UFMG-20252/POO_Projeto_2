import pygame

from entidade.inimigos.InimigoBase import InimigoBase
from config import PATH, ENEMY_SPEED, ENEMY_HP, REWARD, RED, GREEN

class InimigoNormal(InimigoBase):
    def __init__(self):
        super().__init__(
            x=PATH[0][0],
            y=PATH[0][1],
            vida=ENEMY_HP,
            velocidade=ENEMY_SPEED,
            recompensa=REWARD,
            cor=RED,
            nome="Normal",
            tamanho=15,
            pontos = 1
        )
        
    def draw(self, screen):
        pygame.draw.circle(screen, self._cor, (int(self._x), int(self._y)), self._tamanho)
        
        ratio = self._hp / self._max_hp
        barra_width = self._tamanho * 2
        pygame.draw.rect(screen, RED, (self._x - barra_width//2, self._y - self._tamanho - 10, barra_width, 5))
        pygame.draw.rect(screen, GREEN, (self._x - barra_width//2, self._y - self._tamanho - 10, barra_width * ratio, 5))