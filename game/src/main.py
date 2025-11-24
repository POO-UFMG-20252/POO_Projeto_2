import pygame
import math
import os
import sys
from mapa import *
from entidade.inimigos.impl import InimigoNormal, InimigoRapido, InimigoForte
from entidade.inimigos import Onda
from entidade.defesas.impl import TorreNormal, TorreSniper, TorreRapida

class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tower Defense Simples - Pygame")
        self.clock = pygame.time.Clock()
        
        self.inimigos = []
        self.torres = []
        self.projeteis = []
        
        self.vidas = 10
        self.dinheiro = 120
        self.wave_timer = 0
        self.game_over = False
        self.running = True
        
        self.wave_atual = 1
        self.onda = Onda(self.wave_atual)
        self.tempo_entre_waves = 180  # 3 segundos entre waves
        self.wave_timer = 0
        self.aguardando_proxima_wave = False
        
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Sistema de seleção de torres
        self.tipos_torres = [
            {"classe": TorreNormal, "nome": "Normal", "custo": 50, "cor": BLUE},
            {"classe": TorreRapida, "nome": "Rápida", "custo": 75, "cor": YELLOW},
            {"classe": TorreSniper, "nome": "Sniper", "custo": 100, "cor": BLACK},
        ]
        self.torre_selecionada = 0  # Índice do tipo de torre selecionada
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                if event.button == 1:  # Clique esquerdo - construir
                    self.construir_torre()
                elif event.button == 3:  # Clique direito - mudar tipo de torre
                    self.mudar_tipo_torre()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.torre_selecionada = 0
                elif event.key == pygame.K_2:
                    self.torre_selecionada = 1
                elif event.key == pygame.K_3:
                    self.torre_selecionada = 2
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def construir_torre(self):
        mx, my = pygame.mouse.get_pos()
        tipo_torre = self.tipos_torres[self.torre_selecionada]
        
        if self.dinheiro >= tipo_torre["custo"]:
            torre = tipo_torre["classe"](mx, my)
            self.torres.append(torre)
            self.dinheiro -= tipo_torre["custo"]
            print(f"Torre {tipo_torre['nome']} construída!")
        else:
            print(f"Dinheiro insuficiente! Necessário: ${tipo_torre['custo']}")
    
    def mudar_tipo_torre(self):
        self.torre_selecionada = (self.torre_selecionada + 1) % len(self.tipos_torres)
        tipo_atual = self.tipos_torres[self.torre_selecionada]
        print(f"Torre selecionada: {tipo_atual['nome']} (Custo: ${tipo_atual['custo']})")
    
    def spawn_inimigo(self):
        self.inimigos.append(InimigoBase())
    
    def update(self):
        if not self.game_over:
            # Sistema de waves
            if not self.onda.esta_ativa() and not self.aguardando_proxima_wave:
                if len(self.inimigos) == 0:  # Só começa nova wave quando não há inimigos
                    self.aguardando_proxima_wave = True
                    self.wave_timer = 0
            
            if self.aguardando_proxima_wave:
                self.wave_timer += 1
                if self.wave_timer >= self.tempo_entre_waves:
                    self.wave_atual += 1
                    self.onda = Onda(self.wave_atual)
                    self.aguardando_proxima_wave = False
                    print(f"🏁 Wave {self.wave_atual} iniciada!")
            
            # Spawn de inimigos controlado pela onda
            inimigos_novos = self.onda.update()
            for inimigo in inimigos_novos:
                self.inimigos.append(inimigo)

            # Atualizar Torres
            for torre in self.torres:
                torre.update(self.inimigos, self.projeteis)

            # Atualizar Projéteis
            for projetil in self.projeteis[:]:
                projetil.update()
                if not projetil.esta_ativo():
                    self.projeteis.remove(projetil)

            # Atualizar Inimigos
            for inimigo in self.inimigos[:]:
                dano_jogador = inimigo.update()
                if dano_jogador:
                    self.vidas -= 1
                    self.inimigos.remove(inimigo)
                    if self.vidas <= 0:
                        self.game_over = True
                elif not inimigo.esta_ativo():
                    self.dinheiro += inimigo.recompensa
                    self.inimigos.remove(inimigo)
    
    def draw(self):
        # Fundo (Grama)
        self.screen.fill(GREEN)
        
        # Desenhar Caminho
        if len(PATH) > 1:
            pygame.draw.lines(self.screen, PATH_COLOR, False, PATH, 40)
        
        # Desenhar Torres
        for torre in self.torres:
            torre.draw(self.screen)
            
        # Desenhar Inimigos
        for inimigo in self.inimigos:
            inimigo.draw(self.screen)
            
        # Desenhar Projéteis
        for projetil in self.projeteis:
            projetil.draw(self.screen)
        
        # UI (Interface)
        self.desenhar_ui()
    
    def desenhar_ui(self):
        money_text = self.font.render(f"Dinheiro: ${self.dinheiro}", True, BLACK)
        lives_text = self.font.render(f"Vidas: {self.vidas}", True, BLACK)
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        
        # Info da wave
        wave_text = self.font.render(f"Wave: {self.wave_atual}", True, BLACK)
        inimigos_wave_text = self.font.render(f"Inimigos: {self.onda.inimigos_restantes}", True, BLACK)
        
        self.screen.blit(wave_text, (WIDTH - 150, 10))
        self.screen.blit(inimigos_wave_text, (WIDTH - 150, 40))
        
        if self.aguardando_proxima_wave:
            prox_wave_text = self.font.render(f"Próxima wave em: {((self.tempo_entre_waves - self.wave_timer) // 60) + 1}s", True, RED)
            self.screen.blit(prox_wave_text, (WIDTH // 2 - 100, 20))

        # Info da torre selecionada
        tipo_atual = self.tipos_torres[self.torre_selecionada]
        torre_text = self.font.render(
            f"Torre: {tipo_atual['nome']} (${tipo_atual['custo']}) - Tecla {self.torre_selecionada + 1}", 
            True, tipo_atual["cor"]
        )
        self.screen.blit(torre_text, (10, HEIGHT - 70))
        
        # Instruções
        instrucoes = self.font.render("Clique Esq: Construir | Clique Dir: Mudar Torre | 1,2,3: Selecionar Torre", True, WHITE)
        self.screen.blit(instrucoes, (10, HEIGHT - 40))

        if self.game_over:
            over_text = self.font.render("GAME OVER - Pressione ESC para sair", True, BLACK)
            center_x = WIDTH // 2 - over_text.get_width() // 2
            center_y = HEIGHT // 2 - over_text.get_height() // 2
            pygame.draw.rect(self.screen, RED, (center_x - 20, center_y - 10, over_text.get_width() + 40, over_text.get_height() + 20))
            self.screen.blit(over_text, (center_x, center_y))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        
        
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()