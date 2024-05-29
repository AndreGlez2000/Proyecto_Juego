from typing import List
import pygame
import os
import random

pygame.init()

# CONSTANTES GLOBALES
PANTALLA_Y = 600
PANTALLA_X = 1100
PANTALLA = pygame.display.set_mode((PANTALLA_X, PANTALLA_Y))

# Cargar imágenes
IDLE = [pygame.image.load(os.path.join("imagenes/Player/idle", f"idle {i}.png")) for i in range(1, 11)]
RUNNING = [pygame.image.load(os.path.join("imagenes/Player/run", f"run {i}.png")) for i in range(1, 9)]
JUMPING = pygame.image.load(os.path.join("imagenes/Player/jump", "jump 1.png"))
DUCKING = [pygame.image.load(os.path.join("imagenes/Player/duck", f"duck {i}.png")) for i in range(1, 11)]

ENEMY = [pygame.image.load(os.path.join("imagenes/Enemigo", f"fly {i}.png")) for i in range(1, 7)]
OBSTACLE_1 = [pygame.image.load(os.path.join("imagenes/Obstaculo", "obstaculo 1.png"))]
OBSTACLE_2 = [pygame.image.load(os.path.join("imagenes/Obstaculo", "obstaculo 2.png"))]

NUBE = pygame.image.load(os.path.join("imagenes/Otros", "Cloud.png"))
BG = pygame.image.load(os.path.join("imagenes/Otros", "Track.png"))

class Player:
    POS_Y = 361
    POS_DUCK_Y = 373
    JUMP_VEL = 6.2  # Aumentar la velocidad del salto

    def __init__(self, player_num):
        self.POS_X = 90  # Posición inicial de todos los jugadores
        self.idle_img = IDLE
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.player_num = player_num

        self.player_idle = True
        self.player_duck = False
        self.player_run = False
        self.player_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.idle_img[0]
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.POS_X
        self.player_rect.y = self.POS_Y
        self.gravity = 0.8

    def update(self, userInput):
        if self.player_jump:
            self.jump()
        elif self.player_run:
            self.run()
        elif self.player_duck:
            self.duck()
        else:
            self.idle()

        if self.step_index >= 10:
            self.step_index = 0

        if self.player_num == 1:
            if userInput[pygame.K_UP] and not self.player_jump:
                self.player_idle = False
                self.player_duck = False
                self.player_run = False
                self.player_jump = True
                self.jump_vel = self.JUMP_VEL
            elif userInput[pygame.K_DOWN] and not self.player_jump:
                self.player_idle = False
                self.player_duck = True
                self.player_run = False
                self.player_jump = False
            elif not self.player_jump:
                self.player_idle = False
                self.player_duck = False
                self.player_run = True
                self.player_jump = False
        elif self.player_num == 2:
            if userInput[pygame.K_SPACE] and not self.player_jump:
                self.player_idle = False
                self.player_duck = False
                self.player_run = False
                self.player_jump = True
                self.jump_vel = self.JUMP_VEL
            elif userInput[pygame.K_z] and not self.player_jump:
                self.player_idle = False
                self.player_duck = True
                self.player_run = False
                self.player_jump = False
            elif not self.player_jump:
                self.player_idle = False
                self.player_duck = False
                self.player_run = True
                self.player_jump = False
        elif self.player_num == 3:
            if pygame.mouse.get_pressed()[0] and not self.player_jump:
                self.player_idle = False
                self.player_duck = False
                self.player_run = False
                self.player_jump = True
                self.jump_vel = self.JUMP_VEL
            elif pygame.mouse.get_pressed()[2] and not self.player_jump:
                self.player_idle = False
                self.player_duck = True
                self.player_run = False
                self.player_jump = False
            elif not self.player_jump:
                self.player_idle = False
                self.player_duck = False
                self.player_run = True
                self.player_jump = False

    def idle(self):
        self.image = self.idle_img[self.step_index // (30 // len(self.idle_img))]
        self.step_index += 1
        if self.step_index >= 30:
            self.step_index = 0
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.POS_X
        self.player_rect.y = self.POS_Y
        self.player_rect.width = 35  # Ajustar el ancho del rectángulo de colisión
        self.player_rect.height = 40  # Ajustar la altura del rectángulo de colisión

    def duck(self):
        self.image = self.duck_img[self.step_index // (10 // len(self.duck_img))]
        self.step_index += 1
        if self.step_index >= 10:
            self.step_index = 0
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.POS_X
        self.player_rect.y = self.POS_DUCK_Y
        self.player_rect.width = 35  # Ajustar el ancho del rectángulo de colisión
        self.player_rect.height = 40  # Ajustar la altura del rectángulo de colisión

    def run(self):
        self.image = self.run_img[self.step_index // (16 // len(self.run_img))]
        self.step_index += 1
        if self.step_index >= 16:
            self.step_index = 0
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.POS_X
        self.player_rect.y = self.POS_Y
        self.player_rect.width = 35  # Ajustar el ancho del rectángulo de colisión
        self.player_rect.height = 40  # Ajustar la altura del rectángulo de colisión

    def jump(self):
        self.image = self.jump_img
        if self.player_jump:
            self.player_rect.y -= self.jump_vel * 4
            self.jump_vel -= self.gravity
        if self.jump_vel < -self.JUMP_VEL:
            self.player_jump = False
            self.jump_vel = self.JUMP_VEL

        self.step_index += 1

    def draw(self, PANTALLA):
        PANTALLA.blit(self.image, (self.player_rect.x, self.player_rect.y))

class Cloud:
    def __init__(self):
        self.x = PANTALLA_X + random.randint(800, 1000)
        self.y = random.randint(180, 220)
        self.image = NUBE
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = PANTALLA_X + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, PANTALLA):
        PANTALLA.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = PANTALLA_X

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, PANTALLA):
        PANTALLA.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image: List[pygame.Surface]):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 397
        self.rect.width = 30  # Ajustar el ancho del rectángulo de colisión
        self.rect.height = 30  # Ajustar la altura del rectángulo de colisión
        self.rect.x += 15  # Ajuste horizontal
        self.rect.y -= 20  # Ajuste vertical


