import pygame
import math
from entidade import Entidade
from projetil import ProjetilBase

class TorreBase(Entidade):
    def __init__(self, x, y, alcance, cooldown, dano, custo, cor, nome):
        super().__init__(x, y)
        self.alcance = alcance
        self.cooldown_max = cooldown
        self.cooldown = 0
        self.dano = dano
        self.custo = custo
        self.cor = cor
        self.nome = nome
        self.alvo = None

    def update(self, inimigos, projeteis):
        """Atualiza a torre e verifica se pode atacar"""
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        # Encontrar alvo
        self.alvo = self._encontrar_alvo(inimigos)
        
        if self.alvo:
            self.atacar(projeteis)
            self.cooldown = self.cooldown_max

    def _encontrar_alvo(self, inimigos):
        """Encontra o inimigo mais próximo dentro do alcance"""
        alvo = None
        menor_distancia = self.alcance

        for inimigo in inimigos:
            if inimigo.esta_ativo():
                distancia = math.hypot(inimigo.x - self.x, inimigo.y - self.y)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    alvo = inimigo
        
        return alvo

    def atacar(self, projeteis):
        """Método para atacar - deve ser sobrescrito pelas classes filhas"""
        projeteis.append(ProjetilBase(self.x, self.y, self.alvo, self.dano))

    def draw(self, screen):
        """Desenha a torre e seu alcance (opcional)"""
        # Base da torre
        pygame.draw.rect(screen, self.cor, (self.x - 15, self.y - 15, 30, 30))
        
        # Desenhar nome da torre
        font = pygame.font.SysFont(None, 20)
        nome_texto = font.render(self.nome, True, (255, 255, 255))
        screen.blit(nome_texto, (self.x - nome_texto.get_width() // 2, self.y - 35))
        
        # Alcance (transparente)
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cor_alcance = (*self.cor[:3], 30)  # Mesma cor mas transparente
        pygame.draw.circle(surface, cor_alcance, (self.x, self.y), self.alcance)
        screen.blit(surface, (0, 0))

    def get_info(self):
        """Retorna informações da torre para UI"""
        return {
            "nome": self.nome,
            "dano": self.dano,
            "alcance": self.alcance,
            "velocidade_ataque": 60 / self.cooldown_max,  # ataques por segundo
            "custo": self.custo
        }