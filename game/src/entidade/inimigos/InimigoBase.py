from abc import abstractmethod
import math
from entidade import EntidadeBase
from config import PATH

class InimigoBase(EntidadeBase):
    def __init__(self, x, y, vida, velocidade, recompensa, cor, nome, tamanho=15, pontos=1):
        super().__init__(x, y)
        self._path_index = 0
        self._hp = vida
        self._max_hp = vida
        self._velocidade = velocidade
        self._recompensa = recompensa
        self._cor = cor
        self._nome = nome
        self._tamanho = tamanho
        self._alive = True
        self._pontos = pontos
        
    @abstractmethod
    def draw(self, screen):
        pass    
    
    def update(self):
        return self.move()
    
    def move(self):
        if self._path_index < len(PATH) - 1:
            target_x, target_y = PATH[self._path_index + 1]
            dx = target_x - self._x
            dy = target_y - self._y
            dist = math.hypot(dx, dy)
            
            if dist < self._velocidade:
                self._path_index += 1
            else:
                self._x += (dx / dist) * self._velocidade
                self._y += (dy / dist) * self._velocidade
        else:
            return True
        
        return False

    def tomar_dano(self, dano):
        self._hp -= dano
        if self._hp <= 0:
            self._alive = False
            self._ativo = False
    
    def esta_ativo(self):
        return self._ativo and self._alive

    def get_info(self):
        return {
            "nome": self._nome,
            "vida": self._hp,
            "velocidade": self._velocidade,
            "recompensa": self._recompensa
        }
        
    @property
    def path_index(self):
        return self._path_index

    @path_index.setter
    def path_index(self, valor):
        self._path_index = valor

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, valor):
        self._hp = valor

    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, valor):
        self._max_hp = valor

    @property
    def velocidade(self):
        return self._velocidade

    @velocidade.setter
    def velocidade(self, valor):
        self._velocidade = valor

    @property
    def recompensa(self):
        return self._recompensa

    @recompensa.setter
    def recompensa(self, valor):
        self._recompensa = valor

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, valor):
        self._cor = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, valor):
        self._tamanho = valor

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, valor):
        self._alive = valor

    @property
    def pontos(self):
        return self._pontos

    @pontos.setter
    def pontos(self, valor):
        self._pontos = valor