import pygame
from pygame.locals import *
import random
import math
from pygame import mixer

pygame.init()

surface = pygame.display.set_mode((800, 600))

bg = pygame.image.load("resources/background.png")

mixer.music.load("resources/Flying.mp3")
mixer.music.play(-1)

pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("resources/ufo.png")
pygame.display.set_icon(icon)

player_image = pygame.image.load("resources/player.png")
player_x = 390
player_y = 480
player_x_change = 0

enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load("resources/enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(5)
    enemy_y_change.append(40)

bullet_image = pygame.image.load("resources/bullet.png")
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "hold"

score = 0
font = pygame.font.Font("freesansbold.ttf", 30)
textx = 10
texty = 10

game_over_font = pygame.font.Font("freesansbold.ttf", 64)
game_over_score = pygame.font.Font("freesansbold.ttf", 50)
game_over_play_again = pygame.font.Font("freesansbold.ttf", 30)


def show_score(x, y):
    s = font.render("Score : " + str(score), True, (255, 255, 255))
    surface.blit(s, (x, y))


def game_over():
    gof = game_over_font.render("GAME OVER", True, (255, 255, 255))
    gos = game_over_score.render("YOUR SCORE : " + str(score), True, (255, 255, 255))
    gopa = game_over_play_again.render("HIT ENTER TO PLAY AGAIN", True, (255, 255, 255))
    surface.blit(gof, (200, 220))
    surface.blit(gos, (195, 290))
    surface.blit(gopa, (200, 360))


def player(a, b):
    surface.blit(player_image, (a, b))


def enemy(ex, ey, i):
    surface.blit(enemy_image[i], (ex, ey))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    surface.blit(bullet_image, (x + 16, y + 10))


def is_collision(bx, by, ex, ey):
    dist = math.sqrt((math.pow(bx - ex, 2) + math.pow(by - ey, 2)))
    if dist < 27:
        return True
    else:
        return False


running = True
while running:
    surface.fill((0, 0, 0))

    surface.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_RIGHT:
                player_x_change = 6
            if event.key == K_LEFT:
                player_x_change = -6
            if event.key == K_SPACE:
                if bullet_state == "hold":
                    bullet_sound = mixer.Sound("resources/laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
            if enemy_y[0] >= 2000:
                if event.key == K_RETURN:
                    for t in range(num_of_enemies):
                        enemy_y[t] = random.randint(50, 150)
                    score = 0
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):

        if enemy_y[i] >= 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 5
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -5
            enemy_y[i] += enemy_y_change[i]

        collision = is_collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i])
        if collision:
            enemy_sound = mixer.Sound("resources/explosion.wav")
            enemy_sound.play()
            bullet_y = 500
            bullet_state = "hold"
            score += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 500
        bullet_state = "hold"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(textx, texty)
    pygame.display.update()
