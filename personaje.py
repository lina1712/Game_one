import pygame

class Cubo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 10
        self.color = "pink"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.imagen = pygame.image.load("C:/Users/dolli/Documents/GitHub/cohete.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        #self.imagen = pygame.transform.rotate(self.imagen, 90)

#dibujar mi personaje en pantalla
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        #pygame.draw.rect(ventana, self.color, self.rect)
        ventana.blit(self.imagen, (self.x, self.y))
