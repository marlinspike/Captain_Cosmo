import pygame
from pygame import event
from pygame import display
from pygame import surface
from player import Player
from enemy import Enemy
running = True

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))
surf = pygame.Surface((50, 50))
surf.fill((0,0,0))
rect = surf.get_rect()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500) #Add a new enemy ever 250 milliseconds

# Initialize pygame
pygame.init()

player = Player(SCREEN_HEIGHT, SCREEN_WIDTH)  #Create the Player
# Create groups to hold enemy sprites and all sprites
enemies = pygame.sprite.Group() # enemies is used for collision detection and position updates
all_sprites = pygame.sprite.Group()  # all_sprites is used for rendering
all_sprites.add(player)

#Main Loop
while running:
    for event in pygame.event.get():  # Did user hit a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:  # Did user hit quit
            running = False
        elif event.type == ADDENEMY:  # Add a new enemy?
            new_enemy = Enemy(SCREEN_HEIGHT, SCREEN_WIDTH)  # Create the new enemy and add it to sprite groups
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    player.update(pygame.key.get_pressed())
    enemies.update()
    screen.fill((0, 0, 0))  # Fill the screen with black
    #screen.blit(player.surf, player.rect)  # Draw the player on the screen
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    #Using SpriteCollide instead of SprinteCollideAny, so that we can delete the enemy that collided with us automatically
    if pygame.sprite.spritecollide(player, enemies, True):  # Check if any enemies have collided with the player
        if (player.hit()):
            player.kill()  # If so, then remove the player and stop the loop
            running = False
    pygame.display.flip()
