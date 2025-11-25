from entidade.inimigos.InimigoBase import InimigoBase
from config import PATH, ENEMY_SPEED, ENEMY_HP, REWARD
import pygame

class InimigoForte(InimigoBase):
    def __init__(self):
        super().__init__(
            x=PATH[0][0],
            y=PATH[0][1],
            vida=int(ENEMY_HP * 5),
            velocidade=ENEMY_SPEED * 0.6,  
            recompensa=int(REWARD * 2),
            cor=(128, 0, 128),
            nome="Boss",
            tamanho=20,
            pontos = 3
        )

    def draw(self, screen):
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
        pygame.draw.circle(screen, (100, 0, 100), (int(self.x), int(self.y)), self.tamanho - 5)
        
        ratio = self.hp / self.max_hp
        barra_width = self.tamanho * 2
        barra_height = 6
        pygame.draw.rect(screen, (100, 0, 0), (self.x - barra_width//2, self.y - self.tamanho - 15, barra_width, barra_height))
        pygame.draw.rect(screen, (0, 200, 0), (self.x - barra_width//2, self.y - self.tamanho - 15, barra_width * ratio, barra_height))
        
        font = pygame.font.SysFont(None, 18)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width()//2, self.y - self.tamanho - 30))