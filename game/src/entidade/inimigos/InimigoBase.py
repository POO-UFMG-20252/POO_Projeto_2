import pygame
import math
from entidade import Entidade
from mapa import PATH, ENEMY_SPEED, ENEMY_HP, REWARD, RED, GREEN

class InimigoBase(Entidade):
    def __init__(self, x, y, vida, velocidade, recompensa, cor, nome, tamanho=15, pontos=1):
        super().__init__(x, y)
        self.path_index = 0
        self.hp = vida
        self.max_hp = vida
        self.velocidade = velocidade
        self.recompensa = recompensa
        self.cor = cor
        self.nome = nome
        self.tamanho = tamanho
        self.alive = True
        self.pontos = pontos
    def move(self):
        if self.path_index < len(PATH) - 1:
            target_x, target_y = PATH[self.path_index + 1]
            # Vetor de direção
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            
            if dist < self.velocidade:
                # Chegou no waypoint, vai para o próximo
                self.path_index += 1
            else:
                # Normaliza e move
                self.x += (dx / dist) * self.velocidade
                self.y += (dy / dist) * self.velocidade
        else:
            # Chegou ao fim do caminho
            return True # Retorna True se causou dano ao jogador
        return False

    def update(self):
        return self.move()

    def draw(self, screen):
        # Desenha o inimigo
        pygame.draw.circle(screen, self.cor, (int(self.x), int(self.y)), self.tamanho)
        
        # Barra de vida
        ratio = self.hp / self.max_hp
        barra_width = self.tamanho * 2
        pygame.draw.rect(screen, RED, (self.x - barra_width//2, self.y - self.tamanho - 10, barra_width, 5))
        pygame.draw.rect(screen, GREEN, (self.x - barra_width//2, self.y - self.tamanho - 10, barra_width * ratio, 5))
        
        # Nome do inimigo (opcional)
        if self.tamanho > 15:  # Só mostra nome em inimigos maiores
            font = pygame.font.SysFont(None, 16)
            nome_texto = font.render(self.nome, True, (255, 255, 255))
            screen.blit(nome_texto, (self.x - nome_texto.get_width()//2, self.y - self.tamanho - 25))
    
    def tomar_dano(self, dano):
        self.hp -= dano
        if self.hp <= 0:
            self.alive = False
            self.ativo = False
    
    def esta_ativo(self):
        return self.ativo and self.alive

    def get_info(self):
        """Retorna informações do inimigo"""
        return {
            "nome": self.nome,
            "vida": self.hp,
            "velocidade": self.velocidade,
            "recompensa": self.recompensa
        }