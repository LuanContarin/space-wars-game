import sys
import pygame
import random
from gameover import game_over
from components.button import Button
from shared.helpers import get_font, get_random_enemy, resource_path

def play_game(SCREEN):

    pygame.mixer.init()

    pygame.mixer.music.load(resource_path("./assets/sounds/bg.mp3"))

    pygame.mixer.music.play(loops=-1, start=0.0)
    pygame.mixer.music.set_volume(0.5)

    tfsound = pygame.mixer.Sound(resource_path("./assets/sounds/tie-fighter.mp3"))

    pygame.display.set_caption("Space Wars")

    # Fill the screen with black (the background color)
    SCREEN.fill((0, 0, 0))

    # Load the background screen
    bg = pygame.image.load(resource_path("./assets/images/menu-background.png"))
    bg_width = bg.get_width()
    bg_height = bg.get_height()

    # Initial position of the background
    bg_x = 0

    # Load the player image
    player = pygame.transform.scale(pygame.image.load(resource_path("./assets/images/player.png")).convert_alpha(), (75, 75))
    player_width = player.get_width()
    player_height = player.get_height()

    # Initial position of the player
    player_x = SCREEN.get_width() // 2 - player_width // 2
    player_y = SCREEN.get_height() // 2 - player_height // 2

    # Load explosion image and sound
    explosion_image = pygame.transform.scale(pygame.image.load(resource_path("./assets/images/explosion.png")).convert_alpha(), (75, 75))
    explosion_sound = pygame.mixer.Sound(resource_path("./assets/sounds/explosion-sound.mp3"))
    explosions = []

    # Load bullet image
    bullet_red = pygame.image.load(resource_path("./assets/images/red_laser.png")).convert_alpha()
    bullet_green = pygame.image.load(resource_path("./assets/images/green_laser.png")).convert_alpha()
    bullet_width = bullet_red.get_width()
    bullet_width = bullet_green.get_width()
    bullet_height = bullet_red.get_height()
    bullet_height = bullet_green.get_height()

    # Defining the movement speeds
    background_speed = 9
    player_speed = 8

    # Player health properties
    player_health = 100
    max_health = 100

    # Bullet properties
    bullet_speed = 11
    bullet_cooldown = 300  # Time in milliseconds between bullets
    last_bullet_time = 0  # Tracks the time when the last bullet was fired
    bullets = []  # List to track bullets

    # Enemy properties
    enemy_speed = 3
    enemies = []  # List to track enemies

    # Bullet properties for enemies
    enemy_bullet_speed = 10
    last_enemy_bullet_time = 0
    enemy_shoot_timers = {} # Dictionary to track each enemy's shooting timer and cooldown
    enemy_bullets = []  # List to track enemy bullets

    # Score properties
    score = 0
    font = pygame.font.Font(None, 36)  # Font for displaying the score

    clock = pygame.time.Clock()
    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
            
        sound1 = pygame.mixer.Sound(resource_path("./assets/sounds/shot1.mp3"))
        sound1.set_volume(0.3)
        sound2 = pygame.mixer.Sound(resource_path("./assets/sounds/shot2.mp3"))
        sound2.set_volume(0.3)
        sound3 = pygame.mixer.Sound(resource_path("./assets/sounds/shot3.mp3"))
        sound3.set_volume(0.3)

        # Check for continuous shooting with cooldown
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_cooldown:
            sound = random.choice([sound1, sound2, sound3])
            sound.play()
            # Spawn a bullet at the center-right of the player
            bullet_x = player_x + player_width
            bullet_y = player_y + player_height // 2 - bullet_height // 2
            bullets.append((bullet_x, bullet_y))
            last_bullet_time = current_time  # Update the last bullet time

        # Update bullet positions
        bullets = [(x + bullet_speed, y) for x, y in bullets if x < SCREEN.get_width()]

        # Enemy shooting logic
        for idx, (enemy_x, enemy_y, enemy) in enumerate(enemies):
            # Initialize shooting timer and cooldown if not already set
            if idx not in enemy_shoot_timers:
                enemy_shoot_timers[idx] = {
                    "last_shot": pygame.time.get_ticks(),
                    "cooldown": random.randint(500, 1500)  # Random cooldown between 500ms and 1500ms
                }

            # Get the current time and the enemy's shooting data
            current_time = pygame.time.get_ticks()
            last_shot = enemy_shoot_timers[idx]["last_shot"]
            cooldown = enemy_shoot_timers[idx]["cooldown"]

            # Check if the enemy can shoot
            if current_time - last_shot >= cooldown:
                # Spawn a bullet at the center-left of the enemy
                bullet_x = enemy_x - bullet_width
                bullet_y = enemy_y + enemy.get_height() // 2 - bullet_height // 2
                enemy_bullets.append((bullet_x, bullet_y))

                # Update the shooting timer and set a new random cooldown
                enemy_shoot_timers[idx]["last_shot"] = current_time
                enemy_shoot_timers[idx]["cooldown"] = random.randint(500, 1500)

        # Update enemy bullet positions
        enemy_bullets = [(x - enemy_bullet_speed, y) for x, y in enemy_bullets if x > -bullet_width]

        # Update enemy positions (move enemies from right to left)
        enemies = [(x - enemy_speed, y, img) for x, y, img in enemies if x > -img.get_width()]

        # Randomly spawn enemies at the right edge
        if random.randint(1, 60) == 1:
            enemy = get_random_enemy()
            enemy_y = random.randint(0, SCREEN.get_height() - enemy.get_height())
            enemies.append((SCREEN.get_width(), enemy_y, enemy))

        # Check collisions between player's bullets and enemies
        bullets_to_remove = []
        enemies_to_remove = []
        for bullet_x, bullet_y in bullets:
            for i, (enemy_x, enemy_y, enemy) in enumerate(enemies):
                if (
                    bullet_x < enemy_x + enemy.get_width()
                    and bullet_x + bullet_width > enemy_x
                    and bullet_y < enemy_y + enemy.get_height()
                    and bullet_y + bullet_height > enemy_y
                ):
                    bullets_to_remove.append((bullet_x, bullet_y))
                    enemies_to_remove.append(i)
                    score += 1  # Add 10 points for each destroyed enemy

                    explosions.append({
                        "x": enemy_x,
                        "y": enemy_y,
                        "time": pygame.time.get_ticks()
                    })

                    explosion_sound.play()

        # Display explosions and remove them after 300ms
        current_time = pygame.time.get_ticks()
        for explosion in explosions[:]:
            if current_time - explosion["time"] > 300:  # Show for 300ms
                explosions.remove(explosion)
            else:
                SCREEN.blit(explosion_image, (explosion["x"], explosion["y"]))

        # Remove collided bullets and enemies/enemies timers
        bullets = [b for b in bullets if b not in bullets_to_remove]
        enemies = [e for i, e in enumerate(enemies) if i not in enemies_to_remove]
        enemy_shoot_timers = {i: timer for i, timer in enemy_shoot_timers.items() if i < len(enemies)}

        # Check collisions between enemy bullets and the player
        for bullet_x, bullet_y in enemy_bullets:
            if (
                bullet_x < player_x + player_width and
                bullet_x + bullet_width > player_x and
                bullet_y < player_y + player_height and
                bullet_y + bullet_height > player_y
            ):
                player_health -= 5  # Reduce player health
                enemy_bullets.remove((bullet_x, bullet_y))  # Remove the bullet

                # Check if player's health is 0 or below
                if (player_health <= 0):
                    game_over(SCREEN) 

        # Draw the health bar
        x = 10
        y = 10
        health_bar_width = 300
        health_bar_height = 20
        health_ratio = player_health / max_health
        pygame.draw.rect(SCREEN, (0, 0, 0), (x, y, health_bar_width, health_bar_height))  # Background
        pygame.draw.rect(SCREEN, (190, 190, 190), (x - 2, y -2, health_bar_width + 4, health_bar_height + 4), 2) # Stroke
        pygame.draw.rect(SCREEN, (0, 255, 0), (x, y, health_bar_width * health_ratio, health_bar_height))  # Current health

        # Draw the score on the screen
        score_text = get_font(18).render(f"score: {score}", True, (255, 255, 255))
        SCREEN.blit(score_text, (10, 35))

        # Draw the bullets on the screen
        for bullet_x, bullet_y in bullets:
            SCREEN.blit(bullet_green, (bullet_x, bullet_y))

        # Draw the enemy bullets on the screen
        for bullet_x, bullet_y in enemy_bullets:
            SCREEN.blit(bullet_red, (bullet_x, bullet_y))

        # Draw the enemies on the screen
        for enemy_x, enemy_y, enemy in enemies:
            SCREEN.blit(enemy, (enemy_x, enemy_y))

        # Draw the player on the screen
        SCREEN.blit(player, (player_x, player_y))

        pygame.display.flip()
        clock.tick(60)
