from .animated_image import AnimatedImage
from .medieval_button import MedievalButton
from .medieval_panel import MedievalPanel
from .medieval_text import MedievalText


class Menu:
    def __init__(self, background_color: str, panel: MedievalPanel, texts: list[MedievalText],
                 buttons: list[MedievalButton], animated_image: AnimatedImage = None,
                 animated_image_x: int = None, animated_image_y: int = None):
        self.background_color = background_color
        self.panel = panel
        self.texts = texts
        self.buttons = buttons
        self.animated_image = animated_image
        self.animated_image_x = animated_image_x
        self.animated_image_y = animated_image_y

    def update(self):
        self.animated_image.update()

    def draw(self, screen):
        screen.fill(self.background_color)

        self.panel.draw(screen)

        for text in self.texts:
            text.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        if self.animated_image:
            frame_surf = self.animated_image.get_frame().image_surf

            screen.blit(
                frame_surf,
                frame_surf.get_rect(center=(self.animated_image_x, self.animated_image_y))
            )
