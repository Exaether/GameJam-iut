import pygame
from entities.player import Player

class IntroGame:
    FADE_IN_DURATION_SECONDS = 0.8
    FADE_OUT_DURATION_SECONDS = 0.8
    TYPING_SPEED_CHAR_PER_SEC = 15
    BACKSPACE_SPEED_CHAR_PER_SEC = 15
    DELAY_AFTER_LINE_SECONDS = 0.2

    DIALOG_BOX_PADDING = 16
    DIALOG_BOX_MIN_HEIGHT = 120
    DIALOG_BOX_BG_COLOR = (0, 0, 0, 180)
    DIALOG_TEXT_COLOR = (230, 230, 230)
    DIALOG_HINT_COLOR = (200, 200, 200)
    DIALOG_HINT_TEXT = "[Entrée]"
    DIALOG_BOX_BOTTOM_MARGIN = 40
    DIALOG_HINT_MARGIN_X = 16
    DIALOG_HINT_MARGIN_Y = 12

    MODE_TYPING_NORMAL = "typing_normal"
    MODE_TYPING_BEFORE = "typing_before"
    MODE_BACKSPACING_TO_ANCHOR = "backspacing_to_anchor"
    MODE_TYPING_REPLACEMENT = "typing_replacement"
    MODE_COMPLETED = "completed"

    REPLACE_TOKEN = "|REPLACE|"

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.screen_rect = pygame.Rect(0, 0, self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT)

        self.player = self.__init_player()
        self.target_x = self.screen_rect.centerx - self.player.SPRITE_SIZE // 2
        self.fade_in_alpha = 255
        self.fade_out_alpha = 0
        self.is_fading_out = False

        self.current_line_index = 0
        self.current_text = ""
        self.full_text = ""
        self.chars_shown = 0
        self.type_accumulator = 0.0
        self.backspace_accumulator = 0.0
        self.allow_advance = False
        self.mode = self.MODE_TYPING_NORMAL
        self.anchor_length = 0
        self.replacement_suffix = ""

        self.font = pygame.font.Font("./assets/font/VPPixel-Standard.ttf", 25) if self.settings else None

        self.dialog_lines = [
            "Ca c'est Georgres, Geores est ce qu'on appel un voleur",
            "Comme tout voleur, Georges vol",
            "Mais contrairement aux autres Georges a des co...|REPLACE|Mais contrairement aux autres Georges a du courage !",
            "C'est pour ça que Georges va au chateau pour voler le roi et trouver le fam...",
        ]

        self.__prepare_current_line()

    def __init_player(self):
        player = Player(self.settings.GAME_SCREEN_WIDTH + 100, self.settings.GAME_SCREEN_HEIGHT // 2)
        player.direction = "left"
        player.speed = 220
        player.is_moving = True
        return player

    def __prepare_current_line(self, anchor_pattern=None):
        """Prépare la ligne courante pour affichage
                Si la ligne contient le token |REPLACE| on prépare l'animation de remplacement de char
                Sinon, on prépare l'animation de base de typing
        """
        raw_line = self.dialog_lines[self.current_line_index]
        if self.REPLACE_TOKEN in raw_line:
            before, replacement = raw_line.split(self.REPLACE_TOKEN)
            self.full_text = before
            if anchor_pattern:
                idx = before.rfind(anchor_pattern)
                self.anchor_length = idx + len(anchor_pattern) if idx != -1 else 0
            else:
                self.anchor_length = 0
            self.replacement_suffix = replacement[self.anchor_length:]
            self.mode = self.MODE_TYPING_BEFORE
        else:
            self.full_text = raw_line
            self.anchor_length = 0
            self.replacement_suffix = ""
            self.mode = self.MODE_TYPING_NORMAL
        self.current_text = ""
        self.chars_shown = 0
        self.type_accumulator = 0.0
        self.backspace_accumulator = 0.0
        self.allow_advance = False

    def handle_events(self, events):
        for event in events:
            """permet de passer à la ligne suivante ou skip l'animation et charger la ligne suivante"""
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.allow_advance and not self.is_fading_out:
                    self.__advance_dialog_or_fade_out()
                elif not self.allow_advance and not self.is_fading_out:
                    self.__skip_typing_animation()

    def __advance_dialog_or_fade_out(self):
        """permet de charger la ligne suivante et faire lancer le fade out de fin"""
        if self.current_line_index < len(self.dialog_lines) - 1:
            self.current_line_index += 1
            if self.current_line_index == 2:
                self.__prepare_current_line(anchor_pattern=" a ")
            else:
                self.__prepare_current_line()   
        else:
            self.is_fading_out = True
            self.fade_out_alpha = 0

    def __skip_typing_animation(self):
        """on force l'affichage de la ligne courante"""
        self.current_text = self.__get_final_text_for_current_line()
        self.mode = self.MODE_COMPLETED
        self.allow_advance = True
        self.type_accumulator = 0.0
        self.backspace_accumulator = 0.0

    def __get_final_text_for_current_line(self):
        final_text = self.full_text
        if self.mode in (self.MODE_TYPING_BEFORE, self.MODE_BACKSPACING_TO_ANCHOR, self.MODE_TYPING_REPLACEMENT) and self.replacement_suffix:
            final_text = self.full_text[:self.anchor_length] + self.replacement_suffix
        return final_text

    def __update_fade(self, dt):
        # Tant qu'on est pas au dernier dialogue on reste sur le fade in qui s'execute lors du chargement de l'intro
        if self.fade_in_alpha > 0:
            self.fade_in_alpha = max(0, self.fade_in_alpha - int(255 * dt / self.FADE_IN_DURATION_SECONDS))
        if self.is_fading_out:
            self.fade_out_alpha = min(255, self.fade_out_alpha + int(255 * dt / self.FADE_OUT_DURATION_SECONDS))
            if self.fade_out_alpha >= 255:
                self.game.play()

    def __update_player_motion(self, dt):
        """On fait bouger le joueur vers la gauche jusqu'à ce qu'il soit centré puis il reste idle"""
        if self.player.rect.x > self.target_x:
            self.player.move(None, -1, 0, dt)
        else:
            # pour changer sa position et le mettre idle à la fin de sa course (et le faire une seule fois)
            if self.player.is_moving:
                self.player.idle()
                self.player.direction = "down"
            self.player.update(dt, None)

    def __update_typing(self, dt):
        if self.mode == self.MODE_TYPING_NORMAL:
            self.__typing_normal(dt)
        elif self.mode == self.MODE_TYPING_BEFORE:
            self.__typing_before(dt)
        elif self.mode == self.MODE_BACKSPACING_TO_ANCHOR:
            self.__backspacing_to_anchor(dt)
        elif self.mode == self.MODE_TYPING_REPLACEMENT:
            self.__typing_replacement(dt)

    def __typing_normal(self, dt):
        """Grâce a la preparation de la ligne on peut déjà commencer à écrire le texte"""
        if self.chars_shown < len(self.full_text):
            self.type_accumulator += dt * self.TYPING_SPEED_CHAR_PER_SEC
            chars_to_add = int(self.type_accumulator) - self.chars_shown
            if chars_to_add > 0:
                self.chars_shown = self.chars_shown + chars_to_add
                self.current_text = self.full_text[:self.chars_shown]
        else:
            self.type_accumulator += dt
            if self.type_accumulator >= self.DELAY_AFTER_LINE_SECONDS:
                self.allow_advance = True

    def __typing_before(self, dt):
        if self.chars_shown < len(self.full_text):
            self.type_accumulator += dt * self.TYPING_SPEED_CHAR_PER_SEC
            chars_to_add = int(self.type_accumulator) - self.chars_shown
            if chars_to_add > 0:
                self.chars_shown = min(len(self.full_text), self.chars_shown + chars_to_add)
                self.current_text = self.full_text[:self.chars_shown]
        else:
            self.mode = self.MODE_BACKSPACING_TO_ANCHOR
            self.backspace_accumulator = 0.0

    def __backspacing_to_anchor(self, dt):
        if len(self.current_text) > self.anchor_length:
            self.backspace_accumulator += dt * self.BACKSPACE_SPEED_CHAR_PER_SEC
            total_to_remove = int(self.backspace_accumulator)
            current_len = len(self.full_text)
            removed_so_far = current_len - len(self.current_text)
            to_remove_now = total_to_remove - removed_so_far
            while to_remove_now > 0 and len(self.current_text) > self.anchor_length:
                self.current_text = self.current_text[:-1]
                to_remove_now -= 1
        else:
            self.mode = self.MODE_TYPING_REPLACEMENT
            self.type_accumulator = 0.0
            self.chars_shown = 0

    def __typing_replacement(self, dt):
        if self.chars_shown < len(self.replacement_suffix):
            self.type_accumulator += dt * self.TYPING_SPEED_CHAR_PER_SEC
            chars_to_add = int(self.type_accumulator) - self.chars_shown
            if chars_to_add > 0:
                self.chars_shown = min(len(self.replacement_suffix), self.chars_shown + chars_to_add)
                self.current_text = self.full_text[:self.anchor_length] + self.replacement_suffix[:self.chars_shown]
        else:
            self.type_accumulator += dt
            if self.type_accumulator >= self.DELAY_AFTER_LINE_SECONDS:
                self.allow_advance = True

    def __wrap_text(self, text, font, max_width):
        lines = []
        if text:
            words = text.split(" ")
            current_line = ""
            for word in words:
                test_line = (current_line + " " + word) if current_line else word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    if font.size(word)[0] <= max_width:
                        current_line = word
                    else:
                        part = ""
                        for ch in word:
                            test_part = part + ch
                            if font.size(test_part)[0] <= max_width:
                                part = test_part
                            else:
                                if part:
                                    lines.append(part)
                                part = ch
                        current_line = part
            if current_line:
                lines.append(current_line)
        return lines

    def update(self, dt):
        # Lance le fade puis l'animation du joueur et du texte
        self.__update_fade(dt)
        self.__update_player_motion(dt)
        # la premiere ligne de texte étant init avec la classe on peut commencer a écrire
        self.__update_typing(dt)

    def __draw_dialog_box(self, surface):
        dialog_width = int(self.settings.GAME_SCREEN_WIDTH * 0.8)
        dialog_x = (self.settings.GAME_SCREEN_WIDTH - dialog_width) // 2

        if self.font:
            max_text_width = dialog_width - 2 * self.DIALOG_BOX_PADDING
            lines = self.__wrap_text(self.current_text, self.font, max_text_width)
            line_height = self.font.get_linesize()
            text_height = max(line_height, len(lines) * line_height)
            dialog_height = max(self.DIALOG_BOX_MIN_HEIGHT, text_height + 2 * self.DIALOG_BOX_PADDING)

            dialog_rect = pygame.Rect(
                dialog_x,
                self.settings.GAME_SCREEN_HEIGHT - dialog_height - self.DIALOG_BOX_BOTTOM_MARGIN,
                dialog_width,
                dialog_height,
            )

            self.__draw_dialog_background(surface, dialog_rect)
            self.__draw_dialog_text(surface, lines, dialog_rect, line_height)
            self.__draw_dialog_hint(surface, dialog_rect)

    def __draw_dialog_background(self, surface, dialog_rect):
        bg = pygame.Surface(dialog_rect.size, pygame.SRCALPHA)
        bg.fill(self.DIALOG_BOX_BG_COLOR)
        surface.blit(bg, dialog_rect.topleft)

    def __draw_dialog_text(self, surface, lines, dialog_rect, line_height):
        y = dialog_rect.y + self.DIALOG_BOX_PADDING
        for line in lines:
            text_surface = self.font.render(line, True, self.DIALOG_TEXT_COLOR)
            x = dialog_rect.centerx - text_surface.get_width() // 2
            surface.blit(text_surface, (x, y))
            y += line_height

    def __draw_dialog_hint(self, surface, dialog_rect):
        if self.allow_advance and not self.is_fading_out:
            hint_surface = self.font.render(self.DIALOG_HINT_TEXT, True, self.DIALOG_HINT_COLOR)
            x = dialog_rect.right - hint_surface.get_width() - self.DIALOG_HINT_MARGIN_X
            y = dialog_rect.bottom - hint_surface.get_height() - self.DIALOG_HINT_MARGIN_Y
            surface.blit(hint_surface, (x, y))

    def draw(self, surface):
        """dessine la scène, fade_layer + player + dialog_box"""
        surface.fill((0, 0, 0))
        camera = (0, 0)
        self.player.draw(surface, camera)
        self.__draw_dialog_box(surface)
        self.__draw_fade_layers(surface)

    def __draw_fade_layers(self, surface):
        if self.fade_in_alpha > 0:
            fade = pygame.Surface(self.screen_rect.size)
            fade.fill((0, 0, 0))
            fade.set_alpha(self.fade_in_alpha)
            surface.blit(fade, (0, 0))
        if self.is_fading_out and self.fade_out_alpha > 0:
            fade = pygame.Surface(self.screen_rect.size)
            fade.fill((0, 0, 0))
            fade.set_alpha(self.fade_out_alpha)
            surface.blit(fade, (0, 0))