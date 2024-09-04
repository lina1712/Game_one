import pygame

class Bala:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 10
        self.alto = 10
        self.velocidad = 15
        self.color = "white"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load("C:/Users/dolli/Documents/GitHub/bala_fuego.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))

    def movimiento(self):
        self.y -= self.velocidad
