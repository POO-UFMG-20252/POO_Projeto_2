# Cores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
DARK_GREEN = (0, 99, 29)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)
PATH_COLOR = (180, 160, 140)
ORANGE = (252, 75, 8)

# Configurações da Tela
WIDTH, HEIGHT = 800, 600

# Configurações de Jogo
ENEMY_SPEED = 2
ENEMY_HP = 15
REWARD = 5
TOWER_COST = 50
TOWER_RANGE = 150
TOWER_COOLDOWN = 30  # Frames entre tiros
BULLET_SPEED = 7
BULLET_DAMAGE = 5

# Caminho (Waypoints) - Pontos por onde os inimigos passarão
PATH = [
    (0, 100), (200, 100), (200, 400), (500, 400), (500, 150), 
    (700, 150), (700, 500), (800, 500)
]

# Pontos onde podemos colocar torres
TORRES = [
    (150, 150),
    (250, 250),
    (150, 350),
    (350, 350),
    (450, 250),
    (250, 450),
    (450, 450),
    (550, 350),
    (650, 250),
    (750, 250),
    (750, 350),
    (750, 450),
    (650, 100),
    (550, 100)
]
