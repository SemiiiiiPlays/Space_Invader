import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 500))
isRunning = True

pygame.display.set_caption("Space Invader")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

score_value = 0
font = pygame.font.Font("gamefont.ttf", 30)
gameOverFont = pygame.font.Font("gamefont.ttf", 65)
scoreX = 10
scoreY = 10

playerIcon = pygame.image.load("player.png")
playerX = 370
playerY = 400
playerX_Change = 0

enemyIcon = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
enemyCount = 6

for i in range(enemyCount):
    enemyIcon.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(80, 720))
    enemyY.append(random.randint(1, 3) * 50)
    enemyX_Change.append(0.3)
    enemyY_Change.append(40)

bulletIcon = pygame.image.load("bullet.png").convert_alpha()
bulletX = 0
bulletY = 400
bulletY_Change = -2
# 0 - not in screen; 1 - currently in screen
bulletState = 0

background = pygame.image.load("bg.png").convert()

mixer.music.load("background.wav")
mixer.music.set_volume(0.4)
mixer.music.play(-1)


def game_over_text():
    game_over = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (230, 220))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerIcon, (x, y))


def enemy(x, y, num):
    screen.blit(enemyIcon[num], (x, y))


def shoot(x, y):
    global bulletState
    bulletState = 1
    screen.blit(bulletIcon, (x + 23, y - 45))


def colliding(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance <= 27:
        return True
    else:
        return False


while isRunning:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    player(playerX, playerY)
    show_score(scoreX, scoreY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.5
            if event.key == pygame.K_SPACE:
                if bulletState == 0:
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.set_volume(0.5)
                    bulletSound.play()
                    bulletX = playerX
                    shoot(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    playerX += playerX_Change
    if playerX <= 4:
        playerX = 4
    elif playerX >= 730:
        playerX = 730

    for i in range(enemyCount):
        if enemyY[i] > 400:
            for j in range(enemyCount):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 4:
            enemyX_Change[i] *= -1
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 730:
            enemyX_Change[i] *= -1
            enemyY[i] += enemyY_Change[i]

        collision = colliding(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collisionSound = mixer.Sound("explosion.wav")
            collisionSound.set_volume(0.5)
            collisionSound.play()
            bulletY = 480
            bulletState = 0
            score_value += 100
            enemyX[i] = random.randint(80, 720)
            enemyY[i] = random.randint(1, 3) * 50
            enemyX_Change[i] = 0.3 + (score_value / 100) ** 1.5 * 0.002

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bulletState = 0

    if bulletState == 1:
        shoot(bulletX, bulletY)
        bulletY += bulletY_Change

    pygame.display.update()
