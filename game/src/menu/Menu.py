import pygame
from mapa import *
from database.Database import Database

class Menu:
    def __init__(self, screen, database: Database):
        self.screen = screen
        self.database = database
        
        self.font_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_normal = pygame.font.SysFont("Arial", 32)
        self.font_pequena = pygame.font.SysFont("Arial", 24)
        self.font_ranking = pygame.font.SysFont("Arial", 20)
        
        self.nome_jogador = ""
        self.input_ativo = True
        self.cursor_visivel = True
        self.cursor_timer = 0
        self.cursor_intervalo = 30  # frames para piscar o cursor
        
        # Cores do menu
        self.cor_fundo = (30, 30, 60)
        self.cor_titulo = (255, 215, 0)
        self.cor_texto = (255, 255, 255)
        self.cor_input = (50, 50, 80)
        self.cor_input_ativo = (70, 70, 100)
        self.cor_botao = (0, 150, 0)
        self.cor_botao_hover = (0, 200, 0)
        
        # Estado do botão
        self.botao_rect = pygame.Rect(0, 0, 250, 50)
        self.botao_hover = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair"
            
            if event.type == pygame.KEYDOWN:
                if self.input_ativo:
                    if event.key == pygame.K_RETURN:
                        if self.nome_jogador.strip():  # Só permite se tiver nome
                            return "iniciar"
                    elif event.key == pygame.K_BACKSPACE:
                        self.nome_jogador = self.nome_jogador[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return "sair"
                    else:
                        # Limita o tamanho do nome e aceita apenas caracteres alfanuméricos
                        if len(self.nome_jogador) < 15 and event.unicode.isprintable():
                            self.nome_jogador += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_rect.collidepoint(event.pos):
                    if self.nome_jogador.strip():
                        return "iniciar"
        
        return "menu"

    def update(self):
        # Atualiza o cursor piscante
        self.cursor_timer += 1
        if self.cursor_timer >= self.cursor_intervalo:
            self.cursor_visivel = not self.cursor_visivel
            self.cursor_timer = 0
        
        # Verifica hover do botão
        mouse_pos = pygame.mouse.get_pos()
        self.botao_hover = self.botao_rect.collidepoint(mouse_pos)

    def draw(self):
        # Fundo gradiente
        self.screen.fill(self.cor_fundo)
        
        # Desenha alguns elementos decorativos
        self._draw_background_elements()
        
        # Título do jogo
        titulo = self.font_titulo.render("TOWER DEFENSE", True, self.cor_titulo)
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(titulo, titulo_rect)
        
        # Instrução
        instrucao = self.font_normal.render("Digite seu nome:", True, self.cor_texto)
        instrucao_rect = instrucao.get_rect(center=(WIDTH // 2, HEIGHT - 225))
        self.screen.blit(instrucao, instrucao_rect)
        
        # Ranking
        self._draw_ranking()
                
        # Campo de input
        input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 200, 300, 50)
        cor_input = self.cor_input_ativo if self.input_ativo else self.cor_input
        pygame.draw.rect(self.screen, cor_input, input_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.cor_texto, input_rect, 2, border_radius=10)
        
        # Texto do nome
        nome_texto = self.font_normal.render(self.nome_jogador, True, self.cor_texto)
        nome_rect = nome_texto.get_rect(midleft=(input_rect.left + 10, input_rect.centery))
        self.screen.blit(nome_texto, nome_rect)
        
        # Cursor piscante
        if self.input_ativo and self.cursor_visivel:
            cursor_x = nome_rect.right + 2
            cursor_rect = pygame.Rect(cursor_x, input_rect.centery - 15, 2, 30)
            pygame.draw.rect(self.screen, self.cor_texto, cursor_rect)
        
        # Botão de iniciar
        self.botao_rect.center = (WIDTH // 2, HEIGHT - 100)
        cor_botao = self.cor_botao_hover if self.botao_hover else self.cor_botao
        pygame.draw.rect(self.screen, cor_botao, self.botao_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.cor_texto, self.botao_rect, 2, border_radius=15)
        
        texto_botao = self.font_normal.render("INICIAR JOGO", True, self.cor_texto)
        texto_botao_rect = texto_botao.get_rect(center=self.botao_rect.center)
        self.screen.blit(texto_botao, texto_botao_rect)
        
        # Texto de instruções adicionais
        #if not self.nome_jogador.strip():
        #    aviso = self.font_pequena.render("Digite um nome para continuar", True, (255, 100, 100))
        #    aviso_rect = aviso.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        #    self.screen.blit(aviso, aviso_rect)
        
        instrucoes = self.font_pequena.render("Pressione ESC para sair", True, (200, 200, 200))
        instrucoes_rect = instrucoes.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(instrucoes, instrucoes_rect)

    def _draw_ranking(self):
        # 01 - Nome - Wave 000 - 000 Pontos
        linhas = []
        
        cont = 0
        for jogador in self.database.obter_top_10():
            linhas.append(f"{str(cont+1).zfill(2)} - {jogador[0]} - Wave {str(jogador[2]).zfill(3)} - {str(jogador[1]).zfill(3)} Pontos")
            cont = cont + 1
        
        #while (cont < 10):
        #    linhas.append(f"{str(cont+1).zfill(2)} - XXXX - Wave XXX - XXX Pontos")
        #    cont = cont + 1
        
        ranking_height = 100
        ranking = self.font_normal.render("RANKING", True, self.cor_texto)
        ranking_rect = ranking.get_rect(center=(WIDTH // 2, ranking_height))
        self.screen.blit(ranking, ranking_rect)

        ranking_height = 125
        cont = 1
        for linha in linhas:
            texto = self.font_ranking.render(linha, True, self.cor_texto)
            texto_rect = texto.get_rect(center=(WIDTH // 2, ranking_height + 20 * cont))
            self.screen.blit(
                texto,
                texto_rect
            )
            cont += 1

    def _draw_background_elements(self):
        """Desenha elementos decorativos de fundo"""
        # Torres decorativas
        for i in range(4):
            x = 100 + i * 200
            y = 100
            pygame.draw.rect(self.screen, BLUE, (x-15, y-15, 30, 30))
            pygame.draw.rect(self.screen, (100, 100, 255), (x-10, y-10, 20, 20))
        
        # Inimigos decorativos
        for i in range(4):
            x = 150 + i * 150
            y = HEIGHT - 100
            pygame.draw.circle(self.screen, RED, (x, y), 12)
            pygame.draw.circle(self.screen, (200, 50, 50), (x, y), 8)

    def get_nome_jogador(self):
        return self.nome_jogador.strip() if self.nome_jogador.strip() else "Jogador"