from datetime import datetime
import time

from pynput import mouse, keyboard
from pynput.keyboard import Key

from .events import Macro, Action
from ..config.recorder_config import Config
from ..states.states import States
from ..states.decode import decode_map


class EventHandler:
    def __init__(self, config: Config, states: States):
        """
        Класс представляет логику обработки, а конкретнее записи событий
        приходящих с устройств ввода, такие как клики мыши, скролл, движения,
        нажатия клавиш клавиатуры.

        :param config: (Config) Dataclass с настройками.
        :param states: (States) Класс с состояниями.
        """
        self._event_list = []
        self._current_marco_name: str = ""
        self._delay = config.settings.delay
        self._mouse_record = config.settings.mouse_record
        self._keyboard_record = config.settings.keyboard_record
        self._states = states

        self._mouse_listener = None
        self._keyboard_listener = None

    def set_settings(self, rec_mouse: bool, rec_keyboard: bool):
        """
        Можно изменить настройки записи событий после инициализации.
        :param rec_mouse: (bool) Указывает, записывать мышь или нет.
        :param rec_keyboard: (bool) Указывает, записывать клавиатуру или нет.
        :return:
        """
        self._mouse_record = rec_mouse
        self._keyboard_record = rec_keyboard

    def _on_move(self, x: int, y: int) -> None:
        current_time = time.time()
        self._event_list.append((Action.MOVE, x, y, current_time))

    def _on_click(self, x: int, y: int, button: str, pressed: str) -> None:
        action = Action.CLICK_DOWN if pressed else Action.CLICK_UP
        button_type = str(button).split('.')[-1]
        current_time = time.time()
        self._event_list.append((action, x, y, button_type, current_time))

    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        current_time = time.time()
        self._event_list.append((Action.SCROLL, x, y, dx, dy, current_time))

    def __on_key(self, key, event_type: Action) -> None:
        current_time = time.time()
        if isinstance(key, Key):
            key_str = key
            if key == Key.shift:
                self._states.shift_pressed = not self._states.shift_pressed
            elif key == Key.caps_lock and event_type.endswith("s"):
                self._states.caps_pressed = not self._states.caps_pressed
        else:
            code = key.vk

            if code in decode_map:
                cur_lang = self._states.current_lang
                _case = "lower"
                if self._states.shift_pressed or self._states.caps_pressed:
                    _case = "upper"
                key_str = decode_map[code][cur_lang][_case]
            else:
                key_str = str(key)
            # if event_type == "key_press": # для теста
            #     print(f"press_key: {key_str}, key.vk: {code}   ", end="")
        self._event_list.append((event_type, key_str, current_time))

    def _on_key_press(self, key) -> None:
        self.__on_key(key, Action.KEY_PRESS)

    def _on_key_release(self, key) -> None:
        # if not isinstance(key, Key): # для теста
        #     print()
        self.__on_key(key, Action.KEY_RELEASE)

    def start(self) -> None:
        """
        Запускает обработчики событий мыши и клавиатуры.
        :return: (None)
        """
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

    def stop(self) -> None:
        """
        Останавливает обработчики событий мыши и клавиатуры.
        :return: (None)
        """
        if self._mouse_listener:
            self._mouse_listener.stop()

        if self._keyboard_listener:
            self._keyboard_listener.stop()
        time.sleep(0.15)

    def get_last_macro(self) -> Macro:
        """
        Функция возвращает последний записанный макрос, в виде объекта Macro.
        """
        return Macro(
            filename=self._current_marco_name,
            event_list=self._event_list
        )
