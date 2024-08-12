from typing import Optional, Tuple, List, Dict
from datetime import datetime
import threading

from .keyboard_handler import KeyboardEventHandler
from .mouse_handler import MouseEventHandler
from .events import Macro


class EventHandler:
    def __init__(
            self,
            duration: float = 0.01,
            mouse_record: bool = True,
            keyboard_record: bool = True
    ):
        self._macros = {}
        self._current_marco_name: str = ""
        self._mouse_handler = MouseEventHandler(duration) if mouse_record else None
        self._keyboard_handler = KeyboardEventHandler(
            duration) if keyboard_record else None
        self._mouse_thread: Optional[threading.Thread] = None
        self._keyboard_thread: Optional[threading.Thread] = None

    def start(self):
        self._current_marco_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]

        # Пересоздаем только потоки для обработчиков
        if self._mouse_handler:
            self._mouse_thread = threading.Thread(target=self._mouse_handler.start)
            self._mouse_thread.start()

        if self._keyboard_handler:
            self._keyboard_thread = threading.Thread(target=self._keyboard_handler.start)
            self._keyboard_thread.start()

    def stop(self):
        # Останавливаем обработчики
        if self._mouse_handler:
            self._mouse_handler.stop()
            self._mouse_thread.join()

        if self._keyboard_handler:
            self._keyboard_handler.stop()
            self._keyboard_thread.join()

        self._macros[self._current_marco_name] = Macro(
            filename=self._current_marco_name,
            mouse_events=self._mouse_handler.events_list,
            keyboard_evens=self._keyboard_handler.events_list
        )

    def get_last_macro(self) -> Macro:
        """
        Функция возвращает последний записанный макрос, в виде объекта Macro.
        """
        return self._macros[self._current_marco_name]
