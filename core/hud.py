from pygame.font import Font

from core.clock import Clock
from core.settings import Settings
from entities.compass import Compass


class HUD:
    def __init__(self, player, suspicion_service):
        self.player = player
        self.suspicion_service = suspicion_service
        self.compass = Compass(Settings.GAME_SCREEN_WIDTH / 2, Settings.GAME_SCREEN_HEIGHT / 2)
        self.clock = Clock(Settings.GAME_SCREEN_WIDTH)
        self.score_font = Font(None, 36)
        self.nb_items_max = self.suspicion_service.total_items

    def draw(self, screen, map_layer):
        # Score
        self._draw_score(screen)

        self.suspicion_service.draw_suspicion(screen, Settings.DEBUG_MODE)

        # Boussole
        if self.nb_items_max > 0 and map_layer == Settings.LAYER_OF_MAP:
            self.compass.draw(screen)
        self.clock.draw(screen)

        # Debug
        if Settings.DEBUG_MODE:
            self._draw_debug_info(screen)

    def _draw_score(self, screen):
        score_text = self.score_font.render(
            f"Items: {self.player.items_collected}/{self.nb_items_max}",
            True,
            Settings.WHITE
        )
        score_rect = score_text.get_rect()
        score_rect.topright = (Settings.GAME_SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)

    def _draw_debug_info(self, screen):
        """Affiche les informations de débogage à l'écran."""
        font = Font(None, 24)
        text = font.render(f"Position: {self.player.get_position()}", True, Settings.WHITE)
        screen.blit(text, (10, 10))
