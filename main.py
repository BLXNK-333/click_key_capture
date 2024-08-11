import logging.config

from src.config.logging_config import logging_config
from src.config.recorder_config import load_config
from src.hot_keys_handler.hot_keys_handler import HotKeysHandler
from src.sounds import Sounds
from src.event_handlers.event_handler import EventHandler


def main():
    config = load_config()
    sounds = Sounds(config=config)
    event_handler = EventHandler()

    hot_keys_handler = HotKeysHandler(
        config=config,
        sounds=sounds,
        event_handler=event_handler
    )

    hot_keys_handler.start()


if __name__ == '__main__':
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    logger.info("Start service.")

    main()

    logger.info("Stop service.")