import pygame
from pygame.locals import *
import sys
from config import *
from utilities import *
from random import choice, randint, random

# inicializar modulo de pygame
pygame.init()
screen = pygame.display.set_mode(size_screen)
clock = pygame.time.Clock()
pygame.display.set_caption("Space Breakout")

# Setear imagenes
try:
    heart_full = pygame.transform.scale(
    pygame.image.load("./src/assets/corazon_lleno.png"), (heart_width, heart_height))

    player_image = pygame.image.load("./src/assets/breakout.png")
    player_image = pygame.transform.scale(player_image, (player_widht, player_height))


    ladrillo_image = pygame.image.load("./src/assets/ladrillo.png")
    ladrillo_image = pygame.transform.scale(ladrillo_image, (ladrillo_width, ladrillo_height))

    enemy_image = pygame.image.load("./src/assets/enemy.png")
    enemy_image = pygame.transform.scale(enemy_image, (enemy_widht, enemy_height))


    powe_up_iamge = pygame.image.load("./src/assets/powerup.png")
    powe_up_iamge = pygame.transform.scale(powe_up_iamge, (bonus_widht, bonus_height))

    speed_up_iamge = pygame.image.load("./src/assets/speedup.png")
    speed_up_iamge = pygame.transform.scale(speed_up_iamge, (bonus_widht, bonus_height))


    laser_iamge = pygame.image.load("./src/assets/laser.png")
    laser_iamge = pygame.transform.scale(laser_iamge, (bonus_widht, bonus_height))

    life_image = pygame.image.load("./src/assets/corazon_lleno.png")
    life_image = pygame.transform.scale(life_image, (bonus_widht, bonus_height))

    bullet_image = pygame.image.load("./src/assets/bullet.png")
    bullet_image = pygame.transform.scale(bullet_image, (10, 15))

    background = pygame.transform.scale(
        pygame.image.load("./src/assets/fondo.jpg"), size_screen)
    
    background_init = pygame.transform.scale(
        pygame.image.load("./src/assets/fondoinicio.jpg"), size_screen)
    
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")

#seteo de sonidos
bonus_sound = pygame.mixer.Sound("./src/assets/bonus.mp3")
bonus_sound.set_volume(0.5)


rebote_sound = pygame.mixer.Sound("./src/assets/rebote.mp3")
rebote_sound.set_volume(0.5)

perder_vida_sound = pygame.mixer.Sound("./src/assets/golpe.mp3")
perder_vida_sound.set_volume(0.4)

perder_vida_player_sound =  pygame.mixer.Sound("./src/assets/golpeplayer.mp3")
perder_vida_player_sound.set_volume(0.4)

win_sound = pygame.mixer.Sound("./src/assets/win.mp3")
win_sound.set_volume(0.4)

game_over_sound = pygame.mixer.Sound("./src/assets/gameover.mp3")
game_over_sound.set_volume(0.4)

romper_ladrillo_sound = pygame.mixer.Sound("./src/assets/romperladrillo.mp3")
romper_ladrillo_sound.set_volume(0.2)

laser_sound = pygame.mixer.Sound("./src/assets/laser.mp3")
laser_sound.set_volume(0.1)


playing_music = True


# seteo fuente

fuente = pygame.font.SysFont("Impact", 18)
fuente_inicio = pygame.font.SysFont("Impact", 48)

#seteo datos
score = 0
high_score = 0
lives = 3

texto = fuente.render(f"Score: {score}", True, green)
rect_texto = texto.get_rect()

