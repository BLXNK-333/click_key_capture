import logging
from typing import List
import time
import traceback

from pynput import keyboard
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

from ..config.recorder_config import Config
from ..event_handlers.events import AnyEvent, Action


class EventReplay:
    def __init__(self, config: Config):
        """
        Класс представляет собой проигрыватель макросов. Иногда возникают
        ошибки при "воспроизведении" кириллицы.

        :param config: (Config) DataClass с настройками.
        """
        self._logger = logging.getLogger(__name__)
        self._replay_delay = config.settings.delay_before_playback
        self._mouse_controller = MouseController()
        self._keyboard_controller = KeyboardController()
        self._running = True

        # Словарь, сопоставляющий тип события с методом воспроизведения
        self._event_handlers = {
            Action.MOVE: self._play_mouse_move,
            Action.CLICK_DOWN: self._play_mouse_down,
            Action.CLICK_UP: self._play_mouse_up,
            Action.SCROLL: self._play_mouse_scroll,
            Action.KEY_PRESS: self._play_key_press,
            Action.KEY_RELEASE: self._play_key_release,
        }

        # Добавление горячих клавиш для Ctrl+C
        self._hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+c': self._stop_and_exit
        })

    def set_replay_delay(self, delay: int) -> None:
        """
        Можно изменить настройки после задержки перед воспроизведением
        макроса после инициализации класса.

        :param delay: (int) Задержка перед воспроизведением.
        :return: (None)
        """
        self._replay_delay = delay

    def _stop_and_exit(self):
        self._logger.debug("Stop signal received..")
        self._hotkey_listener.stop()
        self._release_resources()
        self._running = False

    def _release_resources(self):
        """
        Отжимает клавиши, чтобы избежать негативных эффектов, после воспроизведения.
        """
        try:
            for key in (Key.shift, Key.ctrl, Key.alt):
                self._keyboard_controller.release(key)
        except Exception as e:
            self._logger.error(f"Error releasing keyboard keys: {e}")

        try:
            for button in (Button.left, Button.right, Button.middle):
                self._mouse_controller.release(button)
        except Exception as e:
            self._logger.error(f"Error releasing mouse buttons: {e}")

    def _play_mouse_move(self, x, y):
        self._mouse_controller.position = (x, y)

    def _play_mouse_down(self, x, y, button):
        self._mouse_controller.position = (x, y)
        button_obj = getattr(Button, button)
        self._mouse_controller.press(button_obj)

    def _play_mouse_up(self, x, y, button):
        self._mouse_controller.position = (x, y)
        button_obj = getattr(Button, button)
        self._mouse_controller.release(button_obj)

    def _play_mouse_scroll(self, x, y, dx, dy):
        self._mouse_controller.position = (x, y)
        self._mouse_controller.scroll(dx, dy)

    def _play_key_press(self, key):
        if key.startswith("Key."):
            key = getattr(Key, key.split('.')[1])
        self._keyboard_controller.press(key)

    def _play_key_release(self, key):
        if key.startswith("Key."):
            key = getattr(Key, key.split('.')[1])
        self._keyboard_controller.release(key)

    def play_events(self, event_list: List[AnyEvent]) -> None:
        """
        Воспроизводит события с устройств ввода.

        :param event_list: Список с событиями с устройств ввода.
        :return: (None)
        """
        if not event_list:
            self._logger.info("No events to play.")
            return

        self._hotkey_listener.start()
        self._logger.info(
            f"Replay will start after a delay of {self._replay_delay} seconds ...")
        time.sleep(self._replay_delay)
        self._logger.info("Start replay.")
        try:
            for event in event_list:
                if not self._running:
                    break
                event_type, *args, delay = event
                self._event_handlers[event_type](*args)
                time.sleep(delay)
        except KeyError:
            traceback.print_exc()
        finally:
            self._release_resources()
            self._logger.info("Playback finished.")
