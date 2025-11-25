import pygame
from entidade.defesas.TorreBase import TorreBase
from config import BLACK, TOWER_RANGE, BULLET_DAMAGE, TOWER_COOLDOWN

class TorreSniper(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=int(TOWER_RANGE * 1.5),
            cooldown=TOWER_COOLDOWN * 3,
            dano=BULLET_DAMAGE * 3,
            custo=100,
            cor=BLACK,
            nome="Torre Sniper"
        )

    def draw(self, screen):
        pontos = [
            (self.x, self.y - 20), 
            (self.x - 15, self.y + 15), 
            (self.x + 15, self.y + 15)
        ]
        pygame.draw.polygon(screen, self.cor, pontos)
        
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cor_alcance = (*self.cor[:3], 30)
        pygame.draw.circle(surface, cor_alcance, (self.x, self.y), self.alcance)
        screen.blit(surface, (0, 0))
        
        font = pygame.font.SysFont(None, 20)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width() // 2, self.y - 40))