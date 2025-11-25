from entidade.inimigos.InimigoBase import InimigoBase
from config import PATH, ENEMY_SPEED, ENEMY_HP, REWARD
import pygame

class InimigoRapido(InimigoBase):
    def __init__(self):
        super().__init__(
            x=PATH[0][0],
            y=PATH[0][1],
            vida=int(ENEMY_HP * 0.6), 
            velocidade=ENEMY_SPEED * 1.8,
            recompensa=int(REWARD * 1.2),
            cor=(255, 165, 0),
            nome="Rápido",
            tamanho=12,
            pontos = 2
        )

    def draw(self, screen):
        pygame.draw.circle(screen, self._cor, (int(self._x), int(self._y)), self._tamanho)
        
        for i in range(1, 4):
            alpha = 100 - (i * 25)
            if self._path_index > 0 and len(PATH) > self._path_index:
                prev_x, prev_y = PATH[self._path_index]
                trail_x = self._x - (self._x - prev_x) * 0.1 * i
                trail_y = self._y - (self._y - prev_y) * 0.1 * i
                surface = pygame.Surface((self._tamanho*2, self._tamanho*2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*self._cor[:3], alpha), (self._tamanho, self._tamanho), self._tamanho * 0.7)
                screen.blit(surface, (trail_x - self._tamanho, trail_y - self._tamanho))
        
        ratio = self._hp / self._max_hp
        barra_width = self._tamanho * 2
        pygame.draw.rect(screen, (200, 0, 0), (self._x - barra_width//2, self._y - self._tamanho - 10, barra_width, 4))
        pygame.draw.rect(screen, (0, 200, 0), (self._x - barra_width//2, self._y - self._tamanho - 10, barra_width * ratio, 4))