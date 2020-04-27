import pygame
import random
import enemy

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Boss(enemy.Enemy):
    DAMAGE_CAUSED = 2
    def __init__(self, screen_height, screen_width):
        super(Boss, self).__init__(screen_height, screen_width)
        self.surf = pygame.image.load("./img/boss.png").convert()
        self.speed = random.randint(7, 12)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
