import logging.config

from src.config.logging_config import logging_config
from src.config.recorder_config import load_config
from src.hot_keys_handler.hot_keys_handler import HotKeysHandler
from src.file_io.sounds import Sounds
from src.event_handlers.event_handler import EventHandler
from src.post_processing.post_processing import PostProcessing
from src.states.states import States


def main():
    config = load_config()
    states = States()
    sounds = Sounds(config=config)
    event_handler = EventHandler(config=config, states=states)
    post_processor = PostProcessing(config=config)

    hot_keys_handler = HotKeysHandler(
        config=config,
        sounds=sounds,
        event_handler=event_handler,
        post_processor=post_processor,
        states=states
    )

    hot_keys_handler.start()


if __name__ == '__main__':
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    logger.info("Start service.")

    main()

    logger.info("Stop service.")