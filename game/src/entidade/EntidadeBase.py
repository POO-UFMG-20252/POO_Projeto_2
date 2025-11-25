from abc import ABC, abstractmethod
class EntidadeBase(ABC):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._ativo = True
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    def esta_ativo(self):
        return self._ativo
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y