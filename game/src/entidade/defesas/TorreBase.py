import math
from abc import ABC, abstractmethod
from entidade import Entidade
from projetil import ProjetilBase

class TorreBase(Entidade):
    def __init__(self, x, y, alcance, cooldown, dano, custo, cor, nome):
        super().__init__(x, y)
        self._alcance = alcance
        self._cooldown_max = cooldown
        self._cooldown = 0
        self._dano = dano
        self._custo = custo
        self._cor = cor
        self._nome = nome
        self._alvo = None

    @abstractmethod
    def draw(self, screen):
        pass

    def update(self, inimigos, projeteis):
        if self._cooldown > 0:
            self._cooldown -= 1
            return

        self._alvo = self.__encontrar_alvo(inimigos)
        
        if self._alvo:
            self.atacar(projeteis)
            self._cooldown = self._cooldown_max

    def __encontrar_alvo(self, inimigos):
        alvo = None
        menor_distancia = self._alcance

        for inimigo in inimigos:
            if inimigo.esta_ativo():
                distancia = math.hypot(inimigo.x - self._x, inimigo.y - self._y)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    alvo = inimigo
        
        return alvo

    def atacar(self, projeteis):
        projeteis.append(ProjetilBase(self._x, self._y, self._alvo, self._dano))

    def get_info(self):
        return {
            "nome": self._nome,
            "dano": self._dano,
            "alcance": self._alcance,
            "velocidade_ataque": 60 / self._cooldown_max,  
            "custo": self._custo
        }
        
    @property
    def alcance(self):
        return self._alcance

    @alcance.setter
    def alcance(self, valor):
        self._alcance = valor

    @property
    def cooldown_max(self):
        return self._cooldown_max

    @cooldown_max.setter
    def cooldown_max(self, valor):
        self._cooldown_max = valor

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, valor):
        self._cooldown = valor

    @property
    def dano(self):
        return self._dano

    @dano.setter
    def dano(self, valor):
        self._dano = valor

    @property
    def custo(self):
        return self._custo

    @custo.setter
    def custo(self, valor):
        self._custo = valor

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
    def alvo(self):
        return self._alvo

    @alvo.setter
    def alvo(self, inimigo):
        self._alvo = inimigo
    
    @property
    def pode_atirar(self):
        return self._cooldown <= 0