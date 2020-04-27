import pygame
import random

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Cloud(pygame.sprite.Sprite):
    def __init__(self, screen_height, screen_width):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("./img/cloud.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width
        self.rect = self.surf.get_rect(
            center=(
                random.randint(self.SCREEN_WIDTH + 20,
                               self.SCREEN_WIDTH + 100),
                random.randint(0, self.SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(20, 30)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
