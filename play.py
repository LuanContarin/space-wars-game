import pygame
from options import options_menu
from components.button import Button
from shared.helpers import get_font


def play_game(SCREEN):
    pygame.display.set_caption("Space Wars")

    bg = pygame.image.load("./assets/images/menu-background.png")

    scroll = 0

    playerImg = pygame.image.load('./assets/images/nave.png').convert_alpha()
    playerImg = pygame.transform.scale(playerImg, (100,100))

    player_rect = playerImg.get_rect()

    pos_player_x = 0
    pos_player_y = 0

    while True:

        i = 0
        while(i < 1200): 
            SCREEN.blit(bg, (bg.get_width()*i 
                            + scroll, 0)) 
            i += 1

        scroll -= 0.5
    
        if abs(scroll) > bg.get_width(): 
            scroll = 0

        SCREEN.blit(playerImg,(400,pos_player_y))

        for event in pygame.event.get():
          
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and pos_player_y > 1:
                    pos_player_y -=40 

                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and pos_player_y < SCREEN.get_height():
                    pos_player_y +=40

        player_rect.y = pos_player_y
        player_rect.x = pos_player_x            


        pygame.display.update()
