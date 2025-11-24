from entidade.inimigos.InimigoBase import InimigoBase
from mapa import PATH, ENEMY_SPEED, ENEMY_HP, REWARD
import pygame

class InimigoRapido(InimigoBase):
    def __init__(self):
        super().__init__(
            x=PATH[0][0],
            y=PATH[0][1],
            vida=int(ENEMY_HP * 0.6),  # 40% menos vida
            velocidade=ENEMY_SPEED * 1.8,  # 80% mais rápido
            recompensa=int(REWARD * 1.2),  # 20% mais recompensa
            cor=(255, 165, 0),  # Laranja
            nome="Rápido",
            tamanho=12,
            pontos = 2
        )

    def draw(self, screen):
        """Desenha o inimigo rápido com visual diferenciado"""
        # Corpo principal
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
        
        # Efeito de velocidade (rastro)
        for i in range(1, 4):
            alpha = 100 - (i * 25)
            if self.path_index > 0 and len(PATH) > self.path_index:
                prev_x, prev_y = PATH[self.path_index]
                trail_x = self.x - (self.x - prev_x) * 0.1 * i
                trail_y = self.y - (self.y - prev_y) * 0.1 * i
                surface = pygame.Surface((self.tamanho*2, self.tamanho*2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*self.cor[:3], alpha), (self.tamanho, self.tamanho), self.tamanho * 0.7)
                screen.blit(surface, (trail_x - self.tamanho, trail_y - self.tamanho))
        
        # Barra de vida
        ratio = self.hp / self.max_hp
        barra_width = self.tamanho * 2
        pygame.draw.rect(screen, (200, 0, 0), (self.x - barra_width//2, self.y - self.tamanho - 10, barra_width, 4))
        pygame.draw.rect(screen, (0, 200, 0), (self.x - barra_width//2, self.y - self.tamanho - 10, barra_width * ratio, 4))