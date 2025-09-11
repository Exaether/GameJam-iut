from pygame.font import Font
from pygame.mixer import Sound

from paths import get_asset_path

from components.image import Image


class Resources:
    __instance = None

    # Couleurs
    MENU_BACKGROUND_COLOR = "#2f1b14"
    WOOD_COLOR = "#b27b59"
    SILVER_COLOR = "#cdcde1"
    GOLD_COLOR = "#f7be47"
    LIGHT_WOOD_COLOR = "#ffc97f"
    LIGHT_SILVER_COLOR = "#e6e6f2"
    LIGHT_GOLD_COLOR = "#ffff73"
    CRIMSON_COLOR = "#a50034"
    BLUE_COLOR = "#0064c8"
    PURPLE_COLOR = "#6a4c93"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self._initialized = True

        # Jaquette du jeu
        self.__game_cover = None

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

        # Effets sonores
        self.__pickup_sound = None
        self.__detect_sound = None
        self.__pick_trapdoor_sound = None
        self.__defeat_sound = None

        # Images pour le tutoriel
        self.__tutorial_frame_00 = None
        self.__tutorial_frame_01 = None
        self.__tutorial_frame_02 = None
        self.__tutorial_frame_03 = None
        self.__tutorial_frame_04 = None
        self.__tutorial_frame_05 = None
        self.__tutorial_frame_06 = None
        self.__tutorial_frame_07 = None
        self.__tutorial_frame_08 = None
        self.__tutorial_frame_09 = None
        self.__tutorial_frame_10 = None
        self.__tutorial_frame_11 = None
        self.__tutorial_frame_12 = None
        self.__tutorial_frame_13 = None
        self.__tutorial_frame_14 = None
        self.__tutorial_frame_15 = None

    # ========================= SECTION JAQUETTE =========================

    @property
    def game_cover(self):
        if self.__game_cover is None:
                self.__game_cover = Image(
                    get_asset_path('other','game_cover.png'),
                    500, 0
                )
        return self.__game_cover

    # ========================= SECTION PANNEAUX =========================

    @property
    def wood_panel_image(self):
        if self.__wood_panel_image is None:
            self.__wood_panel_image = Image(
                get_asset_path('ui','panels','wood_panel_long.png'),
                0, 600
            )
        return self.__wood_panel_image

    @property
    def silver_panel_image(self):
        if self.__silver_panel_image is None:
            self.__silver_panel_image = Image(
                get_asset_path('ui','panels','silver_panel.png'),
                600, 0
            )
        return self.__silver_panel_image

    @property
    def gold_panel_image(self):
        if self.__gold_panel_image is None:
            self.__gold_panel_image = Image(
                get_asset_path('ui','panels','gold_panel.png'),
                600, 0
            )
        return self.__gold_panel_image

    # ========================= SECTION BOUTONS =========================

    # =============================== BOIS ==============================

    @property
    def wood_button_image_normal(self):
        if self.__wood_button_image_normal is None:
            self.__wood_button_image_normal = Image(
                get_asset_path('ui','buttons','wood_button_normal.png'),
                0, 80
            )
        return self.__wood_button_image_normal

    @property
    def wood_button_image_pressed(self):
        if self.__wood_button_image_pressed is None:
            self.__wood_button_image_pressed = Image(
                get_asset_path('ui','buttons','wood_button_pressed.png'),
                0, 80
            )
        return self.__wood_button_image_pressed

    # ========================= ARGENT =========================

    @property
    def silver_button_image_normal(self):
        if self.__silver_button_image_normal is None:
            self.__silver_button_image_normal = Image(
                get_asset_path('ui','buttons','silver_button_normal.png'),
                0, 80
            )
        return self.__silver_button_image_normal

    @property
    def silver_button_image_pressed(self):
        if self.__silver_button_image_pressed is None:
            self.__silver_button_image_pressed = Image(
                get_asset_path('ui','buttons','silver_button_pressed.png'),
                0, 80
            )
        return self.__silver_button_image_pressed

    @property
    def silver_button_image_normal_short(self):
        if self.__silver_button_image_normal_short is None:
            self.__silver_button_image_normal_short = Image(
                get_asset_path('ui','buttons','silver_button_normal_short.png'),
                0, 80
            )
        return self.__silver_button_image_normal_short

    @property
    def silver_button_image_pressed_short(self):
        if self.__silver_button_image_pressed_short is None:
            self.__silver_button_image_pressed_short = Image(
                get_asset_path('ui','buttons','silver_button_pressed_short.png'),
                0, 80
            )
        return self.__silver_button_image_pressed_short

    # ========================= OR =========================

    @property
    def gold_button_image_normal(self):
        if self.__gold_button_image_normal is None:
            self.__gold_button_image_normal = Image(
                get_asset_path('ui','buttons','gold_button_normal.png'),
                0, 80
            )
        return self.__gold_button_image_normal

    @property
    def gold_button_image_pressed(self):
        if self.__gold_button_image_pressed is None:
            self.__gold_button_image_pressed = Image(
                get_asset_path('ui','buttons','gold_button_pressed.png'),
                0, 80
            )
        return self.__gold_button_image_pressed

    # ========================= SECTION POLICES =========================

    @property
    def game_title_font(self):
        if self.__game_title_font is None:
            self.__game_title_font = Font(get_asset_path('font','VPPixel-Simplified.ttf'), 75)
        return self.__game_title_font

    @property
    def title_font(self):
        if self.__title_font is None:
            self.__title_font = Font(get_asset_path('font','VPPixel-Simplified.ttf'), 50)
        return self.__title_font

    @property
    def subtitle_font(self):
        if self.__subtitle_font is None:
            self.__subtitle_font = Font(get_asset_path('font','VPPixel-Simplified.ttf'), 35)
        return self.__subtitle_font

    @property
    def description_font(self):
        if self.__description_font is None:
            self.__description_font = Font(get_asset_path('font','VPPixel-Simplified.ttf'), 30)
        return self.__description_font

    @property
    def button_font(self):
        if self.__buttons_font is None:
            self.__buttons_font = Font(get_asset_path('font','VPPixel-Simplified.ttf'), 35)
        return self.__buttons_font

    # ========================= SECTION EFFETS SONORES =========================

    @property
    def pickup_sound(self):
        if self.__pickup_sound is None:
            self.__pickup_sound = Sound(get_asset_path('SFX','pickItems.wav'))
        return self.__pickup_sound

    @property
    def detect_sound(self):
        if self.__detect_sound is None:
            self.__detect_sound = Sound(get_asset_path('SFX','alert.wav'))
            # Réduction du volume à 50%
            self.__detect_sound.set_volume(0.5)
        return self.__detect_sound

    @property
    def pick_trapdoor_sound(self):
        if self.__pick_trapdoor_sound is None:
            self.__pick_trapdoor_sound = Sound(get_asset_path('SFX','trapdoor.wav'))
        return self.__pick_trapdoor_sound

    @property
    def defeat_sound(self):
        if self.__defeat_sound is None:
            self.__defeat_sound = Sound(get_asset_path('SFX','defeat.wav'))
        return self.__defeat_sound

    # ========================= SECTION TUTORIEL =========================

    @property
    def tutorial_frame_00(self):
        if self.__tutorial_frame_00 is None:
            self.__tutorial_frame_00 = Image(
                get_asset_path('ui','tutorial','frame0000.png'),
                400, 0
            )
        return self.__tutorial_frame_00

    @property
    def tutorial_frame_01(self):
        if self.__tutorial_frame_01 is None:
            self.__tutorial_frame_01 = Image(
                get_asset_path('ui','tutorial','frame0001.png'),
                400, 0
            )
        return self.__tutorial_frame_01

    @property
    def tutorial_frame_02(self):
        if self.__tutorial_frame_02 is None:
            self.__tutorial_frame_02 = Image(
                get_asset_path('ui','tutorial','frame0002.png'),
                400, 0
            )
        return self.__tutorial_frame_02

    @property
    def tutorial_frame_03(self):
        if self.__tutorial_frame_03 is None:
            self.__tutorial_frame_03 = Image(
                get_asset_path('ui','tutorial','frame0003.png'),
                400, 0
            )
        return self.__tutorial_frame_03

    @property
    def tutorial_frame_04(self):
        if self.__tutorial_frame_04 is None:
            self.__tutorial_frame_04 = Image(
                get_asset_path('ui','tutorial','frame0004.png'),
                400, 0
            )
        return self.__tutorial_frame_04

    @property
    def tutorial_frame_05(self):
        if self.__tutorial_frame_05 is None:
            self.__tutorial_frame_05 = Image(
                get_asset_path('ui','tutorial','frame0005.png'),
                400, 0
            )
        return self.__tutorial_frame_05

    @property
    def tutorial_frame_06(self):
        if self.__tutorial_frame_06 is None:
            self.__tutorial_frame_06 = Image(
                get_asset_path('ui','tutorial','frame0006.png'),
                400, 0
            )
        return self.__tutorial_frame_06

    @property
    def tutorial_frame_07(self):
        if self.__tutorial_frame_07 is None:
            self.__tutorial_frame_07 = Image(
                get_asset_path('ui','tutorial','frame0007.png'),
                400, 0
            )
        return self.__tutorial_frame_07

    @property
    def tutorial_frame_08(self):
        if self.__tutorial_frame_08 is None:
            self.__tutorial_frame_08 = Image(
                get_asset_path('ui','tutorial','frame0008.png'),
                400, 0
            )
        return self.__tutorial_frame_08

    @property
    def tutorial_frame_09(self):
        if self.__tutorial_frame_09 is None:
            self.__tutorial_frame_09 = Image(
                get_asset_path('ui','tutorial','frame0009.png'),
                400, 0
            )
        return self.__tutorial_frame_09

    @property
    def tutorial_frame_10(self):
        if self.__tutorial_frame_10 is None:
            self.__tutorial_frame_10 = Image(
                get_asset_path('ui','tutorial','frame0010.png'),
                400, 0
            )
        return self.__tutorial_frame_10

    @property
    def tutorial_frame_11(self):
        if self.__tutorial_frame_11 is None:
            self.__tutorial_frame_11 = Image(
                get_asset_path('ui','tutorial','frame0011.png'),
                400, 0
            )
        return self.__tutorial_frame_11

    @property
    def tutorial_frame_12(self):
        if self.__tutorial_frame_12 is None:
            self.__tutorial_frame_12 = Image(
                get_asset_path('ui','tutorial','frame0012.png'),
                400, 0
            )
        return self.__tutorial_frame_12

    @property
    def tutorial_frame_13(self):
        if self.__tutorial_frame_13 is None:
            self.__tutorial_frame_13 = Image(
                get_asset_path('ui','tutorial','frame0013.png'),
                400, 0
            )
        return self.__tutorial_frame_13

    @property
    def tutorial_frame_14(self):
        if self.__tutorial_frame_14 is None:
            self.__tutorial_frame_14 = Image(
                get_asset_path('ui','tutorial','frame0014.png'),
                400, 0
            )
        return self.__tutorial_frame_14

    @property
    def tutorial_frame_15(self):
        if self.__tutorial_frame_15 is None:
            self.__tutorial_frame_15 = Image(
                get_asset_path('ui','tutorial','frame0015.png'),
                400, 0
            )
        return self.__tutorial_frame_15
