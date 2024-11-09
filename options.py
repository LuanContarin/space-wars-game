import pygame
from components.button import Button
from shared.helpers import get_font

def options_menu(SCREEN):
    pygame.display.set_caption("Options")

    # define background screen
    bg = pygame.image.load("./assets/images/menu-background.png")
    SCREEN.blit(bg, (0, 0))

    while True:
        #TODO

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_BACK = Button(image=None, pos=(SCREEN.get_rect().centerx, 320), text_input="BACK", font=get_font(70), base_color="#ffff00", hovering_color="White")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    from menu import main_menu # delayed import to avoid circular import
                    main_menu(SCREEN)

        pygame.display.update()
