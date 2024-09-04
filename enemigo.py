import pygame

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 80
        self.alto = 80
        self.velocidad = 5
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.vida = 3
        self.imagen = pygame.image.load("C:/Users/dolli/Documents/GitHub/game_one/marciano.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))

    def movimiento(self):
        self.y += self.velocidad
