import pygame
import math
import os
import sys
from config import *
from entidade.inimigos.impl import InimigoNormal, InimigoRapido, InimigoForte
from entidade.inimigos import Onda
from entidade.defesas.impl import TorreNormal, TorreSniper, TorreRapida
from menu.Menu import Menu
from database.Database import Database
from player import Player

class Jogo:
    def __init__(self, nome_jogador: str, database: Database):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"Tower Defense - {nome_jogador}")
        self.clock = pygame.time.Clock()
        
        self.nome_jogador = nome_jogador
        
        self.player = Player(vida=10, dinheiro=120, inimigos_eliminados=0)
        
        self.db = database
        
        self.inimigos = []
        self.torres = []
        self.projeteis = []
        
        self.vidas = 10
        self.dinheiro = 120
        self.wave_timer = 0
        self.game_over = False
        self.running = True
        self.pontuacao_salva = False 
        
        self.wave_atual = 1
        self.onda = Onda(self.wave_atual)
        self.tempo_entre_waves = 180
        self.wave_timer = 0
        self.aguardando_proxima_wave = False
        
        self.font = pygame.font.SysFont("Arial", 24)
        self.font_pequena = pygame.font.SysFont("Arial", 18)
        self.mostrar_leaderboard = False
        
        self.tipos_torres = [
            {"classe": TorreNormal, "nome": "Normal", "custo": 50, "cor": BLUE},
            {"classe": TorreRapida, "nome": "Rápida", "custo": 75, "cor": YELLOW},
            {"classe": TorreSniper, "nome": "Sniper", "custo": 100, "cor": BLACK},
        ]
        self.torre_selecionada = 0
        
        print(f" Jogo iniciado para: {nome_jogador}")
        print(f" Pontuação inicial: {self.player.pontuacao}")
    
    def handle_events(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONUP and not self.game_over:
                if event.button == 1:
                    self.construir_torre()
                elif event.button == 3:
                    self.mudar_tipo_torre()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.torre_selecionada = 0
                elif event.key == pygame.K_2:
                    self.torre_selecionada = 1
                elif event.key == pygame.K_3:
                    self.torre_selecionada = 2
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                
    def construir_torre(self):
        mx, my = pygame.mouse.get_pos()
        tipo_torre = self.tipos_torres[self.torre_selecionada]
        
        if self.dinheiro >= tipo_torre["custo"]:
            torre = tipo_torre["classe"](mx, my)
            self.torres.append(torre)
            self.dinheiro -= tipo_torre["custo"]
            self.player.gastar_dinheiro(tipo_torre["custo"])
            print(f"Torre {tipo_torre['nome']} construída por {self.nome_jogador}!")
        else:
            print(f"Dinheiro insuficiente! Necessário: ${tipo_torre['custo']}")
    
    def mudar_tipo_torre(self):
        self.torre_selecionada = (self.torre_selecionada + 1) % len(self.tipos_torres)
        tipo_atual = self.tipos_torres[self.torre_selecionada]
        print(f"Torre selecionada: {tipo_atual['nome']} (Custo: ${tipo_atual['custo']})")
    
    def update(self):
        if not self.game_over:
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
                    print(f" Wave {self.wave_atual} iniciada!")
            
            inimigos_novos = self.onda.update()
            for inimigo in inimigos_novos:
                self.inimigos.append(inimigo)

            for torre in self.torres:
                torre.update(self.inimigos, self.projeteis)

            for projetil in self.projeteis[:]:
                projetil.update()
                if not projetil.esta_ativo():
                    self.projeteis.remove(projetil)

            for inimigo in self.inimigos[:]:
                dano_jogador = inimigo.update()
                
                if dano_jogador:
                    self.vidas -= 1
                    self.player.receber_dano(1)
                    self.inimigos.remove(inimigo)
                    
                    if self.vidas <= 0:
                        self.game_over = True
                        self.salvar_pontuacao_final()
                
                elif not inimigo.esta_ativo():
                    self.dinheiro += inimigo.recompensa
                    self.player.adicionar_dinheiro(inimigo.recompensa)
                    
                    self.player.adicionar_pontuacao(inimigo.pontos)
                    self.player.adicionar_inimigo(1)
                    self.inimigos.remove(inimigo)
        else:
            if not self.pontuacao_salva:
                self.salvar_pontuacao_final()
    
    def salvar_pontuacao_final(self):
        if not self.pontuacao_salva:
            print("\n" + "="*50)
            print(f" GAME OVER - {self.nome_jogador}")
            print("="*50)
            print(f" Pontuação Final: {self.player.pontuacao}")
            print(f" Wave Alcançada: {self.wave_atual}")
            print(f" Dinheiro Final: ${self.dinheiro}")
            print(f" Torres Construídas: {len(self.torres)}")
            print(f" Inimigos Eliminados: {self.player.inimigos_eliminados}")
            print("="*50)
            
            sucesso = self.db.salvar_pontuacao(
                nome_player=self.nome_jogador,
                pontuacao=self.player.pontuacao,
                wave_alcancada=self.wave_atual,
                dinheiro_final=self.dinheiro,
                torres_construidas=len(self.torres),
                inimigos_eliminados=self.player.inimigos_eliminados
            )
            
            if sucesso:
                print(" Pontuação salva no leaderboard!")
                
                top_10 = self.db.obter_top_10()
                if top_10:
                    print("\n TOP 10 LEADERBOARD ")
                    print("-" * 70)
                    for i, (nome, pontos, wave, inimigos, data) in enumerate(top_10, 1):
                        print(f"{i}º. {nome:20s} | {pontos:5d} pts | Wave {wave:2d} | {inimigos:4d} mortes")
                    print("-" * 70)
            
            self.pontuacao_salva = True
    
    def draw(self):
        self.screen.fill(DARK_GREEN)
        
        if len(PATH) > 1:
            pygame.draw.lines(self.screen, PATH_COLOR, False, PATH, 40)
        
        for torre in self.torres:
            torre.draw(self.screen)
            
        for inimigo in self.inimigos:
            inimigo.draw(self.screen)
            
        for projetil in self.projeteis:
            projetil.draw(self.screen)
        
        self.desenhar_ui()

        if self.game_over and self.mostrar_leaderboard:
            self.desenhar_leaderboard()
    
    def desenhar_ui(self):
        money_text = self.font.render(f"Dinheiro: ${self.dinheiro}", True, BLACK)
        lives_text = self.font.render(f"Vidas: {self.vidas}", True, BLACK)
        player_text = self.font_pequena.render(f"Jogador: {self.nome_jogador}", True, BLACK)
        
        pontuacao_text = self.font.render(f"Pontos: {self.player.pontuacao}", True, (255, 215, 0))
        eliminados_text = self.font_pequena.render(f"Eliminados: {self.player.inimigos_eliminados}", True, BLACK)
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(pontuacao_text, (10, 70))
        self.screen.blit(eliminados_text, (10, 100))
        self.screen.blit(player_text, (10, 125))
        
        wave_text = self.font.render(f"Wave: {self.wave_atual}", True, BLACK)
        inimigos_wave_text = self.font.render(f"Próximos Inimigos: {self.onda.inimigos_restantes}", True, BLACK)
        
        self.screen.blit(wave_text, (WIDTH - 230, 10))
        self.screen.blit(inimigos_wave_text, (WIDTH - 230, 40))
        
        if self.aguardando_proxima_wave:
            tempo_restante = ((self.tempo_entre_waves - self.wave_timer) // 60) + 1
            prox_wave_text = self.font.render(f"Próxima wave em: {tempo_restante}s", True, RED)
            self.screen.blit(prox_wave_text, (WIDTH // 2 - 100, 20))

        tipo_atual = self.tipos_torres[self.torre_selecionada]
        torre_text = self.font.render(
            f"Torre: {tipo_atual['nome']} (${tipo_atual['custo']}) - Tecla {self.torre_selecionada + 1}", 
            True, tipo_atual["cor"]
        )
        self.screen.blit(torre_text, (10, HEIGHT - 70))
        
        instrucoes = self.font.render("Clique Esq: Construir | Clique Dir: Mudar Torre | 1,2,3: Selecionar Torre", True, WHITE)
        self.screen.blit(instrucoes, (10, HEIGHT - 40))

        if self.game_over:
            self.desenhar_tela_game_over()
    
    def desenhar_tela_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        titulo = self.font.render("GAME OVER", True, (255, 50, 50))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(titulo, titulo_rect)
        
        stats = [
            f"Jogador: {self.nome_jogador}",
            f" Pontuação Final: {self.player.pontuacao}",
            f" Wave alcançada: {self.wave_atual}",
            f" Inimigos eliminados: {self.player.inimigos_eliminados}",
            f" Dinheiro final: ${self.dinheiro}",
            f" Torres construídas: {len(self.torres)}"
        ]
        
        for i, stat in enumerate(stats):
            texto = self.font.render(stat, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90 + i * 30))
            self.screen.blit(texto, texto_rect)
        
        instrucoes = self.font.render("Pressione ESC para voltar ao menu", True, (200, 200, 200))
        instrucoes_rect = instrucoes.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(instrucoes, instrucoes_rect)

        if not self.mostrar_leaderboard:
            press_enter = self.font.render("Pressione ENTER para ver o ranking", True, (200,200,200))
            press_enter_rect = press_enter.get_rect(center=(WIDTH//2, HEIGHT - 100))
            self.screen.blit(press_enter, press_enter_rect)

    def desenhar_leaderboard(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        self.screen.blit(overlay, (0, 0))

        titulo = self.font.render("TOP 10 - LEADERBOARD", True, (255, 215, 0))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, 80))
        self.screen.blit(titulo, titulo_rect)

        top10 = self.db.obter_top_10()
        if not top10:
            vazio = self.font.render("Nenhum registro ainda.", True, WHITE)
            self.screen.blit(vazio, vazio.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            return

        for i, (nome, pontos, wave, mortes, data) in enumerate(top10, 1):
            linha = f"{i}. {nome:<10}  {pontos:>4} pts   Wave {wave}"
            texto = self.font.render(linha, True, WHITE)
            self.screen.blit(texto, (WIDTH//2 - 180, 140 + i * 30))

        instr = self.font.render("Pressione ENTER para voltar ao menu", True, (200,200,200))
        self.screen.blit(instr, instr.get_rect(center=(WIDTH // 2, HEIGHT - 80)))
    
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower Defense")
    clock = pygame.time.Clock()
    
    running = True
    estado = "menu"
    nome_jogador = "Jogador"
    
    database = Database()
    
    menu = Menu(screen, database)
    jogo = None
    
    while running:
        if estado == "menu":
            resultado = menu.handle_events()
            menu.update()
            menu.draw()
            
            if resultado == "iniciar":
                nome_jogador = menu.get_nome_jogador()
                jogo = Jogo(nome_jogador, database)
                estado = "jogo"
            elif resultado == "sair":
                running = False
        
        elif estado == "jogo":
            if jogo.game_over:
                jogo.draw()  
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and not jogo.mostrar_leaderboard:
                            jogo.mostrar_leaderboard = True

                        elif event.key == pygame.K_RETURN and jogo.mostrar_leaderboard:
                            estado = "menu"
                            jogo = None

                        elif event.key == pygame.K_ESCAPE:
                            estado = "menu"
                            jogo = None
            else:
                jogo.handle_events()
                jogo.update()
                jogo.draw()

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()