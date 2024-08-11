import subprocess
import threading

from .config.recorder_config import Config


class Sounds:
    def __init__(self, config: Config):
        """
        Воспроизводит звуки, в отдельном процессе, не блокируя основной поток.
        :param config: (Config) Принимает аргумент, класс конфигурации.
        """
        self._start_sound = config.paths.start_sound
        self._stop_sound = config.paths.stop_sound
        self._exit_sound = config.paths.exit_sound

    def _playsound(self, filepath: str) -> threading.Thread:
        def run_sound():
            subprocess.run(
                ['ffplay', '-nodisp', '-autoexit', filepath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        sound_thread = threading.Thread(target=run_sound)
        sound_thread.start()
        return sound_thread

    def play_start_sound(self):
        self._playsound(self._start_sound)

    def play_stop_sound(self):
        self._playsound(self._stop_sound)

    def play_exit_sound(self):
        self._playsound(self._exit_sound)
