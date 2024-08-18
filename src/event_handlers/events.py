from typing import Tuple, Union, List
from dataclasses import dataclass
from enum import StrEnum

MouseEvent = Union[
    Tuple[str, int, int, float],
    Tuple[str, int, int, str, float],
    Tuple[str, int, int, int, int, float]
]

KeyboardEvent = Tuple[str, str, float]

AnyEvent = Union[KeyboardEvent, MouseEvent]


@dataclass
class Macro:
    filename: str
    event_list: List[Union[MouseEvent, KeyboardEvent]]


class Action(StrEnum):
    MOVE = "move",
    CLICK_DOWN = "click_down",
    CLICK_UP = "click_up",
    SCROLL = "scroll",
    KEY_PRESS = "key_press",
    KEY_RELEASE = "key_release"
