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

    teclaUP = False
    teclaDW = False

    acc_y = 0

    while True:

        #Renderização dos itens na tela
        i = 0
        while(i < 1200): 
            SCREEN.blit(bg, (bg.get_width()*i 
                            + scroll, 0)) 
            i += 1

        scroll -= 0.5
    
        if abs(scroll) > bg.get_width(): 
            scroll = 0

        SCREEN.blit(playerImg,(400,pos_player_y))

        acc_y *= 0.999

        for event in pygame.event.get():
          
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w):
                    teclaUP = True
                     
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    teclaDW = True 

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP or event.key == pygame.K_w):
                    teclaUP = False
                     
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    teclaDW = False            

        if pos_player_y < 1:    
            acc_y = 0
            dy = 0

        if pos_player_y > SCREEN.get_height() - 100:    
            acc_y  = 0
            dy = 0

        dy = 0

        if teclaUP:
            dy += -0.001

        if teclaDW:
            dy += 0.001

        acc_y += dy
      
        pos_player_y += acc_y            

        pygame.display.update()
