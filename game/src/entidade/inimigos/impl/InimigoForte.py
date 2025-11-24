from entidade.inimigos.InimigoBase import InimigoBase
from mapa import PATH, ENEMY_SPEED, ENEMY_HP, REWARD
import pygame

class InimigoForte(InimigoBase):
    def __init__(self):
        super().__init__(
            x=PATH[0][0],
            y=PATH[0][1],
            vida=int(ENEMY_HP * 3.5),  # 150% mais vida
            velocidade=ENEMY_SPEED * 0.6,  # 40% mais devagar
            recompensa=int(REWARD * 2),  # 100% mais recompensa
            cor=(128, 0, 128),  # Roxo
            nome="Boss",
            tamanho=20,
            pontos = 3
        )

    def draw(self, screen):
        """Desenha o inimigo forte com visual diferenciado"""
        # Corpo principal maior
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
        
        # Detalhes para parecer mais "forte"
        pygame.draw.circle(screen, (100, 0, 100), (int(self.x), int(self.y)), self.tamanho - 5)
        
        # Barra de vida mais destacada
        ratio = self.hp / self.max_hp
        barra_width = self.tamanho * 2
        barra_height = 6
        
        # Fundo da barra
        pygame.draw.rect(screen, (100, 0, 0), (self.x - barra_width//2, self.y - self.tamanho - 15, barra_width, barra_height))
        # Vida atual
        pygame.draw.rect(screen, (0, 200, 0), (self.x - barra_width//2, self.y - self.tamanho - 15, barra_width * ratio, barra_height))
        
        # Nome
        font = pygame.font.SysFont(None, 18)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width()//2, self.y - self.tamanho - 30))