import pygame
from entidade.defesas.TorreBase import TorreBase
from config import BLUE, TOWER_RANGE, TOWER_COOLDOWN, BULLET_DAMAGE

class TorreNormal(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=TOWER_RANGE,
            cooldown=TOWER_COOLDOWN,
            dano=BULLET_DAMAGE,
            custo=50,
            cor=BLUE,
            nome="Torre Normal"
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self._cor, (self.x - 15, self.y - 15, 30, 30))
        
        font = pygame.font.SysFont(None, 20)
        nome_texto = font.render(self._nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self._x - nome_texto.get_width() // 2, self._y - 35))
        
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cor_alcance = (*self._cor[:3], 30)
        pygame.draw.circle(surface, cor_alcance, (self._x, self._y), self._alcance)
        screen.blit(surface, (0, 0))