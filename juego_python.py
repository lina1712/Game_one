# importar la libreria pygame
import pygame
#importar el personaje
from personaje import Cubo
#importar el enemigo
from enemigo import Enemigo
#importar la bala
from bala import Bala

from premio import Premio

import random
import sys


pygame.init()

pygame.mixer.init()

# constantes y creacion de la ventana
ANCHO = 1000
ALTO = 720
VENTANA = pygame.display.set_mode([ANCHO,ALTO])
FPS = 60
pygame.display.set_caption("Mi juego")

FUENTE = pygame.font.SysFont("Cascadia code", 40)
SONIDO_DISPARO = pygame.mixer.Sound('C:/Users/dolli/Documents/GitHub/game_one/laser.mp3')
SONIDO_MUERTE_ENEMIGO = pygame.mixer.Sound('C:/Users/dolli/Documents/GitHub/game_one/muerte_enemigo.mp3')
SONIDO_MUERTE_PERSONAJE = pygame.mixer.Sound('C:/Users/dolli/Documents/GitHub/game_one/muerte_personaje.mp3')



def pantalla_inicio():
    ventana_inicio = True
    while ventana_inicio:
        VENTANA.fill("black")
        texto_inicio = FUENTE.render("Presiona ENTER para comenzar", True, "White")
        VENTANA.blit(texto_inicio, (ANCHO // 2 - texto_inicio.get_width() // 2, ALTO // 2 - texto_inicio.get_height() // 2))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ventana_inicio = False


def pantalla_puntajes(puntos):
    nombre = ""

    #crear la ventana para mostrar los puntajes
    ventana_puntajes = True
    while ventana_puntajes:
        VENTANA.fill("black")

        #mostar mensaje de ingreso de nombre
        texto_nombre = FUENTE.render(f"Introduce tu nombre :{nombre}", True, "White")
        VENTANA.blit(texto_nombre, (ANCHO // 2 - texto_nombre.get_width() // 2, 50))

        #mostrar puntajes
        texto_puntajes = FUENTE.render("Puntajes:", True, "White")
        VENTANA.blit(texto_puntajes, (ANCHO // 2 - texto_puntajes.get_width() // 2, 150))


        #leer todas la spuntuaciones
        with open('puntuaciones.txt', 'r') as archivo:
            puntuaciones = archivo.readlines()

        puntuaciones.sort(reverse=True, key=lambda x: int(x.split(":")[1].strip()))

        #mostar las primeras puntuaciones
        for i, puntaje in enumerate(puntuaciones[:5]):
            texto_puntaje = FUENTE.render(puntaje.strip(), True, "White")
            VENTANA.blit(texto_puntaje, (ANCHO // 2 - texto_puntaje.get_width() // 2, 100 + i * 40 ))

        texto_reiniciar = FUENTE.render("Presiona ESPACIO para volver a jugar", True, "White")
        VENTANA.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO - 100))

        pygame.display.update()

        #eventos para salir o volver a jugar
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.key == pygame.K_RETURN:
                    with open('puntuaciones.txt', 'a') as archivo:
                        archivo.write(f"{nombre} : {puntos}\n")
                    ventana_puntajes = False
                elif evento.key == pygame.K_SPACE and len(nombre) > 0:
                    ventana_puntajes =False
                else:
                    if len(nombre) < 10:
                        nombre += evento.unicode

def juego():

    while True:
        pantalla_inicio()

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
            nonlocal ultima_bala

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
                        if vida < 3:
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

        if not pantalla_puntajes(puntos):
            break
        #SONIDO_MUERTE.play()

juego()
pygame.quit()
