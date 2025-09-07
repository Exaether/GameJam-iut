from components.image import Image


class MedievalPanel:
    def __init__(self, image: Image, center_x: int, center_y: int):
        self.image = image
        self.center_x = center_x
        self.center_y = center_y

        self.rect = self.image.image_surf.get_rect(center=(self.center_x, self.center_y))

    def draw(self, surface):
        surface.blit(self.image.image_surf, self.rect)
