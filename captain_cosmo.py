import pygame
from pygame import event
from pygame import display
from pygame import surface
from player import Player
from enemy import Enemy
from cloud import Cloud
from boss import Boss
from forcefield import Forcefield
import random

running = True
Game_Clock = pygame.time.Clock()
# Define constants for the screen width and height
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Captain Cosmo")
screen.fill((0, 0, 0))
surf = pygame.Surface((50, 50))
surf.fill((0,0,0))
rect = surf.get_rect()

# Create a custom event for adding a new enemy
EVENT_ADD_ENEMY = pygame.USEREVENT + 1; pygame.time.set_timer(EVENT_ADD_ENEMY, 200)  # Add a new enemy ever 200 milliseconds
EVENT_ADD_HEALING_CLOUD = pygame.USEREVENT + 2; pygame.time.set_timer(EVENT_ADD_HEALING_CLOUD, random.randint(250, 5000))  # Add a new Healing Cloud
EVENT_ADD_BOSS = pygame.USEREVENT + 3;  pygame.time.set_timer(EVENT_ADD_BOSS, random.randint(250, 5000))  # Add a new Boss
EVENT_ADD_FORCEFIELD = pygame.USEREVENT + 4;  pygame.time.set_timer(EVENT_ADD_FORCEFIELD, random.randint(7000, 15000))  # Add a new Forcefield
IS_GAME_OVER = False

# Initialize pygame
pygame.init()
pygame.mixer.music.load("./wav/bgmusic.wav")
pygame.mixer.music.play(-1)

player = Player(SCREEN_HEIGHT, SCREEN_WIDTH)  #Create the Player
# Create groups to hold enemy sprites and all sprites
enemies = pygame.sprite.Group() # enemies is used for collision detection and position updates
clouds = pygame.sprite.Group() # clouds is used for collision detection and position updates
bosses = pygame.sprite.Group()
forcefields = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()  # all_sprites is used for rendering
all_sprites.add(player); all_sprites.add(enemies); all_sprites.add(clouds); all_sprites.add(bosses); all_sprites.add(forcefields)
Last_Update_Time = pygame.time.get_ticks()

def show_score():
    global Last_Update_Time
    if (IS_GAME_OVER == False):
        time_in_secs = pygame.time.get_ticks() / 1000
    else:
        time_in_secs = Last_Update_Time
    score = pygame.font.Font('freesansbold.ttf', 20)
    #if(pygame.time.get_ticks() - Last_Update_Time)/1000 > 1:
    img = score.render(f"Time: {int(time_in_secs)} | Health: {player.get_health()}", True, (255, 255, 255))
    screen.blit(img, (50, 10))
    Last_Update_Time = time_in_secs

#Main Loop
while running:
    for event in pygame.event.get():  # Did user hit a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:  # Did user hit quit
            running = False
        elif event.type == EVENT_ADD_HEALING_CLOUD:
             if (IS_GAME_OVER == False):
                 new_cloud = Cloud(SCREEN_HEIGHT, SCREEN_WIDTH)
                 clouds.add(new_cloud)
                 all_sprites.add(new_cloud)
        elif event.type == EVENT_ADD_BOSS:  # Add a new boss?
            if(IS_GAME_OVER == False):  # Only add new enemies if the Game is still in play (Player not Dead)
                # Create the new enemy and add it to sprite groups
                new_boss = Boss(SCREEN_HEIGHT, SCREEN_WIDTH)
                bosses.add(new_boss)
                all_sprites.add(new_boss)
        elif event.type == EVENT_ADD_ENEMY:  # Add a new enemy?
            if(IS_GAME_OVER == False): # Only add new enemies if the Game is still in play (Player not Dead)
                new_enemy = Enemy(SCREEN_HEIGHT, SCREEN_WIDTH)  # Create the new enemy and add it to sprite groups
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
        elif event.type == EVENT_ADD_FORCEFIELD:
            if (IS_GAME_OVER == False):
                new_ff = Forcefield(SCREEN_HEIGHT, SCREEN_WIDTH)
                forcefields.add(new_ff)
                all_sprites.add(new_ff)

    player.update(pygame.key.get_pressed())
    clouds.update()
    enemies.update()
    bosses.update()
    forcefields.update()
    screen.fill((0, 0, 0))  # Fill the screen with black
    show_score()

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    #Using SpriteCollide instead of SprinteCollideAny, so that we can delete the enemy that collided with us automatically
    if pygame.sprite.spritecollide(player, enemies, True):  # Check if any enemies have collided with the player
        player.hit(Enemy.DAMAGE_CAUSED)
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollide(player, bosses, True):
        player.hit(Boss.DAMAGE_CAUSED)
    if pygame.sprite.spritecollide(player, clouds, True):
        player.heal()  #Heal player if he hits a healing cloud!
    if pygame.sprite.spritecollide(player, forcefields, True):
        player.get_forcefield(Forcefield.POWER_UP) # Heal player if he hits a healing cloud!

    if (player.is_player_dead()):
        IS_GAME_OVER = True
        #player.kill()  # If so, then remove the player and stop the loop
        for e in all_sprites:
            e.kill()
            #running = False #End game 

    pygame.display.flip()
