from typing import Tuple, Union, List
from dataclasses import dataclass

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
