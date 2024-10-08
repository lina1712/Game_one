import pygame
import random

class Premio:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 5
        self.tipo = random.randint(1,2)
        self.color = "orange" if self.tipo == 1 else "green"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load("C:/Users/dolli/Documents/GitHub/game_one/astronauta.png") if self.tipo == 1 else pygame.image.load("C:/Users/dolli/Documents/GitHub/game_one/astronauta2.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))

    def movimiento(self):
        self.y += self.velocidad
