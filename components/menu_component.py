from .medieval_text import MedievalText
from .medieval_button import MedievalButton
from .medieval_panel import MedievalPanel


class MenuComponent:
    def __init__(self, panel: MedievalPanel, title_text: MedievalText,
                 buttons: list[MedievalButton], background_color: str):
        self.panel = panel
        self.title_text = title_text
        self.buttons = buttons
        self.background_color = background_color

    def draw(self, screen):
        screen.fill(self.background_color)

        self.panel.draw(screen)
        self.title_text.draw(screen)

        for button in self.buttons:
            button.draw(screen)
