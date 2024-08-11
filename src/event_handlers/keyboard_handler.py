from typing import List
import time

from pynput import keyboard
from events import KeyboardEvent


class KeyboardEventHandler:
    def __init__(self, duration: float = 0.01):
        self._event_list: List[KeyboardEvent] = []
        self._duration = duration
        self._recording = True
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )

    def _on_key_press(self, key):
        current_time = time.time()
        self._event_list.append(("key_press", str(key), current_time))

    def _on_key_release(self, key):
        current_time = time.time()
        self._event_list.append(("key_release", str(key), current_time))

    def start(self):
        self._event_list = []
        self._keyboard_listener.start()
        while self._recording:
            time.sleep(self._duration)

    def stop(self):
        self._recording = False
        self._keyboard_listener.stop()

    @property
    def events_list(self):
        return self._event_list
