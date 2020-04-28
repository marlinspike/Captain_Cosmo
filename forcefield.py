import pygame
import random
import cloud

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Forcefield(cloud.Cloud):
    POWER_UP = 5 # Give Player 5 bonus health points!
    def __init__(self, screen_height, screen_width):
        super(Forcefield, self).__init__(screen_height, screen_width)
        self.surf = pygame.image.load("./img/forcefield.png").convert()
        self.speed = random.randint(10, 15)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
