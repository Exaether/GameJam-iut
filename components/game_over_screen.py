import pygame
from .medieval_text import MedievalText
from .medieval_button import MedievalButton
from .medieval_frame import MedievalFrame

class GameOverScreen:
    TAVERN_BACKGROUND = "#2F1B14"
    
    def __init__(self, screen_width: int, screen_height: int, final_score: int, 
                 on_retry_action=None, on_menu_action=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.final_score = final_score
        
        # Cadre style parchemin
        frame_width = screen_width - 100
        frame_height = screen_height - 80
        self.main_frame = MedievalFrame(
            50, 40, frame_width, frame_height, 
            border_width=6, shadow_offset=10
        )
        
        title_font = pygame.font.Font(None, 85)
        subtitle_font = pygame.font.Font(None, 55) 
        button_font = pygame.font.Font(None, 42)
        
        # Titre principal en rouge cramoisi
        self.title = MedievalText(
            screen_width // 2, 140, 
            "CAPTURÉ PAR LES GARDES !", 
            title_font, 
            MedievalText.CRIMSON_RED,
            shadow_offset=4
        )
        
        # Sous-titre
        self.score_text = MedievalText(
            screen_width // 2, 210,
            f"Trésors pillés : {final_score}",
            subtitle_font,
            MedievalText.ROYAL_GOLD
        )
        
        encouragement_message = self._get_encouragement_message(final_score)
        self.encouragement_message_text = MedievalText(
            screen_width // 2, 270,
            encouragement_message,
            pygame.font.Font(None, 38),
            MedievalText.NOBLE_BRONZE
        )
        
        retry_text = MedievalText(
            screen_width // 2, 370, "NOUVELLE QUÊTE", 
            button_font, MedievalText.PARCHMENT
        )
        self.retry_button = MedievalButton(
            screen_width // 2, 370, 280, 75, 
            retry_text, 
            MedievalButton.DEEP_NAVY,
            MedievalButton.ROYAL_BLUE,
            on_retry_action
        )
        
        menu_text = MedievalText(
            screen_width // 2, 465, "RETOUR À LA TAVERNE", 
            button_font, MedievalText.ROYAL_GOLD
        )
        self.menu_button = MedievalButton(
            screen_width // 2, 465, 320, 75, 
            menu_text, 
            MedievalButton.CRIMSON_BASE,
            MedievalButton.CRIMSON_HOVER,
            on_menu_action
        )
        
        self.buttons = [self.retry_button, self.menu_button]

    def _get_encouragement_message(self, score: int) -> str:
        """Messages d'encouragement dans le style médiéval noble"""
        if score == 0:
            return "Hélas ! Les gardes étaient trop vigilants..."
        elif score <= 3:
            return "Quelques pièces d'or... Un début prometteur !"
        elif score <= 7:
            return "Belle razzia ! Tu deviens un habile brigand !"
        else:
            return "Magnifique butin ! Le roi tremblent !"

    def draw(self, surface):
        surface.fill(self.TAVERN_BACKGROUND)
        
        # Cadre de parchemin
        self.main_frame.draw(surface)
        
        # Textes
        self.title.draw(surface)
        self.score_text.draw(surface)
        self.encouragement_message_text.draw(surface)
        
        # Boutons
        for button in self.buttons:
            button.draw(surface)
    