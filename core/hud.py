from pygame.font import Font    

from entities.compass import Compass
from core.clock import Clock

class HUD:
    def __init__(self, settings, player, suspicion_service):
        self.settings = settings
        self.player = player
        self.suspicion_service = suspicion_service
        self.compass = Compass(self.settings.GAME_SCREEN_WIDTH / 2, self.settings.GAME_SCREEN_HEIGHT / 2)
        self.clock = Clock(self.settings.GAME_SCREEN_WIDTH)
        self.score_font = Font(None, 36)
        self.nb_items_max = self.suspicion_service.total_items

    def draw(self, screen, map_layer):
        # Score
        score_text = self.score_font.render(
            f"Items: {self.player.items_collected}/{self.nb_items_max}",
            True,
            self.settings.WHITE
        )
        score_rect = score_text.get_rect()
        score_rect.topright = (self.settings.GAME_SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)

        self.suspicion_service.draw_suspicion(screen)

        # Boussole
        if self.nb_items_max > 0 and map_layer == self.settings.LAYER_OF_MAP:
            self.compass.draw(screen)
        self.clock.draw(screen)

        # Debug
        if self.settings.DEBUG_MODE:
            self._draw_debug_info(screen)

    def _draw_debug_info(self, screen):
        """Affiche les informations de débogage à l'écran."""
        font = Font(None, 24)
        text = font.render(f"Position: {self.player.get_position()}", True, self.settings.WHITE)
        screen.blit(text, (10, 10))
