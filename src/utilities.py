import pygame
from config import *

def color_aleatorio():
    from random import randrange
    r = randrange(256)
    g = randrange(256)
    b = randrange(256)
    return(r, g, b)

def color_random(lista_colores):
    from random import randrange
    import config
    return lista_colores[randrange(len(lista_colores))]

def crear_ladrillo(left=0, top=0, ancho=40, alto=40, color=white):
   ladrillo = pygame.Rect(left, top, ancho, alto)
   return {"rect": ladrillo, "color": color}

def mostrar_texto(superficie, texto, fuente, coordenadas, color_fuente):
   sup_texto = fuente.render(texto, True, color_fuente)
   rect_texto = sup_texto.get_rect()
   rect_texto.center = coordenadas
   superficie.blit(sup_texto, rect_texto)
   pygame.display.flip()

def mostrar_vidas(screen, vidas, heart_full, top=10):
   for i in range(vidas):
       hearths_position = width - (vidas - i) * (heart_width + top)
       screen.blit(heart_full, (hearths_position, top))

def crear_pelota(left=0, top=0, ancho=20, alto=20, color=white, speed_x=0, speed_y=0):
   pelota = pygame.Rect(left, top, ancho, alto)
   return {"rect": pelota, "color": color, "speed_x": speed_x, "speed_y": speed_y}

def crear_laser(left=0, top=0, laser_width=2, laser_height=5, speed_y=0, speed_x = 0):
   laser = pygame.Rect(left, top, laser_width, laser_height)
   return {"rect": laser, "speed_y": speed_y, "speed_x" : speed_x}

def crear_bonus(imagen, left, top, tipo, color):
   bonus = pygame.Rect(left, top, bonus_widht, bonus_height)
   return {"position": (left, top), "color": color, "type": tipo, "image": imagen}

def terminar():
    pygame.quit()
    exit()

def pantalla_pausa(screen, fuente):
    screen.fill(black)
    mostrar_texto(screen, "Juego en pausa", fuente, (width // 2, height // 2 - 40), red)
    mostrar_texto(screen, "Presiona P nuevamente para reanudar", fuente, (width // 2, height // 2 + 20), white)
    pygame.display.flip()
    paused = True
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    pygame.mixer.music.unpause()
            if event.type == pygame.QUIT:
                terminar()  # Opcional: permite salir del juego desde la pantalla de pausa


def dibujar_boton(screen, texto, fuente,top, left, widht, height, color):
    # Definir las coordenadas y dimensiones del botón
    boton_rect = pygame.Rect(top, left, widht, height)

    # Dibujar el botón
    pygame.draw.rect(screen, color, boton_rect)
    mostrar_texto(screen, texto , fuente, boton_rect.center, black)
    
    return boton_rect
