import pygame
import random
from components.button import Button
from shared.helpers import get_font, get_random_enemy

def play_game(SCREEN):
    pygame.display.set_caption("Space Wars")

    # Fill the screen with black (the background color)
    SCREEN.fill((0, 0, 0))

    # Load the background screen
    bg = pygame.image.load("./assets/images/menu-background.png")
    bg_width = bg.get_width()
    bg_height = bg.get_height()

    # Initial position of the background
    bg_x = 0

    # Load the player image
    player = pygame.transform.scale(pygame.image.load("./assets/images/player.png").convert_alpha(), (75, 75))
    player_width = player.get_width()
    player_height = player.get_height()

    # Initial position of the player
    player_x = SCREEN.get_width() // 2 - player_width // 2
    player_y = SCREEN.get_height() // 2 - player_height // 2

    # Load bullet image
    bullet = pygame.image.load("./assets/images/red_laser.png").convert_alpha()
    bullet_width = bullet.get_width()
    bullet_height = bullet.get_height()

    # Defining the movement speeds
    background_speed = 9
    player_speed = 8

    # Bullet properties
    bullet_speed = 10
    bullet_cooldown = 300 # Time in milliseconds between bullets
    last_bullet_time = 0  # Tracks the time when the last bullet was fired
    bullets = []  # List to track bullets

    # Enemy properties
    enemy_speed = 3
    enemies = []  # List to track enemies

    clock = pygame.time.Clock()
    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update background position
        bg_x -= background_speed

        # Reset position when it scrolls off-screen
        if bg_x <= -bg_width:
            bg_x = 0

        # Draw the image twice to create the scrolling effect
        SCREEN.blit(bg, (bg_x, 0))
        SCREEN.blit(bg, (bg_x + bg_width, 0))

        # Get the current state of all keys
        keys = pygame.key.get_pressed()

        # Update player position based on keys pressed
        if keys[pygame.K_w]:  # Move up
            player_y -= player_speed
        if keys[pygame.K_s]:  # Move down
            player_y += player_speed
        if keys[pygame.K_a]:  # Move left
            player_x -= player_speed
        if keys[pygame.K_d]:  # Move right
            player_x += player_speed

        # Prevent the player from moving out of bounds
        player_x = max(0, min(SCREEN.get_width() - player_width, player_x))
        player_y = max(0, min(SCREEN.get_height() - player_height, player_y))

        # Check for continuous shooting with cooldown
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_cooldown:
            # Spawn a bullet at the center-right of the player
            bullet_x = player_x + player_width
            bullet_y = player_y + player_height // 2 - bullet_height // 2
            bullets.append((bullet_x, bullet_y))
            last_bullet_time = current_time  # Update the last bullet time

        # Update bullet positions
        bullets = [(x + bullet_speed, y) for x, y in bullets if x < SCREEN.get_width()]

        # Update enemy positions (move enemies from right to left)
        enemies = [(x - enemy_speed, y, img) for x, y, img in enemies if x > -img.get_width()]

        # Randomly spawn enemies at the right edge every 1000ms (1 second)
        if random.randint(1, 60) == 1:  # Random chance per frame (about 1 in 60)
            enemy = get_random_enemy()  # Get a random enemy image
            enemy_y = random.randint(0, SCREEN.get_height() - enemy.get_height())
            enemies.append((SCREEN.get_width(), enemy_y, enemy))  # Spawn enemy at the right side

        # Draw the bullets on the screen
        for bullet_x, bullet_y in bullets:
            SCREEN.blit(bullet, (bullet_x, bullet_y))

        # Draw the enemies on the screen
        for enemy_x, enemy_y, enemy in enemies:
            SCREEN.blit(enemy, (enemy_x, enemy_y))

        # Draw the player on the screen
        SCREEN.blit(player, (player_x, player_y))

        pygame.display.flip()
        clock.tick(60)
