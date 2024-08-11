from typing import Dict, Union, List

from .config.recorder_config import Config
from .event_handlers.events import KeyboardEvent, MouseEvent


class PostProcessing:
    def __init__(self, config: Config):
        self._trim_idle = config.settings.trim_idle
        self._stack_time = config.settings.stack_time
        # KeyboardEvent, MouseEvent - это просто кортежи,
        # с различным возможным, содержимым.
        self._processed_macro: Dict[str, List[Union[KeyboardEvent, MouseEvent]]] = {}

    def _execute_trim_idle(self):
        """
        Обрезает начало записи движений мыши, где мышь не двигалась.
        """
        # TODO Логику работы тут нужно переделать, чтобы корректно
        #  работала для различных типов событий.
        strip_macro = {}
        for event_type, macro in self._processed_macro.items():
            n = len(macro)
            if n > 1:
                idx = jdx = 0
                for i in range(n - 1):
                    # Здесь сравнивает, координаты [x, y] мыши с соседом
                    if macro[i][:3] != macro[i + 1][:3]:
                        idx = i
                        break
                for j in range(n - 1, 0, -1):
                    if macro[j][:3] != macro[j - 1][:3]:
                        jdx = j
                        break
                if idx < jdx:
                    strip_macro[event_type] = macro[idx : jdx + 1]
        self.macros = strip_macro

    def _execute_stack_time(self):
        pass

    def _calculate_delay_between_events(self):
        pass

    def execute(self, macro):
        self._processed_macro = macro
        pass
