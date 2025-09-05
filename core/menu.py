import pygame
from components.medieval_text import MedievalText
from components.medieval_button import MedievalButton
from components.menu_component import MenuComponent

class Menu:
    
    BACKGROUND_COLOR = "#2F1B14"
    
    def __init__(self, settings, game):
        self.settings = settings
        self.game = game

        self.game_text = MedievalText(
            self.settings.MENU_SCREEN_WIDTH // 2, 200,
            self.settings.GAME_TITLE, 
            pygame.font.Font(None, 75),
            MedievalText.ROYAL_GOLD,
            shadow_offset=4
        )

        self.text_play = MedievalText(
            0, 0, "VOLER !", 
            pygame.font.Font(None, 40), 
            MedievalText.PARCHMENT
        )
        self.button_play = MedievalButton(
            self.settings.MENU_SCREEN_WIDTH // 2, 400, 250, 80,
            self.text_play, 
            MedievalButton.DEEP_NAVY, 
            MedievalButton.ROYAL_BLUE, 
            self.game.play
        )

        # Bouton QUITTER avec style médiéval
        self.text_exit = MedievalText(
            0, 0, "FUIR", 
            pygame.font.Font(None, 40), 
            MedievalText.ROYAL_GOLD
        )
        self.button_exit = MedievalButton(
            self.settings.MENU_SCREEN_WIDTH // 2, 500, 250, 80,
            self.text_exit, 
            MedievalButton.CRIMSON_BASE, 
            MedievalButton.CRIMSON_HOVER, 
            self.game.exit
        )

        # Créer le menu avec le composant générique
        self.menu_component = MenuComponent(
            self.game_text, 
            [self.button_play, self.button_exit], 
            self.BACKGROUND_COLOR
        )
    
    def draw(self, screen):
        self.menu_component.draw(screen)
