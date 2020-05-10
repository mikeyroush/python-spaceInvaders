import pygame
import os
import time
from random import uniform

# initialize paths
CURRENT_PATH = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(CURRENT_PATH, 'Images')

# initialize pygame
pygame.init()

# create the screen and background
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_COLOR = pygame.Color("#38174c")

# load images
ICON = pygame.image.load(os.path.join(IMAGE_PATH, 'icon.png'))
PLAYER = pygame.transform.rotozoom(pygame.image.load(os.path.join(IMAGE_PATH, 'player.png')),44,0.25)
ENEMY = pygame.transform.rotozoom(pygame.image.load(os.path.join(IMAGE_PATH, 'enemy.png')),0,0.25)
PLAYER_LASER = pygame.transform.rotozoom(pygame.image.load(os.path.join(IMAGE_PATH, 'player_laser.png')),0,1)
ENEMY_LASER = pygame.transform.rotozoom(pygame.image.load(os.path.join(IMAGE_PATH, 'enemy_laser.png')),180,1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(ICON)

class Entity:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down = 0

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def draw(self, window):
        window.blit(self.img, (self.x,self.y))

class Player(Entity):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.img = PLAYER
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health

    def check_bounds(self):
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.get_width():
            self.x = WIDTH - self.get_width()
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.get_height():
            self.y = HEIGHT - self.get_height()

class Enemy(Entity):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.img = ENEMY
        self.laser_img = ENEMY_LASER
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, speed):
        self.y += speed

# Game Loop
def main():
    running = True
    mainFont = pygame.font.SysFont("comicsans",50)
    clock = pygame.time.Clock()
    FPS = 60
    lives = 5
    score = 0

    player = Player(400,300)
    player_speed = 7
    enemies = []
    enemy_speed = 1

    def redraw_window():
        SCREEN.fill(BACKGROUND_COLOR)
        #draw text
        livesLabel = mainFont.render(f"Lives: {lives}",1,(255,255,255))
        scoreLabel = mainFont.render(f"Score: {score}",1,(255,255,255))

        SCREEN.blit(livesLabel, (10,10))
        SCREEN.blit(scoreLabel, (WIDTH - scoreLabel.get_width() - 10,10))

        for enemy in enemies:
            enemy.draw(SCREEN)
        player.draw(SCREEN)

        pygame.display.update()

    while running:
        clock.tick(FPS)

        #spawn enemies

        for event in pygame.event.get():
            # check if the game has been quit
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: # left
            player.x -= player_speed
        if keys[pygame.K_d]: # right
            player.x += player_speed
        if keys[pygame.K_w]: # up
            player.y -= player_speed
        if keys[pygame.K_s]: # down
            player.y += player_speed   
        player.check_bounds() # make sure the player is still on the screen

        for enemy in eneies[:]:
            enemy.move(enemy_speed)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # update screen with changes
        redraw_window()
    pygame.quit()
main()