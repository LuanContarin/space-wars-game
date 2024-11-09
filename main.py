import pygame
from menu import main_menu

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))

main_menu(SCREEN)