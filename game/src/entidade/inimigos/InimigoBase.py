import pygame
import sys
import math
from ...mapa.Mapa import *

WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 40)
ENTITY_COLOR = (100, 200, 255)
POINT_COLOR = (255, 100, 100)
PATH_COLOR = (80, 80, 90)

class Enemy:
    def __init__(self, x, y, speed=3):
        self.x = x
        self.y = y
        self.vida = 1
        self.armor = 0
        self.speed = speed
        self.target_points = []  # Lista dos pontos no caminho do inimigo
        self.current_target = 0
        self.radius = 15
        self.color = ENTITY_COLOR
        self.reached_end = False
    
    def add_point(self, x, y):
        "Add um ponto ao caminho "
        self.target_points.append((x, y))
    
    def set_points(self, points):
        "define varios pontos de uma vez"
        self.target_points = points
        self.current_target = 0
        self.reached_end = False

    def update(self):
        "calcula onde vai estar no proximo momento e se move"
        if self.reached_end or not self.target_points:
            return
        
        # Pega alvo atual
        if self.current_target >= len(self.target_points):
            self.reached_end = True
            return
        
        target_x, target_y = self.target_points[self.current_target]
        
        # Calcula direção
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Verifica se chegou
        if distance < self.speed:
            self.x = target_x
            self.y = target_y
            self.current_target += 1
        else:
            #Move
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed