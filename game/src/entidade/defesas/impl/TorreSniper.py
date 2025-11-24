import pygame
from entidade.defesas.DefesaBase import TorreBase
from mapa import BLACK, TOWER_RANGE, BULLET_DAMAGE, TOWER_COOLDOWN

class TorreSniper(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=int(TOWER_RANGE * 1.5),  # Maior alcance
            cooldown=TOWER_COOLDOWN * 3,  # Atira mais devagar
            dano=BULLET_DAMAGE * 3,  # Dano triplicado
            custo=100,
            cor=BLACK,
            nome="Torre Sniper"
        )

    def draw(self, screen):
        """Desenha a torre sniper com visual diferenciado"""
        # Base triangular para diferenciar
        pontos = [
            (self.x, self.y - 20),  # Topo
            (self.x - 15, self.y + 15),  # Esquerda inferior
            (self.x + 15, self.y + 15)   # Direita inferior
        ]
        pygame.draw.polygon(screen, self.cor, pontos)
        
        # Alcance
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cor_alcance = (*self.cor[:3], 30)
        pygame.draw.circle(surface, cor_alcance, (self.x, self.y), self.alcance)
        screen.blit(surface, (0, 0))
        
        # Nome
        font = pygame.font.SysFont(None, 20)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width() // 2, self.y - 40))