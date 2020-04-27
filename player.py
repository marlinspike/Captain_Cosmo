import pygame
# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    MAX_HIT_POINTS = 2
    def __init__(self, screen_height, screen_width):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./img/fly_1.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width
        self.hit_points = 0
        #self.surf = pygame.Surface((75, 25))
        #self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.switch_player_image()

    def switch_player_image(self):
        img = "./img/fly_0.png"
        if (self.hit_points == 1):
            img = "./img/fly_1.png"
        if (self.hit_points == 2):
            img = "./img/fly_2.png"
        self.surf = pygame.image.load(img).convert()

    #Hit actions
    #Return: TRUE if player is Dead; FALSE otherwise
    def hit(self) -> bool:
        self.hit_points += 1
        if self.hit_points > self.MAX_HIT_POINTS:
            return True # Player is dead
        else:
            self.switch_player_image()
            return False

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT
