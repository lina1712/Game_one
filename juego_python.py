# importar la libreria pygame
import pygame
#importar el personaje
from personaje import Cubo
#importar el enemigo
from enemigo import Enemigo
#importar la bala
from bala import Bala

from astronauta import Premio

import random


pygame.init()

pygame.mixer.init()

# constantes y creacion de la ventana
ANCHO = 1000
ALTO = 720
VENTANA = pygame.display.set_mode([ANCHO,ALTO])
FPS = 60
FUENTE = pygame.font.SysFont("Cascadia code", 40)
SONIDO_DISPARO = pygame.mixer.Sound('C:/Users/dolli/Documents/GitHub/laser.mp3')
SONIDO_MUERTE_ENEMIGO = pygame.mixer.Sound('C:/Users/dolli/Documents/GitHub/muerte_enemigo.mp3')
SONIDO_MUERTE_PERSONAJE = pygame.mixer.Sound('C:/Users/dolli/Documents/GitHub/muerte_personaje.mp3')

#variables
jugando = True

reloj = pygame.time.Clock()

vida = 3

puntos = 0

tiempo_pasado = 0
tiempo_entre_enemigos = 800

tiempo_pasado_premios = 0
tiempo_entre_premios = 2000

cubo = Cubo(ANCHO/2, ALTO-75)

enemigos = []

premios = []

balas = []

ultima_bala = 0

tiempo_entre_balas = 600

enemigos.append(Enemigo(ANCHO/2, 100))

premios.append(Premio(ANCHO/2, 100))

def crear_bala():
    global ultima_bala

    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))
        ultima_bala = pygame.time.get_ticks()
        SONIDO_DISPARO.play()

def gestionar_teclas(teclas):
    #if teclas[pygame.K_w]:
     #   cubo.y -= cubo.velocidad
    #if teclas[pygame.K_s]:
      #  cubo.y += cubo.velocidad
    if teclas[pygame.K_a]:
        if cubo.x >= 0:
            cubo.x -= cubo.velocidad
    if teclas[pygame.K_d]:
        if cubo.x + cubo.ancho <= ANCHO:
            cubo.x += cubo.velocidad
    if teclas[pygame.K_SPACE]:
        crear_bala()

#creando un bucle para que la ventana quede permanente mientras jugamos
while jugando and vida > 0:

    tiempo_pasado += reloj.tick(FPS)

    if tiempo_pasado > tiempo_entre_enemigos:
        enemigos.append(Enemigo(random.randint(0,ANCHO), -100))
        tiempo_pasado = 0

    tiempo_pasado_premios += reloj.tick(FPS)

    if tiempo_pasado_premios > tiempo_entre_premios:
        premios.append(Premio(random.randint(0,ANCHO), -100))
        tiempo_pasado_premios = 0

    eventos = pygame.event.get()

    teclas = pygame.key.get_pressed()

    texto_vida = FUENTE.render(f"Vida: {vida}", True, "White")

    texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "White")

    gestionar_teclas(teclas)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False

    VENTANA.fill ("purple")

    cubo.dibujar(VENTANA)

    for enemigo in enemigos:
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()

        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            vida -= 1
            SONIDO_MUERTE_PERSONAJE.play()
            print(f'Te quedan {vida} vidas')
            enemigos.remove(enemigo)

        if enemigo.y > ALTO:
            puntos -= 1
            enemigos.remove(enemigo)

        for bala in balas:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                enemigo.vida -= 1
                balas.remove(bala)

        if enemigo.vida <= 0:
            SONIDO_MUERTE_ENEMIGO.play()
            enemigos.remove(enemigo)
            puntos += 3

    for bala in balas:
        bala.dibujar(VENTANA)
        bala.movimiento()

        if bala.y < 0:
            balas.remove(bala)

    for premio in premios:
        premio.dibujar(VENTANA)
        premio.movimiento()

        if pygame.Rect.colliderect(premio.rect, cubo.rect):
            premios.remove(premio)

            if premio.tipo == 1:
                if vida <= 5:
                    vida += 1
                else:
                    puntos += 10

            elif premio.tipo == 2:
                if tiempo_entre_balas > 200:
                    tiempo_entre_balas /= 2
                else:
                    puntos +=10

        if premio.y > ALTO:
            premios.remove(premio)

    VENTANA.blit(texto_vida, (20, 20))
    VENTANA.blit(texto_puntos, (20, 50))

    pygame.display.update()

#SONIDO_MUERTE.play()
pygame.quit()

nombre = input("Introduce tu nombre : ")

with open('puntuaciones.txt', 'a') as archivo:
    archivo.write(f"{nombre} : {puntos}\n")

quit()

