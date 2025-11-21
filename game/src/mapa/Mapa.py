import pygame
pygame.init()

COLORS = {
    "G" : (60,200,60), #grama
    "B" : (180,180,180), #tile construivel
    "R" : (110,110,110), # caminho dos inimigos
}
TILE_SIZE = 48 #tamanho de cada parte
MAP = [ #pra modificar/definir o mapa
["G","R","R","R","R","G","G","G","G"],
["G","R","G","G","R","G","G","G","G"],
["R","R","G","G","R","G","R","R","R"],
["G","G","G","G","R","R","R","G","G"],
["G","G","G","G","G","G","G","G","G"],

]
WIDTH = len(MAP[0]) * TILE_SIZE
HEIGHT = len(MAP) * TILE_SIZE

screen = pygame.display.set_mode((WIDTH,HEIGHT)) #criando a tela
clock =  pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for y,row in enumerate(MAP):
            for x,tile in enumerate(row):
                color = COLORS[tile]
                pygame.draw.rect(screen,color,(x*TILE_SIZE,y * TILE_SIZE,TILE_SIZE,TILE_SIZE))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()