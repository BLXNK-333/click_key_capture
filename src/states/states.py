from .key_layout import switch_layout_generator, is_caps_lock_on


class States:
    def __init__(self):
        self._switch_layout_generator = switch_layout_generator()
        self.current_lang = next(self._switch_layout_generator)
        self.shift_pressed = False
        self.caps_pressed = is_caps_lock_on()

    def switch_to_next_layout(self):
        # Метод для переключения на следующую раскладку
        self.current_lang = next(self._switch_layout_generator)
        return self.current_lang
