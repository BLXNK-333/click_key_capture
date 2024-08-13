from typing import Tuple, Union, List
from dataclasses import dataclass

MouseEvent = Union[
    Tuple[str, str, int, int, float],
    Tuple[str, str, int, int, str, float],
    Tuple[str, str, int, int, int, int, float]
]

KeyboardEvent = Tuple[str, str, str, float]


@dataclass
class Macro:
    filename: str
    event_list: List[Union[MouseEvent, KeyboardEvent]]
