import pygame
from play import play_game
from options import options_menu
from components.button import Button
from shared.helpers import get_font

def main_menu(SCREEN):
    pygame.display.set_caption("Main Menu")

    # define background screen
    bg = pygame.image.load("./assets/images/menu-background.png")
    logo = pygame.image.load("./assets/images/logo.png")
    logo_rect = logo.get_rect()
    logo_rect.center = (SCREEN.get_rect().centerx, 200)

    SCREEN.blit(bg, (0, 0))
    SCREEN.blit(logo, logo_rect)

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON    = Button(image=None, pos=(SCREEN.get_rect().centerx, 320), text_input="play", font=get_font(70), base_color="#ffff00", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(SCREEN.get_rect().centerx, 420), text_input="options", font=get_font(70), base_color="#ffff00", hovering_color="White")
        QUIT_BUTTON    = Button(image=None, pos=(SCREEN.get_rect().centerx, 520), text_input="quit", font=get_font(70), base_color="#ffff00", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game(SCREEN)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options_menu(SCREEN)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()
