import pygame
import os
from random import uniform


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(imagePath, 'player.png'))
        self.image = pygame.transform.rotozoom(self.image, 44, 0.25)
        self.size = self.image.get_rect().size
        self.x = 400 - self.size[0]/2
        self.y = 600 - self.size[1]
        self.dx = 0

    def checkBounds(self):
        if self.x < 0:
            self.x = 0
        elif self.x > 800 - self.size[0]:
            self.x = 800 - self.size[0]

    def move(self, key):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx -= 10
            if event.key == pygame.K_RIGHT:
                self.dx += 10
        if event.type == pygame.KEYUP:
            self.dx = 0

    def update(self):
        self.x += self.dx
        self.checkBounds()
        screen.blit(self.image, (self.x, self.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(imagePath, 'ufo.png'))
        self.image = pygame.transform.rotozoom(self.image, 0, 0.25)
        self.size = self.image.get_rect().size
        self.x = 400 - self.size[0]/2
        self.y = 10
        self.dx = 3

    def checkBounds(self):
        if self.x < 0 or self.x > 800 - self.size[0]:
            self.dx *= -1
            self.y += 10

    def update(self):
        self.x += self.dx
        self.checkBounds()
        screen.blit(self.image, (self.x, self.y))


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

# initialize player and enemies
player = Player()
enemy = Enemy()

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        # check if the game has been quit
        if event.type == pygame.QUIT:
            running = False
        # move player
        player.move(event)

    # update screen with changes
    screen.fill(bgColor)
    player.update()
    enemy.update()
    pygame.display.update()
pygame.quit()
