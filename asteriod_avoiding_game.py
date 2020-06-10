# Name: Jason(Jabin) Choi
# Date: June 9, 2020

# Project Name: Asteriod Avoiding Game
# Reference: https://riptutorial.com/ebook/pygame

# 1 - install / import pygame and random module
import pygame
import random

# 2 - initialize game variables
# 2.1 - game screen
pygame.init()
screen = pygame.display.set_mode((480, 640))    # width(x): 480, height(y): 640

# 2.2 - game speed / time
FPS = 30    # FPS: Frame per Second
fpsClock = pygame.time.Clock()
asteroidTimer = 100

# 2.3 - initial position variable for asteroids
asteroids = [[20, 0, 0]]    # x axis: 20, y axis: 0, 0: first asteroid img

# 2.4 - score
score = 0

# 3 - pictures and sound effects variables
try:
    spaceshipImg = pygame.image.load("./img/spaceship.png")
    asteroid0 = pygame.image.load("./img/asteroid00.png")
    asteroid1 = pygame.image.load("./img/asteroid01.png")
    asteroid2 = pygame.image.load("./img/asteroid02.png")
    asteroidImgs = (asteroid0, asteroid1, asteroid2)
    gameover = pygame.image.load("./img/gameover.jpg")

    takeoffSound = pygame.mixer.Sound("./audio/takeoff.wav")
    landingSound = pygame.mixer.Sound("./audio/landing.wav")

    takeoffSound.play()
except Exception as err:
    print("ERROR: No picture or sound effects are inserted properly.")
    pygame.quit()
    exit(0)

# 4 - create a displayScore function
def displayScore(arg, x, y):    # arg: the score, x and y: a position of where the score is displayed
    font = pygame.font.Font(None, 24)
    text = font.render("SCORE: " + str(arg).zfill(10), True, (0, 0, 0))      # render(a string of the score, antialias, RGB color)
    textRect = text.get_rect()  # a score object (looks a rectangular)
    textRect.centerx = x        # x axis
    textRect.centery = y        # y axis
    screen.blit(text, textRect)     # draw(represent) the score

# 5 - game loop
running = True
while running:
    screen.fill((255, 255, 255))    # 6 - fill the screen with white (e.g. background screen)

    for event in pygame.event.get():    # 7 - keyboard / mouse event(a user action)
        if event.type == pygame.QUIT:   # game ends when clicking a X button
            pygame.quit()
            exit(0)

    # 8 - Game difficulty
    score += 1
    displayScore(score, 380, 10)
    if score % 100 == 0:    # Every time the score increases by 100, the FPS increases by 2
        FPS += 2

    # 9 - change game components status
    # 9.1 - draw(blit) a spaceship and configure its position
    position = pygame.mouse.get_pos()
    spaceshipPos = (position[0], 600)
    screen.blit(spaceshipImg, spaceshipPos)

    spaceshipRect = pygame.Rect(spaceshipImg.get_rect())    # create a rectangular spaceship object
    spaceshipRect.left = spaceshipPos[0]
    spaceshipRect.top = spaceshipPos[1]

    # 9.2 - draw(blit) asteroids and configure their position
    asteroidTimer -= 10
    if asteroidTimer <= 0:
        asteroids.append([random.randint(5, 475), 0, random.randint(0, 2)])     # asteroids[0]: x axis, asteroids[1]: y axis, asteroids[2]: image 0 ~ 2
        asteroidTimer = random.randint(50, 200)

    index = 0
    for stone in asteroids:
        stone[1] += 10      # an asteroid is moving down (e.g. y axis value increases)
        if stone[1] > 640:  # if the asteroid reaches the bottom,
            asteroids.pop(index)    # remove the asteroid

        stoneRect = pygame.Rect(asteroidImgs[stone[2]].get_rect())      # create a rectangular asteroid object
        stoneRect.left = stone[0]
        stoneRect.top = stone[1]

        # if a spacecraft collides with an asteroid,
        if stoneRect.colliderect(spaceshipRect):
            landingSound.play()     # play a landing sound effect
            asteroids.pop(index)    # remove the asteroid
            running = False         # stop the game loop (e.g. the game ends)

        screen.blit(asteroidImgs[stone[2]], (stone[0], stone[1]))   # draw the asteroid
        index += 1

    # 10 - game speed
    fpsClock.tick(FPS)

    # 11 - update the entire screen
    pygame.display.flip()   # Or pygame.display.update()

# 12 - game over
screen.blit(gameover, (0, 0))
displayScore(score, screen.get_rect().centerx, screen.get_rect().centery)
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)