from typing import Optional

from .config.recorder_config import Config
from .hot_keys_handler.hot_keys_handler import HotKeysHandler
from .file_io.sounds import Sounds
from .event_handlers.event_handler import EventHandler
from .post_processing.post_processing import PostProcessing
from .states.states import States
from .event_replay.replay import EventReplay
from .file_io.file_io import read_macro


def record_macro(
    config: Config,
    rec_mouse: bool = True,
    rec_keyboard: bool = True
) -> None:
    """
    Функция запускает скрипт, для записи макроса.

    :param config: (Config) DataClass с конфигурацией.
    :param rec_mouse: (bool) Указывает, следует ли записывать события мыши.
    :param rec_keyboard: (bool) Указывает, следует ли записывать события клавиатуры.
    :return: (None)
    """
    states = States()
    sounds = Sounds(config=config)
    event_handler = EventHandler(config=config, states=states)
    event_handler.set_settings(rec_mouse=rec_mouse, rec_keyboard=rec_keyboard)
    post_processor = PostProcessing(config=config)

    hot_keys_handler = HotKeysHandler(
        config=config,
        sounds=sounds,
        event_handler=event_handler,
        post_processor=post_processor,
        states=states
    )

    hot_keys_handler.start()


def play_macro(
    config: Config,
    macro_path: str,
    delay: Optional[int] = None
) -> None:
    """
    Функция запускает скрипт, для воспроизведения макроса.

    :param config: (Config) DataClass с конфигурацией.
    :param macro_path: (str) Путь к макросу.
    :param delay: (int) Необязательный аргумент, задержка перед
        воспроизведением, в секундах.
    :return: (None)
    """
    macro = read_macro(macro_path)

    if macro:
        replayer = EventReplay(config)
        if delay is not None:
            replayer.set_replay_delay(delay)

        replayer.play_events(macro)
