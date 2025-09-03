import pygame, sys
from pygame.locals import *
from Button import Button
from Player import Player

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Runner")
# Create a clock object to manage FPS
clock = pygame.time.Clock()

"""
    Defenition of font use for text. In this case is the default font of pygame
"""
def get_font(size):
    return pygame.font.Font(None, size)

def main_menu():

    while True:
        screen.blit(screen, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Main Menu", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(960, 100))

        play_button = Button(image=None, pos=(960,250), text_input="Play", font=get_font(75), base_color="#d7fcd4", hovering_color="white")
        exit_button = Button(image=None, pos=(960,450), text_input="Exit", font=get_font(75), base_color="#d7fcd4", hovering_color="white")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, exit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(MENU_MOUSE_POS):
                    play()
                if exit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()  
        
        pygame.display.flip()
        clock.tick(60)

"""
    Function for launch game
"""
def play():
    # Bullet settings
    bullet_width = 5
    bullet_height = 10
    bullet_speed = 7
    bullets = []

    # Player settings
    player = Player() 
    player_x = screen_width // 2 - player.get_player_width() // 2 # Spawn position x
    player_y = screen_height - player.get_player_height() - 10 # Spawn position y
    player_list = pygame.sprite.Group()
    player_list.add(player)
    FLAG_GAME = True

    # Main game loop
    while FLAG_GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or player.get_healPoint() == 0:
                pygame.quit()
                sys.exit()
            
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player.get_speed()
        if keys[pygame.K_RIGHT] and player_x < screen_width - player.get_player_width():
            player_x += player.get_speed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player.get_speed()
        if keys[pygame.K_DOWN] and player_y < screen_height - player.get_player_width():
            player_y += player.get_speed()
        if keys[pygame.K_SPACE]:
            # Create a bullet at the current player position
            bullet_x = player_x + player.get_player_width() // 2 - bullet_width // 2
            bullet_y = player_y
            bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

        

        # Update bullet positions
        for bullet in bullets:
            bullet.y -= bullet_speed

        # Remove bullets that are off the screen
        bullets = [bullet for bullet in bullets if bullet.y > 0]

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), bullet)

        player.rect.x = player_x
        player.rect.y = player_y
        player_list.draw(screen)

        # Update the display
        pygame.display.flip()

        if keys[pygame.K_ESCAPE]:
            FLAG_GAME = False
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 1920, 1080))
            main_menu()
            

        # Cap the frame rate at 60 FPS
        clock.tick(360)

main_menu()