player_upgrade = False
generate_bonus = False
player = pygame.Rect(width // 2, 570, player_widht, player_height)
player_hit = False
ball = crear_pelota(width // 2, player.top - 19, 20, 20, white, 5, -5)
laser1 = None
laser2= None
laser3 = None
enemy = crear_ladrillo(width // 2, 200, enemy_widht,enemy_height, red)
bullet = pygame.Rect(enemy["rect"].left, enemy["rect"].top, 10, 10)
enemy_move_right = True
enemy_lives = 5
enemy_hit = False
bullet_active = False
game_over = False
paused = False

ladrillos = []
bonuses_active = []
player_bonuses = []

# Create bricks and add them to the list
for fila in range(5):
   for col in range(15):
       left = col * (ladrillo_width + 5)
       top = 50 + fila * (ladrillo_height + 5)
       ladrillo = crear_ladrillo(left, top, ladrillo_width, ladrillo_height, color_random(lista_colores))
       ladrillos.append(ladrillo)

bonus_types = ['power_up', 'speed_up', 'laser', 'life']

bonuses = [  crear_bonus(powe_up_iamge , randint(0, width- block_widht), randint(200, 550), bonus_types[0], cyan),
             crear_bonus(speed_up_iamge ,randint(0, width- block_widht), randint(200, 550), bonus_types[1], red),
             crear_bonus(laser_iamge ,randint(0, width- block_widht), randint(200, 550), bonus_types[2], blue),
             crear_bonus(life_image ,randint(0, width- block_widht), randint(200, 550), bonus_types[3], green)
        ]


# Movements
move_left = False
move_right = False

is_running = True
game_started = False


bullet_event = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_event, 1350)


boton_inicio_rect = pygame.Rect(width // 2 - 100, height // 2 - 100, 200, 50)
boton_salir_rect = pygame.Rect(width // 2 - 100, height // 2 , 200, 50)
pygame.display.flip()


esperando_inicio = True
while esperando_inicio:
    mostrar_texto(screen, "SPACE BREAKOUT", fuente_inicio, (width // 2, 50), white)
    dibujar_boton(screen, "INICIAR JUEGO", fuente, width // 2 - 100, height // 2 - 100, 200, 50, green)
    dibujar_boton(screen,"SALIR",fuente, width // 2 - 100, height // 2 , 200, 50, red)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminar()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if boton_inicio_rect.collidepoint(event.pos):
                    esperando_inicio = False
                    is_running = True
                if boton_salir_rect.collidepoint(event.pos):
                    terminar()


pygame.display.flip()

pygame.mouse.set_visible(False)

pygame.mixer.music.load("./src/assets/musicafondo.mp3")

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)


while is_running and lives > 0:
    for e in pygame.event.get():
        if e.type == QUIT:
            is_running = False
        if e.type == bullet_event:
            if enemy:
                screen.blit(bullet_image, bullet)
                bullet.top = enemy["rect"].top
                bullet.left = enemy["rect"].left
                bullet.move_ip(0, 5)
                laser_sound.play()

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                is_running = False
            if e.key == K_RIGHT or e.key == K_d:
                move_right = True
            if e.key == K_LEFT or e.key == K_a:
                move_left = True
            if e.key == K_SPACE:
                if 'laser' in player_bonuses:
                    midtop = player.midtop
                    laser_w , laser_h = size_laser
                    laser1 = crear_laser(midtop[0] - laser_w // 2, midtop[1] - laser_h, laser_w, laser_h,  speed_laser_y, speed_laser1_x)
                    laser2 = crear_laser(midtop[0] - laser_w // 2, midtop[1] - laser_h, laser_w, laser_h,  speed_laser_y, speed_laser2_x)
                    laser3 = crear_laser(midtop[0] - laser_w // 2, midtop[1] - laser_h, laser_w, laser_h, speed_laser_y, speed_laser3_x)
            if e.key == K_p:  # Presionar "P" para pausar o reanudar el juego
                if not game_over:
                    paused = not paused  # Alternar entre pausar y reanudar el juego
                    if paused:
                        pantalla_pausa(screen, fuente)
        if e.type == KEYUP:
            if e.key == K_RIGHT or e.key == K_d:
                move_right = False
            if e.key == K_LEFT or e.key == K_a:
                move_left = False
        if e.type == MOUSEBUTTONDOWN:
            if  e.button == 1:
                game_started = True
                ball_moving = True

        if e.type == MOUSEMOTION:
            # Actualizar la posición del jugador con el mouse
            mouse_x, _ = e.pos
            # Asegurarse de que el jugador no se salga de la pantalla por la izquierda
            if mouse_x < player.width / 2:
                player.centerx = player.width / 2
            # Asegurarse de que el jugador no se salga de la pantalla por la derecha
            elif mouse_x > width - player.width / 2:
                player.centerx = width - player.width / 2
            # En cualquier otro caso, mover el jugador al cursor del mouse
            else:
                player.centerx = mouse_x

    #movimiento del player
    if  move_right and player.right <= (width - PLAYER_SPEED):
        player.left += PLAYER_SPEED

    elif move_left and player.left >= 0 + PLAYER_SPEED:
        player.left -= PLAYER_SPEED


        
#movimiento del enemigo
    if enemy:
        if enemy_move_right:
            enemy["rect"].left += ENEMY_SPEED
        else:
            enemy["rect"].left -= ENEMY_SPEED
        if enemy["rect"].left < 0:
            enemy_move_right = True
        elif enemy["rect"].right > width:
            enemy_move_right = False
        bullet.move_ip(0,5)
        
#colisiones del enemigo
    if enemy:
        if ball["rect"].colliderect(enemy["rect"]):
            if not enemy_hit:
                ball["speed_y"] = -ball["speed_y"]
                enemy_hit = True
                perder_vida_sound.play()
                enemy_lives -= 1
                if enemy_lives <= 0:
                    enemy = None
            else:
                enemy_hit = False

    if enemy:
        for laser in [laser1, laser2, laser3]:
            if laser and laser.get("rect"):
                if enemy:
                    if laser["rect"].colliderect(enemy["rect"]):
                        perder_vida_sound.play()
                        enemy_lives -= 1
                        if enemy_lives <= 0:
                            # Elimina el enemigo si se queda sin vidas
                            enemy = None
    
    if bullet.colliderect(player):
        if not bullet_active:
            # Resta una vida al jugador cuando la bala del enemigo le pega
            perder_vida_player_sound.play()
            lives -= 1
            bullet_active = True
            player_hit_by_bullet = True
    else:
        # Reinicia el estado de la bala cuando se aleja lo suficiente del jugador
        bullet_active = False
        if not bullet.colliderect(player):
            player_hit_by_bullet = False

    if not game_started:
        ball["rect"].left = player.centerx - ball["rect"].width // 2

    try:
        # Mover la pelota
        if game_started:
            ball["rect"].left += ball["speed_x"]
            ball["rect"].top += ball["speed_y"]


            # Rebote en las paredes
            if ball["rect"].left <= 0 or ball["rect"].right >= width:
                ball["speed_x"] = -ball["speed_x"]
                rebote_sound.play()

            if ball["rect"].top <= 50:
                ball["speed_y"] = -ball["speed_y"]
                rebote_sound.play()


            if ball["rect"].colliderect(player):
                if not player_hit:
                    ball["speed_y"] = -ball["speed_y"]
                    player_hit = True
                    rebote_sound.play()
            else:
                player_hit = False

            if ball["rect"].top >= height:
                lives -= 1
                perder_vida_sound.play()
                if lives > 0:
                    ball["rect"].left = player.centerx - ball["rect"].width // 2
                    ball["rect"].top = player.top - ball["rect"].height
            
            if laser1 or laser2 or laser3: 
                if laser1["rect"].bottom >= 0:
                    laser1["rect"].move_ip(laser1["speed_x"], - laser1["speed_y"])
                    laser2["rect"].move_ip(laser2["speed_x"], - laser2["speed_y"])
                    laser3["rect"].move_ip(laser3["speed_x"], - laser3["speed_y"])
                    laser_sound.play()
                else:
                    laser1 = None
                    laser2 = None
                    laser3 = None
            for laser in [laser1, laser2, laser3]:
                if laser:
                    for i, ladrillo in enumerate(ladrillos):
                        if laser["rect"].colliderect(ladrillo["rect"]):
                            romper_ladrillo_sound.play()
                            score += 10
                            texto = fuente.render(f"Score: {score}", True, green)
                            rect_texto = texto.get_rect()
                            ladrillos.remove(ladrillo)
                            laser1 = None
                            laser2 = None
                            laser3 = None
                            break
    except Exception as e:
        print(f"Error al mover la pelota: {e}")

                        

    try:
        for i, ladrillo in enumerate(ladrillos):
            if ball["rect"].colliderect(ladrillo["rect"]):
                romper_ladrillo_sound.play()
                score += 10
                texto = fuente.render(f"Score: {score}", True, green)
                rect_texto = texto.get_rect()
                ladrillos.remove(ladrillo)
                ball["speed_y"] = -ball["speed_y"]

                # Add a bonus with a 10% probability
                if random() < 0.30:
                    bonus = choice(bonuses)
                    bonuses_active.append(bonus)
    except Exception as e:
        print(f"Error al verificar colisiones con ladrillos: {e}")


    try:
        for i, bonus in enumerate(bonuses_active):
            if ball["rect"].colliderect(pygame.Rect(bonus['position'], (bonus_widht, bonus_height))):
                bonus_sound.play()
                if bonus['type'] == 'power_up':
                    player_widht *= 1.2
                    player_image = pygame.transform.scale(player_image, (player_widht , player_height * 1))

                elif bonus['type'] == 'speed_up':
                    ball["speed_x"] *= 1.2
                    ball["speed_y"] *= 1.2
                elif bonus['type'] == 'laser':
                    midtop = player.midtop
                    laser_w , laser_h = size_laser
                    laser1 = crear_laser(midtop[0] - laser_w // 2, midtop[1] - laser_h, laser_w, laser_h, speed_laser_y, speed_laser1_x)
                    laser2 = crear_laser(midtop[0] - laser_w // 2, midtop[1] - laser_h, laser_w, laser_h,  speed_laser_y, speed_laser2_x)
                    laser3 = crear_laser(midtop[0] - laser_w // 2, midtop[1] - laser_h, laser_w, laser_h, speed_laser_y, speed_laser3_x)
                    player_bonuses.append('laser')
                elif bonus['type'] == 'life':
                    lives += 1
                bonuses_active.remove(bonus)
                break
    except Exception as e:
        print(f"Error al verificar colisiones con bonificaciones: {e}")

        
    if lives == 0:
        game_over_sound.play()
        game_over = True

    if len(ladrillos) == 0:
        win_sound.play()
        screen.fill(black)
        mostrar_texto(screen, "Ganaste!", fuente, (width // 2, height // 2), red)
        pygame.display.flip()

            
    clock.tick(FPS)
    screen.fill(black)
    screen.blit(background, (0,0))

    for ladrillo in ladrillos:
        pygame.draw.rect(screen, ladrillo["color"], ladrillo["rect"])
        screen.blit(ladrillo_image, ladrillo["rect"].topleft)




    for bonus in bonuses_active:
        screen.blit(bonus['image'], bonus['position'])

    if laser1 or laser2 or laser3:
        pygame.draw.rect(screen, red, laser1["rect"])
        pygame.draw.rect(screen, red, laser2["rect"])
        pygame.draw.rect(screen, red, laser3["rect"])


    pygame.draw.rect(screen, black, player, border_radius=20)
    screen.blit(player_image, player)
    pygame.draw.ellipse(screen, ball["color"], ball["rect"])
    if enemy:
        screen.blit(enemy_image, enemy["rect"])
        screen.blit(bullet_image, bullet)

    mostrar_vidas(screen, lives, heart_full)
    mostrar_texto(screen, f"Score: {score}", fuente, (40, 20), green)

    pygame.display.flip()

if score > high_score:
    high_score = score
    
while game_over:
    mostrar_texto(screen, f"Última Puntuación: {score}", fuente_inicio, (width // 2, height // 2 - 20), white)
    mostrar_texto(screen, f"Puntuación Más Alta: {high_score}", fuente_inicio, (width // 2, height // 2 + 20), white)
    mostrar_texto(screen, "Game Over", fuente_inicio, (width // 2, height // 2 - 60), red)
    mostrar_texto(screen, "Presione espacio para salir", fuente_inicio, (width // 2, height // 2 + 80), red)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminar()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                game_over = False
                is_running = False
                esperando_inicio = True
   

terminar()