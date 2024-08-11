from logging import getLogger
from ..config.recorder_config import Config


class HotKeysHandler:
    def __init__(self, config: Config):
        self.config = config
        self._logger = getLogger(__name__)

