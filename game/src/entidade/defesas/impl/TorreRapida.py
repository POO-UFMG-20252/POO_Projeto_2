import pygame
from entidade.defesas.DefesaBase import TorreBase
from mapa import YELLOW, TOWER_RANGE, BULLET_DAMAGE, TOWER_COOLDOWN

class TorreRapida(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=int(TOWER_RANGE * 0.8),  # Alcance menor
            cooldown=TOWER_COOLDOWN // 2,  # Atira mais rápido
            dano=BULLET_DAMAGE // 2,  # Dano reduzido
            custo=75,
            cor=YELLOW,
            nome="Torre Rápida"
        )

    def draw(self, screen):
        """Desenha a torre rápida com visual diferenciado"""
        # Formato circular para diferenciar
        pygame.draw.circle(screen, self.cor, (self.x, self.y), 18)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 10)
        
        # Alcance
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cor_alcance = (*self.cor[:3], 30)
        pygame.draw.circle(surface, cor_alcance, (self.x, self.y), self.alcance)
        screen.blit(surface, (0, 0))
        
        # Nome
        font = pygame.font.SysFont(None, 20)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width() // 2, self.y - 40))