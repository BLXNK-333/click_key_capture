from datetime import datetime
import time
from pynput import mouse, keyboard

from .events import Macro
from ..config.recorder_config import Config


class EventHandler:
    def __init__(self, config: Config):
        self._event_list = []
        self._current_marco_name: str = ""
        self._duration = config.settings.duration
        self._mouse_record = config.settings.mouse_record
        self._keyboard_record = config.settings.keyboard_record

        self._mouse_listener = None
        self._keyboard_listener = None

    def _on_move(self, x, y):
        current_time = time.time()
        self._event_list.append(("move", x, y, current_time))

    def _on_click(self, x, y, button, pressed):
        action = "click_down" if pressed else "click_up"
        button_type = str(button).split('.')[-1]
        current_time = time.time()
        self._event_list.append((action, x, y, button_type, current_time))

    def _on_scroll(self, x, y, dx, dy):
        current_time = time.time()
        self._event_list.append(("scroll", x, y, dx, dy, current_time))

    def _on_key_press(self, key):
        current_time = time.time()
        self._event_list.append(("key_press", str(key), current_time))

    def _on_key_release(self, key):
        current_time = time.time()
        self._event_list.append(("key_release", str(key), current_time))

    def start(self):
        self._event_list = []
        self._current_marco_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]

        if self._mouse_record:
            self._mouse_listener = mouse.Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll
            )
            self._mouse_listener.start()

        if self._keyboard_record:
            self._keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self._keyboard_listener.start()

    def stop(self):
        if self._mouse_listener:
            self._mouse_listener.stop()

        if self._keyboard_listener:
            self._keyboard_listener.stop()

    def get_last_macro(self) -> Macro:
        """
        Функция возвращает последний записанный макрос, в виде объекта Macro.
        """
        return Macro(
            filename=self._current_marco_name,
            event_list=self._event_list
        )
