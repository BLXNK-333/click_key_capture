from typing import List
import time

from pynput import mouse
from .events import MouseEvent


class MouseEventHandler:
    def __init__(self, duration: float = 0.01):
        self._event_list: List[MouseEvent] = []
        self._duration = duration
        self._recording = True

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

    def start(self):
        _mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self._event_list = []
        _mouse_listener.start()
        while self._recording:
            time.sleep(self._duration)

    def stop(self):
        self._recording = False

    @property
    def events_list(self):
        return self._event_list
