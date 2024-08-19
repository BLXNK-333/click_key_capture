import pprint
from typing import List, Set
from src.event_handlers.events import AnyEvent, Action


def convert_time_to_delays(events: List[AnyEvent]):
    """
    Заменяет временную метку события на задержку относительно
    времени наступления предыдущего события.
    """
    if not events:
        return []

    converted = []

    for current, next_event in zip(events, events[1:]):
        *data, cur_time = current
        next_time = next_event[-1]
        delay = next_time - cur_time
        converted.append((*data, delay))

    return converted


def remove_unpaired_up_events(events: List[AnyEvent]):
    cleaned_events = []
    untracked = {Action.MOVE, Action.SCROLL}
    pressed = set()

    for event in events:
        _type = event[0]
        if _type in untracked:
            cleaned_events.append(event)
            continue

        if _type.startswith("key"):
            button = event[1]
            if _type == Action.KEY_PRESS:
                cleaned_events.append(event)
                pressed.add(button)
            elif _type == Action.KEY_RELEASE and button in pressed:
                cleaned_events.append(event)
                pressed.remove(button)
        else:
            if len(event) >= 4 and isinstance(event[3], (str, int)):
                button = event[3]
                _key = "click_" + str(button)
                if _type == Action.CLICK_DOWN:
                    cleaned_events.append(event)
                    pressed.add(_key)
                elif _key in pressed:
                    cleaned_events.append(event)
                    pressed.remove(_key)

    return cleaned_events, pressed


def remove_unpaired_down_events(events: List[AnyEvent], pressed: Set[str]):
    if not pressed:
        return events

    cleaned_events = []
    untracked = {Action.MOVE, Action.SCROLL}

    for event in reversed(events):
        _type = event[0]

        if _type in untracked:
            cleaned_events.append(event)
            continue

        if _type.startswith("key"):
            button = event[1]
            if _type == Action.KEY_PRESS and button in pressed:
                pressed.remove(button)
            else:
                cleaned_events.append(event)
        else:
            if len(event) >= 4 and isinstance(event[3], (str, int)):
                button = event[3]
                _key = f"click_{button}"
                if _type == Action.CLICK_DOWN and _key in pressed:
                    pressed.remove(_key)
                else:
                    cleaned_events.append(event)

    return cleaned_events[::-1]


def cleanup_unpaired_events(events: List[AnyEvent]):
    """
    Удаляет из трека события нажатий и отпусканий клавиш клавиатуры или кликов мыши,
    которые не имеют пары. Например, если клавиша была нажата, но не отжата до
    конца макроса, или наоборот.
    """
    return remove_unpaired_down_events(*remove_unpaired_up_events(events))


def _get_rightmost_hot_corner_event_index(events):
    for i in range(len(events) - 1, -1, -1):
        event = events[i][0]
        if event == Action.CLICK_UP:
            return i
    return 0


def get_hot_corner_insert_indices(events):
    i, n = 0, len(events)
    click_down = False
    click_after_indices = []
    candidate = -1
    rightmost_hot_event_index = _get_rightmost_hot_corner_event_index(events)

    for i in range(n):
        event = events[i]
        action = event[0]

        if action == Action.MOVE:
            x, y = event[1], event[2]
            if not x and not y:
                if candidate < 0:
                    candidate = i
                continue
            if not click_down or candidate > rightmost_hot_event_index:
                click_after_indices.append(candidate)
            click_down = False
            candidate = -1

        elif action == Action.CLICK_DOWN:
            click_down = True
        elif action == Action.KEY_PRESS:
            if event[1] == "Key.esc":
                if candidate > -1:
                    click_after_indices.append(candidate)
                click_down = False
                candidate = -1

    if -1 < candidate < rightmost_hot_event_index:
        click_after_indices.append(candidate)

    return click_after_indices


def insert_hot_corner_activate(events: List[AnyEvent]):
    """
    Обрабатывает последовательность событий, добавляя активацию горячего
    угла при перемещении мыши в координаты (0, 0) и изменяя время задержки
    следующего события.
    """
    indices = set(get_hot_corner_insert_indices(events))
    if not indices:
        return events
    result = []
    indices = set(indices)

    for i, event in enumerate(events):
        result.append(event)
        if i in indices:
            result.extend([
                (Action.KEY_PRESS, "Key.cmd", 0.0),
                (Action.KEY_RELEASE, "Key.cmd", 0.0)
                ])
    return result


def post_process_input_events(events: List[AnyEvent]) -> List[AnyEvent]:
    """
    Функция выполняет постобработку событий, записанных с устройств ввода.
    1. Конвертирует время в задержки.
    2. Складывает задержки одинаковых соседних событий.
    3. Удаляет не парные события (нажатия и отжатия).
    4. Добавляет активацию горячего угла при перемещении мыши в координаты (0, 0).

    :param events: Записанный макрос.
    :return: Обработанный макрос.
    """
    return insert_hot_corner_activate(
        cleanup_unpaired_events(
                convert_time_to_delays(events)
                )
            )
