import pprint
import threading
import time
from logging import getLogger

from pynput import keyboard
from ..config.recorder_config import Config
from ..file_io.sounds import Sounds
from ..event_handlers.event_handler import EventHandler
from ..post_processing.post_processing import PostProcessing
from ..states.states import States


class HotKeysHandler:
    def __init__(
            self,
            config: Config,
            sounds: Sounds,
            event_handler: EventHandler,
            post_processor: PostProcessing,
            states: States
    ):
        self._logger = getLogger(__name__)
        self._config = config
        self._sounds = sounds
        self._event_handler = event_handler
        self._post_processor = post_processor
        self._states = states

        self._toggle_recording = config.hot_keys.toggle_recording
        self._exit_the_program = config.hot_keys.exit_the_program
        self._switch_layout = config.hot_keys.switch_layout

        self._running = True
        self._recording = False
        self._recording_thread = None

    def _on_start_recording(self):
        print("_on_start_recording")
        self._recording_thread = threading.Thread(target=self._event_handler.start)
        self._logger.info("Recording from input devices has started.")
        self._sounds.play_start_sound()
        self._recording = True
        self._recording_thread.start()

    def _on_stop_recording(self):
        print("_on_stop_recording")
        if self._recording:
            self._event_handler.stop()
            if self._recording_thread:
                self._recording_thread.join()
            self._logger.info("Recording from input devices has stopped.")
            #
            # x = self._event_handler.get_last_macro()
            # pprint.pprint(x.filename)
            # pprint.pprint(x.event_list)
            last_macro = self._event_handler.get_last_macro()
            self._post_processor.put_macro(last_macro)
            self._sounds.play_stop_sound()
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

    def _on_switch_layout(self):
        self._states.switch_to_next_layout()

    def start(self):
        try:
            with keyboard.GlobalHotKeys({
                self._toggle_recording: self._on_toggle_recording,
                self._exit_the_program: self._on_quit,
                self._switch_layout: self._on_switch_layout
            }) as hotkey_listener:
                while self._running:  # Добавляем условие завершения
                    time.sleep(0.1)
        finally:
            if self._recording_thread and self._recording_thread.is_alive():
                self._recording = False
                self._recording_thread.join()
            self._post_processor.wait_macro_processing()
