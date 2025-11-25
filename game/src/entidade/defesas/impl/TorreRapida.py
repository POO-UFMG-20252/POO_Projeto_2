import pygame
from entidade.defesas.TorreBase import TorreBase
from config import YELLOW, TOWER_RANGE, BULLET_DAMAGE, TOWER_COOLDOWN

class TorreRapida(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=int(TOWER_RANGE * 0.8),
            cooldown=TOWER_COOLDOWN // 2,
            dano=BULLET_DAMAGE // 1.3,
            custo=75,
            cor=YELLOW,
            nome="Torre Rápida"
        )

    def draw(self, screen):
        pygame.draw.circle(screen, self.cor, (self.x, self.y), 18)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 10)
        
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cor_alcance = (*self.cor[:3], 30)
        pygame.draw.circle(surface, cor_alcance, (self.x, self.y), self.alcance)
        screen.blit(surface, (0, 0))
        
        font = pygame.font.SysFont(None, 20)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width() // 2, self.y - 40))