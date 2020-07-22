import math
import random

import pygame
from pygame import mixer
# initialise
pygame.init()

# create screen                  width height
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('innovation.png')
pygame.display.set_icon(icon)

#Background
background=pygame.image.load('spaceshipbg.png').convert()

#Background music
mixer.music.load('Skrillex - Coast Is Clear with Chance The Rapper and th.mp3')
mixer.music.play(-1)


# Enemy Definition
enemyimg = []
enemyX = []
enemyY = []
enemyX_change =[]
enemyY_change = []
num_of_enemies=6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('skull.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyimg[i], (int(x), int(y)))


# player defintion
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerimg, (int(x), int(y)))

#Bullet
bulletimg=pygame.image.load('bullet.png' )
bulletX=0
bulletY=playerY
bulletX_change=0
bulletY_change=1
bullet_state="ready"

#score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

textX= 10
textY=10


#Game Over
over_font=pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text =over_font.render('Game Over',True,(255,255,255))
    screen.blit(over_text,(200,250))



def score_show(x,y):
    score=font.render('Score:'+str(score_value),True,(255,255,255))
    screen.blit(score,(int(x),int(y)))



def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(int(x)+16,int(y)+10))

# collision function
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False


# For closing
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    #Background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #For Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state=='ready':
                    bullet_sound=mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    #For Enemy Boundaries
    for i in range(num_of_enemies):
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # for collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound=mixer.Sound('invaderkilled.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 100
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)


    #Bullet Movement
    if bulletY<=0:
        bulletY=playerY
        bullet_state='ready'
    if bullet_state == "fire" :
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change


    #For Player Boundaries
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 736
    elif playerX >= 736:
        playerX = 0
    if playerY <= 0:
        playerY = 536
    elif playerY >= 536:
        playerY = 0

    player(playerX, playerY)
    score_show(textX,textY)
    pygame.display.update()
