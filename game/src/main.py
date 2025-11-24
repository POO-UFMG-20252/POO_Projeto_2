import pygame
import math
import os
import sys
from mapa import *
from entidade.inimigos.impl import InimigoNormal, InimigoRapido, InimigoForte
from entidade.inimigos import Onda
from entidade.defesas.impl import TorreNormal, TorreSniper, TorreRapida

# CORREÇÃO: Importe do pacote menu
from menu.Menu import Menu  # Agora importa do pacote menu

class Jogo:
    def __init__(self, nome_jogador="Jogador"):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Tower Defense - {nome_jogador}")
        self.clock = pygame.time.Clock()
        
        self.nome_jogador = nome_jogador
        
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
        self.tempo_entre_waves = 180
        self.wave_timer = 0
        self.aguardando_proxima_wave = False
        
        self.font = pygame.font.SysFont("Arial", 24)
        self.font_pequena = pygame.font.SysFont("Arial", 18)
        
        # Sistema de seleção de torres
        self.tipos_torres = [
            {"classe": TorreNormal, "nome": "Normal", "custo": 50, "cor": BLUE},
            {"classe": TorreRapida, "nome": "Rápida", "custo": 75, "cor": YELLOW},
            {"classe": TorreSniper, "nome": "Sniper", "custo": 100, "cor": BLACK},
        ]
        self.torre_selecionada = 0
    
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
            print(f"Torre {tipo_torre['nome']} construída por {self.nome_jogador}!")
        else:
            print(f"Dinheiro insuficiente! Necessário: ${tipo_torre['custo']}")
    
    def mudar_tipo_torre(self):
        self.torre_selecionada = (self.torre_selecionada + 1) % len(self.tipos_torres)
        tipo_atual = self.tipos_torres[self.torre_selecionada]
        print(f"Torre selecionada: {tipo_atual['nome']} (Custo: ${tipo_atual['custo']})")
    
    def update(self):
        if not self.game_over:
            # Sistema de waves
            if not self.onda.esta_ativa() and not self.aguardando_proxima_wave:
                if len(self.inimigos) == 0:
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
        player_text = self.font_pequena.render(f"Jogador: {self.nome_jogador}", True, BLACK)
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(player_text, (10, 70))
        
        # Info da wave
        wave_text = self.font.render(f"Wave: {self.wave_atual}", True, BLACK)
        inimigos_wave_text = self.font.render(f"Inimigos: {self.onda.inimigos_restantes}", True, BLACK)
        
        self.screen.blit(wave_text, (WIDTH - 150, 10))
        self.screen.blit(inimigos_wave_text, (WIDTH - 150, 40))
        
        if self.aguardando_proxima_wave:
            tempo_restante = ((self.tempo_entre_waves - self.wave_timer) // 60) + 1
            prox_wave_text = self.font.render(f"Próxima wave em: {tempo_restante}s", True, RED)
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
            self.desenhar_tela_game_over()
    
    def desenhar_tela_game_over(self):
        """Desenha a tela de game over personalizada"""
        # Fundo semi-transparente
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        titulo = self.font.render("GAME OVER", True, (255, 50, 50))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(titulo, titulo_rect)
        
        # Estatísticas do jogador
        stats = [
            f"Jogador: {self.nome_jogador}",
            f"Wave alcançada: {self.wave_atual}",
            f"Dinheiro final: ${self.dinheiro}",
            f"Torres construídas: {len(self.torres)}"
        ]
        
        for i, stat in enumerate(stats):
            texto = self.font.render(stat, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60 + i * 30))
            self.screen.blit(texto, texto_rect)
        
        # Instruções para voltar ao menu
        instrucoes = self.font.render("Pressione ESC para voltar ao menu", True, (200, 200, 200))
        instrucoes_rect = instrucoes.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(instrucoes, instrucoes_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()


# Configuração do path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower Defense")
    clock = pygame.time.Clock()
    
    running = True
    estado = "menu"
    nome_jogador = "Jogador"
    
    menu = Menu(screen)  # ← AGORA DEVE FUNCIONAR
    jogo = None
    
    while running:
        if estado == "menu":
            # Menu principal
            resultado = menu.handle_events()
            menu.update()
            menu.draw()
            
            if resultado == "iniciar":
                nome_jogador = menu.get_nome_jogador()
                jogo = Jogo(nome_jogador)
                estado = "jogo"
                print(f"🎮 Jogo iniciado para: {nome_jogador}")
            elif resultado == "sair":
                running = False
        
        elif estado == "jogo":
            # Jogo principal
            jogo.handle_events()
            jogo.update()
            jogo.draw()
            
            # Verifica se o jogo terminou
            if jogo.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            estado = "menu"
                            jogo = None
                            print("↩️ Voltando ao menu...")
            elif not jogo.running:
                running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()