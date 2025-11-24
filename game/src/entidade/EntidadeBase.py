import pygame

class Entidade:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ativo = True
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass
    
    def esta_ativo(self):
        return self.ativo