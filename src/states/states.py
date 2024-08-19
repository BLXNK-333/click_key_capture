from .key_layout import switch_layout_generator, is_caps_lock_on


class States:
    def __init__(self):
        """
        Инициализирует объект States, который хранит состояния клавиатуры.
        Включает в себя:

        - Генератор переключения раскладки клавиатуры.
        - Текущую раскладку клавиатуры.
        - Состояние нажатия клавиши Shift.
        - Состояние включенности Caps Lock.
        """
        self._switch_layout_generator = switch_layout_generator()
        self.current_lang = next(self._switch_layout_generator)
        self.shift_pressed = False
        self.caps_pressed = is_caps_lock_on()

    def switch_to_next_layout(self) -> None:
        """
        Метод для переключения на следующую раскладку. Не влияет на
        настройки системы.

        :return: (None)
        """
        self.current_lang = next(self._switch_layout_generator)
        return self.current_lang
