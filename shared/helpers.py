import pygame
import random
import os
import sys

def get_font(size):
    return pygame.font.Font(resource_path("assets/fonts/Starjedi.ttf"), size)

def get_random_enemy():
    enemy_images = [
        pygame.image.load(resource_path("assets/images/enemies/tie_bomber.png")).convert_alpha(),
        pygame.image.load(resource_path("assets/images/enemies/tie_fighter.png")).convert_alpha(),
        pygame.image.load(resource_path("assets/images/enemies/tie_intercepter.png")).convert_alpha(),
    ]

    return random.choice(enemy_images)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
