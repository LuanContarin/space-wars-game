import pygame
from options import options_menu
from components.button import Button
from shared.helpers import get_font

def play_game(SCREEN):
    pygame.display.set_caption("Space Wars")

    # define background screen
    #TODO

    while True:
        #TODO

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
