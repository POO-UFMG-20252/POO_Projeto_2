import pygame
import os
import sys

from config import *
from menu.Menu import Menu
from database.Database import Database
from jogo.Jogo import Jogo

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