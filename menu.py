import pygame
from play import play_game
from components.button import Button
from shared.helpers import get_font

def main_menu(SCREEN):

    pygame.mixer.init()

    pygame.mixer.music.load('./assets/sounds/cantina-band.mp3')

    pygame.mixer.music.play(loops=-1, start=0.0)
    pygame.mixer.music.set_volume(0.5)

    pygame.display.set_caption("Main Menu")

    # define background screen
    bg = pygame.image.load("./assets/images/menu-background.png")
    logo = pygame.image.load("./assets/images/logo.png")
    logo_rect = logo.get_rect()
    logo_rect.center = (SCREEN.get_rect().centerx, 200)

    SCREEN.blit(bg, (0, 0))
    SCREEN.blit(logo, logo_rect)

    # subtitle
    subtitle = get_font(25).render("the ultimate battleship for the galaxy!", False, "#E8E6E3")
    subtitle_rect = subtitle.get_rect(center = (SCREEN.get_rect().centerx, 300))
    SCREEN.blit(subtitle, subtitle_rect)

    # instructions
    instructions = get_font(18).render("press W to up, S to down, A to left, D to right and SPACE to shoot.", False, "#E8E6E3")
    instructions_rect = instructions.get_rect(center = (SCREEN.get_rect().centerx, 340))
    SCREEN.blit(instructions, instructions_rect)

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON    = Button(image=None, pos=(SCREEN.get_rect().centerx, 420), text_input="play", font=get_font(70), base_color="#ffff00", hovering_color="White")
        QUIT_BUTTON    = Button(image=None, pos=(SCREEN.get_rect().centerx, 520), text_input="quit", font=get_font(70), base_color="#ffff00", hovering_color="White")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game(SCREEN)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()
