import pygame
import random
import math
import time

from pygame import mixer

#Comment with ** is things to do

# Initialize pygame
pygame.init()

# Create Windows
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('sfondo.png')
backgroundX = 0
backgroundY = 0
backgroundX_change = 0
backgroundY_change = 0

#background2 - To scroll
background2 = pygame.image.load('sfondo.png')
background2X = 800
background2Y = 0
background2X_change = 0
background2Y_change = 0

'''
# Music in background
mixer.music.load('music.mp3') 
mixer.music.play(-1)
'''

# Title and icon
pygame.display.set_caption("First")

icon = pygame.image.load('First.png')
pygame.display.set_icon(icon)

# Player
play = pygame.image.load('player.png')
playerX = 170
playerY = 460
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enimies = 3

for i in range(num_of_enimies):
    enemyImg.append(pygame.image.load('crow.png'))
    enemyX.append(random.randint(800, 1600)) #crow start in some point on the left of the board
    enemyY.append(random.randint(0, 460)) #crow start in some point over the ground
    enemyX_change.append(random.uniform(-0.6, -0.3)) #random speed
    enemyY_change.append(random.uniform(-0.1, 0.1)) #-> to not move up and down the crow->  enemyY_change.append(0)

# Egg
eggImg = pygame.image.load('eggs.png')    # **maybe it's possible to do the same thing of the crow to have more egg**
eggX = 0
eggY = 0
eggX_change = 2
eggY_change = 0
egg_state = "ready"  # Ready or Fire

# Score
score_value = 0
font = pygame.font.Font('Babydoo.ttf', 50)
textX = 10
textY = 10
def show_score(x, y):
     score = font.render("Score: " + str(score_value), True, (255, 255, 255))
     screen.blit(score, (x, y))

# Game Over
over_font = pygame.font.Font('Babydoo.ttf', 84)
def game_over_text():
    over_text = over_font.render("GAME OVER: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (160, 250))

# function to draw player
def player(x, y):
    screen.blit(play, (x, y))

# function to draw enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# function to draw egg
def fire_egg(x, y):
    global egg_state
    egg_state = "fire"
    screen.blit(eggImg, (x + 32, y + 16))


# function to draw ambient
def sfondo(x, y) :
    screen.blit(background, (x, y))

# function to draw ambient2
def sfondo2(x, y):
    screen.blit(background2, (x, y))


# Fuction for Collision
def isCollision(enemyX, enemyY, eggX, eggY):
    distance = math.sqrt(math.pow(enemyX-eggX, 2) + math.pow(enemyY-eggY, 2))
    if distance < 27:
        return True
    else: return False

#******************************************************#

# Game Loop
running = True
while (running):

    # RGB background
    screen.fill((0, 0, 0))

    # call-function to draw ambient
    sfondo(backgroundX, backgroundY)
    # call-function to draw ambient2
    sfondo2(background2X, background2Y)

    # Code to "scroll" the two ambients
    backgroundX_change = -0.1
    backgroundX += backgroundX_change
    background2X_change = -0.1
    background2X += background2X_change

    # Alternation of the two ambients
    if (int(background2X) == 0):
        backgroundX = 0
        backgroundY = 0
        background2X = 800
        background2Y = 0

    # IMPORTANT - Pygame has the "Event" object, so it records user events (like pressing a key)
    # in an event queue that can be received with the pygame.event.get () code.
    for event in pygame.event.get():

        # Pressing the X of the windows, quit
        if event.type == pygame.QUIT:
            running = False

        # clicking...
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = +0.5
            if egg_state == "ready":
                if event.key == pygame.K_SPACE:
                    egg_Sound = mixer.Sound('pio.wav')
                    egg_Sound.play()
                    fire_egg(playerX, playerY)
                    eggX = playerX
                    eggY = playerY

        # release...   #Problema con il fatto che se premi su e poi giu contemporaneamente di blocca
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_UP:
                playerY_change = 0

    # Position
    playerX += playerX_change
    playerY += playerY_change

    # Bounderies
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 460:
        playerY = 460


    #Enemy movement
    for i in range(num_of_enimies):
        #Game Over
        #If enemy reach the limit, game over
        if enemyX[i] < 0:
            for j in range(num_of_enimies):
                enemyX[j] = -500 #the enemy disappear
            game_over_text()
            running = False
            break

        # each enemy has HIS speed, but when collision, the speed change
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        # upper and lower edge for enemy (bounce)
        if enemyY[i] >= 460:
            enemyY_change[i] = -enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = -enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], eggX, eggY)
        if collision:
            crow_Sound = mixer.Sound('kill crow.wav')
            crow_Sound.play()
            if egg_state == "fire":
                egg_state = "ready"
                eggX = playerX
                eggY = playerY
                score_value += 1
                enemyX[i] = random.randint(800, 1600)
                enemyY[i] = random.randint(0, 460)
                enemyX_change[i] = random.uniform(-0.6, -0.3)
                enemyY_change[i] = random.uniform(-0.1, 0.1)

        # call fuction enemy
        enemy(enemyX[i], enemyY[i], i)

    # chiamata a funzione giocatore
    player(playerX, playerY)

    # Movement Egg
    if egg_state == "fire":
        fire_egg(eggX, eggY)
        eggY += eggY_change
        eggX += eggX_change

    if eggX >= 800:
        egg_state = "ready"

    show_score(textX, textY)

    # To Refresh the screen
    pygame.display.update()

    # Very important - Here for wait 5 second before close windows (automatically)
    if not running:
        time.sleep(5)