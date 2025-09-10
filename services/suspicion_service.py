from pygame.font import Font

from typing import List, Dict, Any


class SuspicionService:
    """Gestion de la suspicion des gardes et des effets associés
      - 35 % : augmente la range et angle de vision des gardes (multiplicateur)
      - 65 % : augmente la vitesse des gardes (multiplicateur)
    """
    THRESHOLD_VISION_BOOST = 35.0
    THRESHOLD_SPEED_BOOST = 65.0

    # En pourcentage d'augmentation
    VISION_RANGE_MULTIPLIER = 1.25
    VISION_ANGLE_MULTIPLIER = 1.2
    SPEED_MULTIPLIER = 1.3

    SUSPICION_COLOR = (255, 200, 100)

    def __init__(self, player):
        self.player = player

        # suspicion 100% (1.0) = tous les items collectés
        self.suspicion = 0.0
        self.total_items = 0
        self.hud_font = Font(None, 28)

        self._thresholds: List[Dict[str, Any]] = [
            {
                "name": "vision_boost",
                "percent": self.THRESHOLD_VISION_BOOST,
                "applied": False,
                "action": self.__apply_vision_boost,
            },
            {
                "name": "speed_boost",
                "percent": self.THRESHOLD_SPEED_BOOST,
                "applied": False,
                "action": self.__apply_speed_boost,
            },
        ]

    def set_total_items_count(self, total: int):
        self.total_items = total
        self.__recalculate_suspicion_percentage()

    def verify_effect_suspicion_to_apply(self, guards_group):
        self.__recalculate_suspicion_percentage()
        self.__apply_thresholds_if_needed(guards_group)

    def draw_suspicion(self, screen, debug_mode):
        text = self.hud_font.render(f"Suspicion: {int(self.suspicion)}%", True, self.SUSPICION_COLOR)
        if debug_mode:
            screen.blit(text, (10, 40))
        else:
            screen.blit(text, (10, 10))

    def __recalculate_suspicion_percentage(self):
        if self.total_items > 0:
            self.suspicion = (self.player.items_collected / self.total_items) * 100.0
        else:
            self.suspicion = 0.0

    def __apply_thresholds_if_needed(self, guards_group):
        for threshold in self._thresholds:
            if self.suspicion >= threshold["percent"] and not threshold["applied"]:
                threshold["action"](guards_group)
                threshold["applied"] = True

    def __apply_vision_boost(self, guards_group):
        for guard in guards_group.sprites():
            guard.apply_vision_scale(self.VISION_RANGE_MULTIPLIER, self.VISION_ANGLE_MULTIPLIER)

    def __apply_speed_boost(self, guards_group):
        for guard in guards_group.sprites():
            guard.speed_multiplier *= self.SPEED_MULTIPLIER
