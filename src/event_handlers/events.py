from typing import Tuple, Union, List
from dataclasses import dataclass

MouseEvent = Union[
    Tuple[str, int, int, float],
    Tuple[str, int, int, str, float],
    Tuple[str, int, int, int, int, float]
]

KeyboardEvent = Tuple[str, str, float]


@dataclass
class Macro:
    filename: str
    mouse_events: List[MouseEvent]
    keyboard_evens: List[KeyboardEvent]
