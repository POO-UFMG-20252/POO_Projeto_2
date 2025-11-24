from entidade.defesas.DefesaBase import TorreBase
from mapa import BLUE, TOWER_RANGE, TOWER_COOLDOWN, BULLET_DAMAGE

class TorreNormal(TorreBase):
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y,
            alcance=TOWER_RANGE,
            cooldown=TOWER_COOLDOWN,
            dano=BULLET_DAMAGE,
            custo=50,
            cor=BLUE,
            nome="Torre Normal"
        )

    # Herda o método atacar padrão da classe base