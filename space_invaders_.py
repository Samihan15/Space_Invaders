import pygame
import os
import sys
import random
import math
from pygame import mixer



# Initialize the pygame
pygame.init()
pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load(('background.jpg'))

# background music
mixer.music.load(r'background music.mp3')
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load(('ufo.png'))
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load(('spaceship.png'))
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(('enemy.png')))
    enemyX.append(random.randint(0 , 800))
    enemyY.append(random.randint(50 , 150))
    enemyX_change.append(0.8)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load(('bullet.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.9
bullet_state = "ready"  # Ready :- you can't see the bullet on the screen 


# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# game over 
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_Score(x,y):
    score = font.render("score :"+ str(score_value),True,(255,255,255))
    screen.blit(score, (x , y))


def game_over():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200 , 250))

def player(x,y):
    screen.blit(playerImg, (x , y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x , y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16 , y + 10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX , 2)) + (math.pow(enemyY-bulletY, 2)))  
    if distance < 27 :
        return True
    else:
        return False

# game loop
running = True
while running:
        # RGB - Red , Green , Blue
    screen.fill((0,0,0))

    # Background
    screen.blit(background, (0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound(('laser.mp3'))
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #  5 = 5 + -0.1 -> 5 = 5 -0.1
    #  5 = 5 + 0.1
   
   
    #player movement 
    playerX += playerX_change

    # adding boundry to the screen for player
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
    # adding boundry to the screen for enemy
        if enemyX[i] <=0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

    # collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound(('explosion.wav'))
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0 , 735)
            enemyY[i] = random.randint(50 , 150)

        enemy(enemyX[i] , enemyY[i], i)

    # bullet movement
    if bulletY <=0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change


    player(playerX , playerY)
    show_Score(textX,textY)
    pygame.display.update()
