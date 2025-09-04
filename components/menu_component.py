import pygame
from .medieval_text import MedievalText
from .medieval_button import MedievalButton
from .medieval_frame import MedievalFrame


class MenuComponent:
    def __init__(self, title_text: MedievalText, buttons: list[MedievalButton], background_color: str):
        self.title_text = title_text
        self.buttons = buttons
        self.background_color = background_color
        
        if buttons:
            min_y = min(button.center_y - button.height//2 for button in buttons) - 100
            max_y = max(button.center_y + button.height//2 for button in buttons) + 50
            frame_height = max_y - min_y
            frame_width = max(button.width for button in buttons) + 150
            
            frame_x = buttons[0].center_x - frame_width//2
            frame_y = min_y
            
            self.frame = MedievalFrame(
                frame_x, frame_y, frame_width, frame_height,
                border_width=4, shadow_offset=8
            )
        else:
            self.frame = None

    def draw(self, screen):
        screen.fill(self.background_color)
        
        if self.frame:
            self.frame.draw(screen)
            
        self.title_text.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)
