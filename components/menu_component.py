from .animated_image import AnimatedImage
from .medieval_text import MedievalText
from .medieval_button import MedievalButton
from .medieval_panel import MedievalPanel


class MenuComponent:
    def __init__(self, panel: MedievalPanel, texts: list[MedievalText],
                 buttons: list[MedievalButton], tutorial: AnimatedImage,
                 tutorial_x: int, tutorial_y: int,
                 background_color: str):
        self.panel = panel
        self.texts = texts
        self.buttons = buttons
        self.tutorial = tutorial
        self.tutorial_x = tutorial_x
        self.tutorial_y = tutorial_y
        self.background_color = background_color

    def update(self):
        self.tutorial.update()

    def draw(self, screen):
        screen.fill(self.background_color)

        self.panel.draw(screen)

        for text in self.texts:
            text.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        image_surf = self.tutorial.get_frame().image_surf

        screen.blit(
            image_surf,
            image_surf.get_rect(center=(self.tutorial_x, self.tutorial_y))
        )
