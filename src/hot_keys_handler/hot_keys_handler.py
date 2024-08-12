import pprint
import threading
import time
from logging import getLogger

from pynput import keyboard
from ..config.recorder_config import Config
from ..sounds import Sounds
from ..event_handlers.event_handler import EventHandler


class HotKeysHandler:
    def __init__(
            self,
            config: Config,
            sounds: Sounds,
            event_handler: EventHandler
    ):
        self._logger = getLogger(__name__)
        self._config = config
        self._sounds = sounds
        self._event_handler = event_handler

        self._toggle_recording = config.hot_keys.toggle_recording
        self._exit_the_program = config.hot_keys.exit_the_program

        self._running = True
        self._recording = False
        self._recording_thread = None

    def _on_start_recording(self):
        print("_on_start_recording")
        self._recording_thread = threading.Thread(target=self._event_handler.start)
        self._recording_thread.start()
        self._logger.info("Recording from input devices has started.")
        self._sounds.play_start_sound()
        self._recording = True

    def _on_stop_recording(self):
        print("_on_stop_recording")
        if self._recording:
            self._event_handler.stop()
            if self._recording_thread:
                self._recording_thread.join()
            self._logger.info("Recording from input devices has stopped.")
            self._sounds.play_stop_sound()
            #
            # x = self._event_handler.get_last_macro()
            # pprint.pprint(x.filename)
            # pprint.pprint(x.mouse_events)
            # pprint.pprint(x.keyboard_evens)
            self._recording = False

    def _on_toggle_recording(self):
        if self._recording:
            self._on_stop_recording()
        else:
            self._on_start_recording()

    def _on_quit(self):
        self._logger.info("Terminating the program...")
        self._sounds.play_exit_sound()
        self._recording = False
        self._running = False  # Сигнал для завершения основного цикла.
        return False  # Прекращает слушать нажатия клавиш и завершает программу

    def start(self):
        try:
            with keyboard.GlobalHotKeys({
                self._toggle_recording: self._on_toggle_recording,
                self._exit_the_program: self._on_quit
            }) as hotkey_listener:
                while self._running:  # Добавляем условие завершения
                    time.sleep(0.1)
        finally:
            if self._recording_thread and self._recording_thread.is_alive():
                self._recording = False
                self._recording_thread.join()
