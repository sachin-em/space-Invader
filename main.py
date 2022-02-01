import pygame
import pygame.freetype
from pygame import mixer
import random
import math

# initialize pygame
pygame.init()

# create screen
width = 1024
height = 600
screen = pygame.display.set_mode((width, height))

# title and icon
pygame.display.set_caption("Space invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

score = 0
life = 3

# player
player_img = pygame.image.load('player.png')
playerX = width / 2 - 32
playerY = height - 64
speedX = 0
speedY = 0

# asteroid
asteroid_img = []
asteroidX = []
asteroidY = []
num_of_asteroids = 4
for i in range(num_of_asteroids):
    asteroid_img.append(pygame.image.load('asteroid.png'))
    asteroidX.append(random.randint(0, (width - 64)))
    asteroidY.append(random.randint(-80, -32))
angle = 0
asteroid_speed = 0.1

# bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bullet_state = 'loaded'
bullet_speed = 4


def player(x, y):
    screen.blit(player_img, (x, y))


def asteroid(x, y):
    global angle
    angle += 0.1
    for k in range(num_of_asteroids):
        img = pygame.transform.rotate(asteroid_img[k], angle)
        screen.blit(img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    screen.blit(bullet_img, (x, y))
    bullet_state = "fired"


def is_collided(x1, y1, x2, y2, diff):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < diff:
        return True
    else:
        return False


running = True
game_over_music = True
# game loop
while running:
    # screen bg
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speedX = -2
            if event.key == pygame.K_RIGHT:
                speedX = 2
            if event.key == pygame.K_UP:
                speedY = -2
            if event.key == pygame.K_DOWN:
                speedY = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "loaded":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX + 16, bulletY)
                    # play shooting sound
                    mixer.init()
                    mixer.music.load('shoot.wav')
                    mixer.music.play()
            if event.key == pygame.K_ESCAPE:
                if life <= 0:
                    life = 3
                    score = 0
                    playerX = width / 2 - 32
                    playerY = height - 64
                    game_over_music = True
                    for i in range(num_of_asteroids):
                        asteroidX[i] = random.randint(0, (width - 64))
                        asteroidY[i] = random.randint(-80, -32)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                speedX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                speedY = 0
    if life > 0:

        score_string = "Score " + str(score)
        life_string = "Life " + str(life)

        GAME_FONT = pygame.freetype.Font("game_font.ttf", 21)
        GAME_FONT.render_to(screen, (0, 10), score_string, (255, 0, 0))
        GAME_FONT.render_to(screen, (0, 30), life_string, (255, 0, 0))

        playerX += speedX
        playerY += speedY
        if playerX < 0:
            playerX = 0
        elif playerX > (width - 64):
            playerX = (width - 64)

        if playerY < 0:
            playerY = 0
        elif playerY > (height - 64):
            playerY = (height - 64)

        if bullet_state == "fired":
            bulletY -= bullet_speed
            fire_bullet(bulletX + 16, bulletY)
        if bulletY < 0:
            bullet_state = "loaded"

        player(playerX, playerY)
        for p in range(num_of_asteroids):
            asteroid(asteroidX[p], asteroidY[p])
            asteroidY[p] += asteroid_speed

        # when bullet hit asteroid
        for i in range(num_of_asteroids):
            if is_collided(bulletX, bulletY, asteroidX[i], asteroidY[i], 32):
                bullet_state = "loaded"
                asteroidX[i] = random.randint(0, (width - 32))
                asteroidY[i] = random.randint(-100, -32)
                score += 1
                asteroid_speed += score * 0.005
                # play shooting sound
                mixer.init()
                mixer.music.load('explosion.mp3')
                mixer.music.play()

        # when asteroid hit player
        for j in range(num_of_asteroids):
            if is_collided(playerX, playerY, asteroidX[j], asteroidY[j], 64):
                life = 0

            # if asteroid gone out of bound
            if asteroidY[j] > height:
                life -= 1
                asteroidX[j] = random.randint(0, (width - 32))
                asteroidY[j] = random.randint(-100, 32)

        if angle > 359:
            angle = 0
    else:
        if game_over_music:
            # play game over sound
            mixer.init()
            mixer.music.load('game_over.mp3')
            mixer.music.play()
            game_over_music = False
        GAME_FONT = pygame.freetype.Font("game_font.ttf", 50)
        GAME_FONT.render_to(screen, (width / 2 - 90, height / 2),
                            "Game Over", (255, 0, 0))
        GAME_FONT2 = pygame.freetype.Font("game_font.ttf", 24)
        GAME_FONT2.render_to(screen, (width / 9, height / 1.5),
                             "Developed By Sachin M",
                             (255, 0, 0))
        GAME_FONT2.render_to(screen, (width / 2, height / 8),
                             score_string,
                             (255, 0, 0))
        GAME_FONT2.render_to(screen, (width / 2, height / 1.1),
                             "Press Esc to start new game",
                             (255, 0, 0))
    pygame.display.update()
