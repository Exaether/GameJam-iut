from components.medieval_text import MedievalText


class ComposedText:
    def __init__(self, subtexts: list[MedievalText]):
        self.subtexts = subtexts

        position = None

        for i, subtext in enumerate(subtexts):
            if i > 0:
                subtext.change_left_position(position)

            position = subtext.get_rect.left + subtext.get_rect.width

    def draw(self, surface):
        for subtext in self.subtexts:
            subtext.draw(surface)
