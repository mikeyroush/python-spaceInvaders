import pygame
import os

# initialize paths
currentPath = os.path.dirname(__file__)
imagePath = os.path.join(currentPath, 'Images')

# initialize pygame
pygame.init()

# create the screen and background
screen = pygame.display.set_mode((800, 600))
bgColor = pygame.Color("#38174c")
screen.fill(bgColor)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join(imagePath, 'icon.png'))
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(os.path.join(imagePath, 'player.png'))
playerImg = pygame.transform.rotozoom(playerImg, 44, 0.25)
playerSize = playerImg.get_rect().size
playerX = 400 - playerSize[0]/2
playerY = 600 - playerSize[1]
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        # check if the game has been quit
        if event.type == pygame.QUIT:
            running = False
        # check for key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 10
            if event.key == pygame.K_RIGHT:
                playerX_change += 10
        if event.type == pygame.KEYUP:
            playerX_change = 0

    # update screen with changes
    screen.fill(bgColor)
    playerX += playerX_change
    player(playerX, playerY)
    pygame.display.update()
pygame.quit()
