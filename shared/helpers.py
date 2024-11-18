import pygame
import random

def get_font(size):
    return pygame.font.Font("assets/fonts/Starjedi.ttf", size)

def get_random_enemy():
    enemy_images = [
        pygame.image.load("assets/images/enemies/tie_bomber.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/tie_fighter.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/tie_intercepter.png").convert_alpha(),
    ]

    return random.choice(enemy_images)