class LargeCactus(Obstacle):
    def __init__(self, image: List[pygame.Surface]):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 347  # Ajustar la posición vertical del cactus grande
        self.rect.width = 40  # Ajustar el ancho del rectángulo de colisión
        self.rect.height = 40  # Ajustar la altura del rectángulo de colisión
        self.rect.x += 15  # Ajuste horizontal
        self.rect.y -= 20  # Ajuste vertical


class Bat(Obstacle):
    def __init__(self, image: List[pygame.Surface]):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 370
        self.index = 0

    def draw(self, PANTALLA):
        if self.index >= 9:
            self.index = 0
        PANTALLA.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main(num_players):
    global game_speed, x_pos_bg, y_pos_bg, puntos, obstacles
    run = True
    clock = pygame.time.Clock()
    players = [Player(player_num=i) for i in range(1, num_players + 1)]
    cloud = Cloud()
    game_speed = 4
    x_pos_bg = 0
    y_pos_bg = 380
    puntos = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global puntos, game_speed
        puntos += 1
        if puntos % 100 == 0:
            game_speed += 1

        text = font.render("Puntos: " + str(puntos), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        PANTALLA.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        PANTALLA.blit(BG, (x_pos_bg, y_pos_bg))
        PANTALLA.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        PANTALLA.fill((55, 55, 55))
        userInput = pygame.key.get_pressed()

        for player in players:
            player.draw(PANTALLA)
            player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(OBSTACLE_1))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(OBSTACLE_2))
            else:
                obstacles.append(Bat(ENEMY))

        for obstacle in obstacles:
            obstacle.draw(PANTALLA)
            obstacle.update()
            for player in players:
                if player.player_rect.colliderect(obstacle.rect):
                    pygame.draw.rect(PANTALLA, (255, 0, 0), player.player_rect, 2)
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

        background()
        cloud.update()
        cloud.draw(PANTALLA)
        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    run = True
    clock = pygame.time.Clock()

    while run:
        PANTALLA.fill((55, 55, 55))
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Seleccione el número de jugadores:", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (PANTALLA_X // 2, PANTALLA_Y // 2 - 50)
        PANTALLA.blit(text, textRect)

        text = font.render("1 Jugador (Flecha Arriba)", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (PANTALLA_X // 2, PANTALLA_Y // 2)
        PANTALLA.blit(text, textRect)

        text = font.render("2 Jugadores (Flecha Arriba y Space)", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (PANTALLA_X // 2, PANTALLA_Y // 2 + 50)
        PANTALLA.blit(text, textRect)

        text = font.render("3 Jugadores (Flecha Arriba, Space y Clics)", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (PANTALLA_X // 2, PANTALLA_Y // 2 + 100)
        PANTALLA.blit(text, textRect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main(num_players=1)
                elif event.key == pygame.K_SPACE:
                    main(num_players=2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                main(num_players=3)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    menu(death_count=0)
