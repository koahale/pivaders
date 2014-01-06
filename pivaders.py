#!/usr/bin/env python

import pygame
from time import sleep
import random

BLACK = [0, 0, 0]; BLUE = [0, 0, 255]; WHITE = [255, 255, 255]
RESOLUTION = [800, 600]
GAME_OVER = False

pygame.init() # Initialise Pygame 
font = pygame.font.SysFont("Arial", 18)
screen = pygame.display.set_mode([RESOLUTION[0], RESOLUTION[1]])
clock = pygame.time.Clock() # Initialise a clock to limit FPS

pygame.display.set_caption('Pivaders - Press ESC to quit')
pygame.mouse.set_visible(False) # We don't need the mouse so hide it

# Load the graphical images we're using.
background_image = pygame.image.load("Space-Background.jpg").convert()

score = 0; shot = 0

##### PLAYER CLASS #####
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.image.load("ship.png").convert() #87 x 80 (image size)
        self.image.set_colorkey(BLACK)
        self.size = (87, 80) # size of the image
        self.rect = pygame.rect.Rect([(RESOLUTION[0] / 2) - self.size[0], RESOLUTION[1] - 125], self.size)
        self.vector = 0
        self.speed = 6
        self.wait = 350 # time in milliseconds between shots
        self.time = pygame.time.get_ticks()

    def update(self):
         # stop the player from leaving either side of the screen
        self.rect.x += self.vector * self.speed
        if self.rect.x > RESOLUTION[0] - self.size[0]:
            self.rect.x = RESOLUTION[0] - self.size[0]
        elif self.rect.x < 0:
            self.rect.x = 0

    def control(self):
        global GAME_OVER, real_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_OVER = True # Quit if window close button is pressed
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_ESCAPE]:
            GAME_OVER = True
        if self.keys[pygame.K_LEFT]:
            player.vector = -1
        elif self.keys[pygame.K_RIGHT]:
            player.vector = 1
        else:
            player.vector = 0 
        if self.keys[pygame.K_SPACE]:
            if real_time - self.time > self.wait:
                make_bullet()
                self.time = real_time

##### ALIENS, BULLETS & BARRIERS CLASSES #####
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Initialise Sprite class
        self.image = pygame.image.load("invader.png").convert() 
        self.image.set_colorkey(BLACK)
        self.size = (40, 30) # size of the image
        self.rect = self.image.get_rect()
        self.vector = [1, 1]
        self.moved = [0, 0] # iterated on as the sprite moves
        self.time = pygame.time.get_ticks()
        self.wait = 1000
        self.distance = [(ALIEN_WIDTH + SPACER), (ALIEN_HEIGHT + SPACER)]
  
    def update(self):
        if current_time - self.time > self.wait:
            if self.moved[0] < 3:
                self.rect.x += self.vector[0] * self.distance[0]
                self.moved[0] +=1
            else:
                if not self.moved[1]:
                    self.rect.y += self.vector[1] * self.distance[1]
                self.vector[0] *= -1
                self.moved = [0, 0]
                self.wait -= 40
            self.time = current_time  

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() # x, y, width & height
        self.vector = 1
        self.speed = 30

    def update(self):
        self.rect.y += self.vector * self.speed
        if bullet.rect.y < 0: # if the bullet goes off the screen, remove it from all groups
            bullet.kill()

### beginnings of block class to create barriers - not yet implimented ###
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) # Initialise the Sprite class
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() # x, y, width & height

#### FUNCTIONS TO CREATE PLAYER BULLETS AND ENEMY MISSILES ####
def make_bullet():
    bullet = Bullet(BLUE, 5, 10)
    bullet.rect.x = player.rect.x + 40
    bullet.rect.y = player.rect.y - 5
    bullet.vector = -1
    bullet_list.add(bullet)
    all_sprite_list.add(bullet)

# missiles not yet implimented...
def make_missile():
    missile = Bullet(RED, 5, 10)
    missile.rect.x = alien.rect.x / 2
    missile.rect.y = alien.rect.z + 40
    missile.list.add(missile)
    all_sprite_list.add(missile)

#### CREATE GROUPS TO CONTROL COLLISSIONS AND DRAWING ####
alien_list = pygame.sprite.Group() # list of sprites (to help with management)
bullet_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group() # list of everything (to help with management)

# Create the player and add it to top-level group
player = Player()
all_sprite_list.add(player) 

###### CREATE A STANDARD WAVE OF ALIENS ########
ROW = 10; COLUMN = 4
ALIEN_WIDTH = 40; ALIEN_HEIGHT = 30; SPACER = 20

for column in range(COLUMN):
    for row in range(ROW):
        alien = Alien() # this is what each alien will look like
        alien.rect.x = SPACER + (row * (ALIEN_WIDTH + SPACER))
        alien.rect.y = SPACER + (column * (ALIEN_HEIGHT + SPACER))
        alien_list.add(alien) # add the aliens to the list we created just now
        all_sprite_list.add(alien) # and also add them to the overall list

###### MAIN GAME LOOP ######## 
while not GAME_OVER: 
    current_time = pygame.time.get_ticks()
    real_time = pygame.time.get_ticks()
    player.control() # control the player
    player.update() # move the player on screen

    for bullet in bullet_list:
        bullet.update() # move the bullets on screen

    for alien in alien_list:
        alien.update() # move the aliens on screen

    ######## SORT THROUGH THE COLLISSION LISTS #########
    # see if a bullet has collided with an alien
    for bullet in bullet_list:
        bullet_hit_list = pygame.sprite.spritecollide(bullet, alien_list, True)

        for alien in bullet_hit_list:
            alien.kill()
            bullet.kill()
            shot += 1
            print "You've shot", shot, "alien(s)!"

    # see if the player has collided with an alien
    alien_hit_list = pygame.sprite.spritecollide(player, alien_list, True)

    # check the list of collisions between player and aliens to see if a life has been lost:
    if len(alien_hit_list) > 0:
        score += 1
        print "Oops - you're dead!"
    
    if len(alien_list) < 1:
        print "You Win!"
    # Update the background then the players' position on the screen
    screen.blit(background_image, [0, 0])
    # draw the sprite list to the screen
    screen.blit(font.render("fps: " + str(clock.get_fps()), 1, WHITE), (0,0))
    all_sprite_list.draw(screen) # draw all actors with a single draw command!
    pygame.display.flip() # Refresh the screen
    clock.tick(30) # Force frame-rate to desired figure

pygame.quit () # Game quits gracefully when 'game_over' turns True