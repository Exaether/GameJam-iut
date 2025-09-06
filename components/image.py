from pygame.image import load
from pygame.transform import scale


class Image:
    def __init__(self, path: str, width: int = 0, height: int = 0):
        self.path = path
        self.width = width
        self.height = height

        self.image_surf = load(path)
        orig_width, orig_height = self.image_surf.get_size()

        if self.width:
            ratio = orig_height / orig_width
            self.height = int(self.width * ratio)
        elif self.height:
            ratio = orig_width / orig_height
            self.width = int(self.height * ratio)

        if self.width and self.height:
            self.image_surf = scale(self.image_surf, (self.width, self.height))
        else:
            self.width = orig_width
            self.height = orig_height
