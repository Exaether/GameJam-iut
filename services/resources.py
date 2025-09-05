from pygame.font import Font

from components.image import Image


class Resources:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self._initialized = True

        # Images pour les panneaux
        self.__wood_panel_image = None
        self.__silver_panel_image = None
        self.__gold_panel_image = None

        # Images pour les boutons
        self.__wood_button_image_normal = None
        self.__wood_button_image_pressed = None
        self.__silver_button_image_normal = None
        self.__silver_button_image_pressed = None
        self.__silver_button_image_normal_short = None
        self.__silver_button_image_pressed_short = None
        self.__gold_button_image_normal = None
        self.__gold_button_image_pressed = None

        # Polices
        self.__game_title_font = None
        self.__title_font = None
        self.__subtitle_font = None
        self.__description_font = None
        self.__buttons_font = None

        # Couleurs
        self.__wood_color = None
        self.__silver_color = None
        self.__gold_color = None

    # ========================= SECTION PANNEAUX =========================

    @property
    def wood_panel_image(self):
        if self.__wood_panel_image is None:
            self.__wood_panel_image = Image(
                "./assets/ui/panels/wood_panel.png",
                600, 0
            )
        return self.__wood_panel_image

    @property
    def silver_panel_image(self):
        if self.__silver_panel_image is None:
            self.__silver_panel_image = Image(
                "./assets/ui/panels/silver_panel.png",
                600, 0
            )
        return self.__silver_panel_image

    @property
    def gold_panel_image(self):
        if self.__gold_panel_image is None:
            self.__gold_panel_image = Image(
                "./assets/ui/panels/gold_panel.png",
                600, 0
            )
        return self.__gold_panel_image

    # ========================= SECTION BOUTONS =========================

    # =============================== BOIS ==============================

    @property
    def wood_button_image_normal(self):
        if self.__wood_button_image_normal is None:
            self.__wood_button_image_normal = Image(
                "./assets/ui/buttons/wood_button_normal.png",
                0, 80
            )
        return self.__wood_button_image_normal

    @property
    def wood_button_image_pressed(self):
        if self.__wood_button_image_pressed is None:
            self.__wood_button_image_pressed = Image(
                "./assets/ui/buttons/wood_button_pressed.png",
                0, 80
            )
        return self.__wood_button_image_pressed

    # ========================= ARGENT =========================

    @property
    def silver_button_image_normal(self):
        if self.__silver_button_image_normal is None:
            self.__silver_button_image_normal = Image(
                "./assets/ui/buttons/silver_button_normal.png",
                0, 80
            )
        return self.__silver_button_image_normal

    @property
    def silver_button_image_pressed(self):
        if self.__silver_button_image_pressed is None:
            self.__silver_button_image_pressed = Image(
                "./assets/ui/buttons/silver_button_pressed.png",
                0, 80
            )
        return self.__silver_button_image_pressed

    @property
    def silver_button_image_normal_short(self):
        if self.__silver_button_image_normal_short is None:
            self.__silver_button_image_normal_short = Image(
                "./assets/ui/buttons/silver_button_normal_short.png",
                0, 80
            )
        return self.__silver_button_image_normal_short

    @property
    def silver_button_image_pressed_short(self):
        if self.__silver_button_image_pressed_short is None:
            self.__silver_button_image_pressed_short = Image(
                "./assets/ui/buttons/silver_button_pressed_short.png",
                0, 80
            )
        return self.__silver_button_image_pressed_short

    # ========================= OR =========================

    @property
    def gold_button_image_normal(self):
        if self.__gold_button_image_normal is None:
            self.__gold_button_image_normal = Image(
                "./assets/ui/buttons/gold_button_normal.png",
                0, 80
            )
        return self.__gold_button_image_normal

    @property
    def gold_button_image_pressed(self):
        if self.__gold_button_image_pressed is None:
            self.__gold_button_image_pressed = Image(
                "./assets/ui/buttons/gold_button_pressed.png",
                0, 80
            )
        return self.__gold_button_image_pressed

    # ========================= SECTION POLICES =========================

    @property
    def game_title_font(self):
        if self.__game_title_font is None:
            self.__game_title_font = Font("./assets/font/VPPixel-Standard.ttf", 75)
        return self.__game_title_font

    @property
    def title_font(self):
        if self.__title_font is None:
            self.__title_font = Font("./assets/font/VPPixel-Standard.ttf", 50)
        return self.__title_font

    @property
    def subtitle_font(self):
        if self.__subtitle_font is None:
            self.__subtitle_font = Font("./assets/font/VPPixel-Standard.ttf", 35)
        return self.__subtitle_font

    @property
    def description_font(self):
        if self.__description_font is None:
            self.__description_font = Font("./assets/font/VPPixel-Standard.ttf", 25)
        return self.__description_font

    @property
    def button_font(self):
        if self.__buttons_font is None:
            self.__buttons_font = Font("./assets/font/VPPixel-Standard.ttf", 35)
        return self.__buttons_font

    # ========================= SECTION COULEURS =========================

    @property
    def wood_color(self):
        if self.__wood_color is None:
            self.__wood_color = "#c29b89"
        return self.__wood_color

    @property
    def silver_color(self):
        if self.__silver_color is None:
            self.__silver_color = "#e6e6f2"
        return self.__silver_color

    @property
    def gold_color(self):
        if self.__gold_color is None:
            self.__gold_color = "#f7be47"
        return self.__gold_color
