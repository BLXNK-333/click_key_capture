from datetime import datetime
import time
from pynput import mouse, keyboard
from pynput.keyboard import Key

from .events import Macro
from ..config.recorder_config import Config
from ..states.states import States


class EventHandler:
    def __init__(self, config: Config, states: States):
        self._event_list = []
        self._current_marco_name: str = ""
        self._delay = config.settings.delay
        self._mouse_record = config.settings.mouse_record
        self._keyboard_record = config.settings.keyboard_record
        self.states = states

        self._mouse_listener = None
        self._keyboard_listener = None

    def _on_move(self, x: int, y: int) -> None:
        current_time = time.time()
        self._event_list.append(("move", x, y, current_time))

    def _on_click(self, x: int, y: int, button: str, pressed: str) -> None:
        action = "click_down" if pressed else "click_up"
        button_type = str(button).split('.')[-1]
        current_time = time.time()
        self._event_list.append((action, x, y, button_type, current_time))

    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        current_time = time.time()
        self._event_list.append(("scroll", x, y, dx, dy, current_time))

    def __on_key(self, key, event_type: str) -> None:
        current_time = time.time()
        if isinstance(key, Key):
            key_str = key.name
            if key == Key.shift:
                self.states.shift_pressed = not self.states.shift_pressed
            elif key == Key.caps_lock and event_type.endswith("s"):
                self.states.caps_pressed = not self.states.caps_pressed
        else:
            key_str = str(key)
            if self.states.shift_pressed or self.states.caps_pressed:
                key_str = key_str.upper()
            print(key_str)
        self._event_list.append((event_type, key_str, current_time))

    def _on_key_press(self, key) -> None:
        self.__on_key(key, "key_press")

    def _on_key_release(self, key) -> None:
        self.__on_key(key, "key_release")

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
            time.sleep(0.15)
            self._mouse_listener.stop()

        if self._keyboard_listener:
            time.sleep(0.15)
            self._keyboard_listener.stop()

    def get_last_macro(self) -> Macro:
        """
        Функция возвращает последний записанный макрос, в виде объекта Macro.
        """
        return Macro(
            filename=self._current_marco_name,
            event_list=self._event_list
        )
