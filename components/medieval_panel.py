from components.image import Image


class MedievalPanel:
    PARCHMENT_BASE = "#E9C7A5"
    PARCHMENT_DARK = "#D3BA9C"
    ROYAL_GOLD = "#D9BF77"
    NOBLE_BRONZE = "#CD853F"
    DEEP_SHADOW = "#5E3B49"
    RICH_BROWN = "#7D5B3A"

    def __init__(self, image: Image, center_x: int, center_y: int):
        self.image = image
        self.center_x = center_x
        self.center_y = center_y

        self.rect = self.image.image_surf.get_rect(center=(self.center_x, self.center_y))

    def draw(self, surface):
        surface.blit(self.image.image_surf, self.rect)
