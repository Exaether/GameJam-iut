from pygame.font import Font


class ItemPickupEffect:
    """Classe pour gérer les effets visuels de la collecte d'items"""

    def __init__(self):
        self.pickup_font = Font(None, 24)
        self.animations = []

    def add_pickup_animation(self, x, y):
        """Ajoute une animation '+1' à la position donnée"""
        self.animations.append({
            'x': x,
            'y': y,
            'timer': 1.0,
            'original_y': y  # Position Y initiale pour l'effet de montée (+1)
        })

    def update(self, dt):
        remaining_animations = []
        for anim in self.animations:
            anim['timer'] -= dt
            if anim['timer'] > 0:
                # Le "+1" monte vers le haut
                anim['y'] -= 30 * dt
                remaining_animations.append(anim)
        self.animations = remaining_animations

    def draw(self, screen, camera):
        """Dessine toutes les animations '+1' en cours"""
        for anim in self.animations:
            # Fade out progressif basé sur le timer
            alpha = int(255 * anim['timer'])
            pickup_text = self.pickup_font.render("+1", True, (0, 255, 0))
            pickup_text.set_alpha(alpha)
            screen.blit(pickup_text, (anim['x'] - 10 + camera[0], anim['y'] - 10 + camera[1]))
