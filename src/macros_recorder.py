from typing import Tuple, List

from src.config.recorder_config import Config


class MacrosRecorder:
    def __init__(self, config: Config):
        self.config = config

    def record_macro(self):
        pass

    def replay_macro(self, macro: List[Tuple]):
        pass
