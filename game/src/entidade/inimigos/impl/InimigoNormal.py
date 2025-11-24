from entidade.inimigos.InimigoBase import InimigoBase
from mapa import PATH, ENEMY_SPEED, ENEMY_HP, REWARD, RED

class InimigoNormal(InimigoBase):
    def __init__(self):
        super().__init__(
            x=PATH[0][0],
            y=PATH[0][1],
            vida=ENEMY_HP,
            velocidade=ENEMY_SPEED,
            recompensa=REWARD,
            cor=RED,
            nome="Normal",
            tamanho=15
        )