import pygame
import os
import time
import math
from random import uniform, randrange

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

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img 
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x,self.y))

    def move(self, speed):
        self.y += speed

    def check_bounds(self):
        return self.y < 0 or self.y > HEIGHT - self.img.get_width()

    def collision(self, obj):
        return collide(obj, self)

class Entity:
    COOLDOWN = 30

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

    def check_bounds(self):
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.get_width():
            self.x = WIDTH - self.get_width()

    def cooldown(self):
        if self.cool_down > self.COOLDOWN:
            self.cool_down = 0
        elif self.cool_down > 0:
            self.cool_down += 1

    def shoot(self):
        if self.cool_down == 0:
            laser = Laser(self.x + self.get_width()/2 - self.laser_img.get_width()/2, self.y + self.get_height()/2, self.laser_img)
            self.lasers.append(laser)
            self.cool_down = 1

    def move_lasers(self, speed):
        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.check_bounds():
                self.lasers.remove(laser)

    def draw(self, window):
        for laser in self.lasers:
            laser.draw(window)
        window.blit(self.img, (self.x,self.y))

class Player(Entity):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.img = PLAYER
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health

    def check_bounds(self):
        super().check_bounds()
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.get_height():
            self.y = HEIGHT - self.get_height()

    def move_lasers(self, speed, objs):
        super().move_lasers(speed)
        for laser in self.lasers:
            for obj in objs:
                if laser.collision(obj):
                    objs.remove(obj)
                    self.lasers.remove(laser)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.get_height() + 10, self.get_width()*self.health/self.max_health, 10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

class Enemy(Entity):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.img = ENEMY
        self.laser_img = ENEMY_LASER
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, speed):
        self.y += speed

    def move_lasers(self, speed, obj):
        super().move_lasers(speed)
        for laser in self.lasers:
            if laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

def collide(obj1, obj2):
    offsetX = math.floor(obj2.x - obj1.x)
    offsetY = math.floor(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offsetX, offsetY)) != None

# Game Loop
def main():
    running = True
    lose = False
    loseCount = 0
    mainFont = pygame.font.SysFont("comicsans",50)
    clock = pygame.time.Clock()
    FPS = 60
    lives = 5
    wave = 0

    player = Player(400,300)
    player_speed = 7
    enemies = []
    enemy_speed = 1
    laser_speed = 10

    def redraw_window():
        SCREEN.fill(BACKGROUND_COLOR)

        #draw text
        livesLabel = mainFont.render(f"Lives: {lives}",1,(255,255,255))
        waveLabel = mainFont.render(f"Wave: {wave}",1,(255,255,255))
        SCREEN.blit(livesLabel, (10,10))
        SCREEN.blit(waveLabel, (WIDTH - waveLabel.get_width() - 10,10))

        #draw enmies
        for enemy in enemies:
            enemy.check_bounds()
            enemy.draw(SCREEN)

        #draw player
        player.check_bounds()
        player.draw(SCREEN)

        if lose:
            loseLabel = mainFont.render("YOU LOSE!",1,(255,255,255))
            SCREEN.blit(loseLabel, ( (WIDTH - loseLabel.get_width())/2, 275))

        pygame.display.update()

    while running:
        # update screen with changes at variable FPS
        clock.tick(FPS)
        redraw_window()

        #check if the game is over
        if lives <= 0 or player.health <= 0:
            lose = True
            loseCount += 1
        if lose:
            if loseCount > FPS * 3:
                running = False
            else:
                continue

        #check if the game has been quit
        for event in pygame.event.get():
            # check if the game has been quit
            if event.type == pygame.QUIT:
                running = False

        #move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: # left
            player.x -= player_speed
        if keys[pygame.K_d]: # right
            player.x += player_speed
        if keys[pygame.K_w]: # up
            player.y -= player_speed
        if keys[pygame.K_s]: # down
            player.y += player_speed 

        #shoot player laser
        if keys[pygame.K_SPACE]:
            player.shoot()
        player.move_lasers(-laser_speed, enemies)

        #spawn enemies
        if len(enemies) == 0:
            wave += 1
            enemy_speed += 0.2
            enemies = [Enemy(uniform(0,WIDTH),uniform(-700*wave,-100)) for _ in range(wave*5)]

        #control enemies
        for enemy in enemies[:]:
            #move enemies and their lasers
            enemy.move(enemy_speed)
            enemy.move_lasers(laser_speed, player)
            #radomly shoot enemy lasers
            if randrange(0, 2 * FPS) == 1:
                enemy.shoot()
            
            #check for collision with player
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            #check if off screen
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

def main_menu():
    titleFont = pygame.font.SysFont("comicsans", 70)
    titleLabel = titleFont.render("Press Enter to play...",1,(255,255,255))
    running = True
    while running:
        SCREEN.fill(BACKGROUND_COLOR)
        SCREEN.blit(titleLabel,((WIDTH - titleLabel.get_width())/2, (HEIGHT - titleLabel.get_height())/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
    pygame.quit()

main_menu()