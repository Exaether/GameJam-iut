import pygame
from services import Resources


class Credits:
    # Couleurs
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)

    def __init__(self, screen_width: int, screen_height: int):
        self.settings = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.resources = Resources()
        self.__init_text()

    def __init_text(self):
        self.font = pygame.font.SysFont("Arial", 36)
        # Liste des lignes de crédits
        self.credits = [
            ("Le Château sans Portes", self.resources.game_title_font),
            ("", self.resources.description_font),
            ("Jeu développé par :", self.resources.title_font),
            ("   Kylian Metayer (chef de projet & développement) ", self.resources.subtitle_font),
            ("   Lukas Faure (Architecte développement)", self.resources.subtitle_font),
            ("   Léo Ducruet (Animation & développement)", self.resources.subtitle_font),
            ("   Joan Le Fol (Développement d'interactions)", self.resources.subtitle_font),
            ("   Valentin Wouters (UI/UX designer & développement)", self.resources.subtitle_font),
            ("", self.resources.description_font),
            ("Graphismes : ", self.resources.title_font),
            ("   Pixel-Boy et AAA - Ninja Adventure Asset Pack (Itch.io)", self.resources.subtitle_font),
            ("   LimeZu - Modern Interiors (Itch.io)", self.resources.subtitle_font),
            ("   Pixel Frog - Kings and Pig (Itch.io)", self.resources.subtitle_font),
            ("   Brackeys - Brackeys' Platformer Bundle (Itch.io)", self.resources.subtitle_font),
            ("   Oink55 - Fantasy UI (Itch.io)", self.resources.subtitle_font),
            ("", self.resources.description_font),
            ("Musique : ", self.resources.title_font),
            ("   Kevin MacLeod - incompetech.com (Creative Commons)", self.resources.subtitle_font),
            ("   RUSTED MUSIC STUDIO Music & Assets - 10 spooky 8bit tracks (Itch.io)",
             self.resources.subtitle_font),
            ("   Eric Fredricksen - sfxr.me", self.resources.subtitle_font),
            ("", self.resources.description_font),
            ("Merci d'avoir joué !", self.resources.title_font),
        ]
        self.credit_surfaces = [font.render(text, True, self.BLANC) for (text, font) in self.credits]
        # Position de départ en Y (en dessous de l'écran)
        self.start_y = 600

    def update(self):
        # Fait défiler vers le haut
        self.start_y -= 1

    def draw(self, surface):
        surface.fill(self.NOIR)
        y = self.start_y
        for line_surface in self.credit_surfaces:
            x = (self.screen_width - line_surface.get_width()) // 2
            surface.blit(line_surface, (x, y))
            y += line_surface.get_height() + 20

        # Retourne False si les crédits sont terminés
        return y > 0
