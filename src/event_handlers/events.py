from typing import Tuple, Union

MouseEvent = Union[
    Tuple[str, int, int, float],
    Tuple[str, int, int, str, float],
    Tuple[str, int, int, int, int, float]
]

KeyboardEvent = Tuple[str, str, float]