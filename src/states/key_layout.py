from typing import List
import subprocess
import ast
import logging

logger = logging.getLogger(__name__)


def execute_gsettings_command(schema: str, key: str) -> str:
    """
    Выполняет команду gsettings для получения значения указанного ключа
    из заданной схемы и возвращает результат в виде строки.

    :param schema: Схема настроек GNOME
    :param key: Ключ для получения значения
    :return: Значение ключа в виде строки
    :raises: CalledProcessError если команда не выполнена успешно
    """
    try:
        result = subprocess.run(
            ['gsettings', 'get', schema, key],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        # Декодируем вывод команды
        output = result.stdout.decode().strip()
        logger.debug(f"gsettings output for schema '{schema}', key '{key}': {output}")
        return output

    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing gsettings command: {e}")
        raise  # Повторное возбуждение исключения для обработки его выше по цепочке


def get_keyboard_layouts() -> List[str]:
    """
    Возвращает раскладки клавиатуры из настроек GNOME
    в виде списка ["ru", "us"].

    :return: Список раскладок клавиатуры
    :raises: Exception если происходит ошибка в процессе получения раскладок
    """
    schema = "org.gnome.desktop.input-sources"
    key = "mru-sources"
    try:
        gsettings_output = execute_gsettings_command(schema, key)
        sources_list = ast.literal_eval(gsettings_output)
        if sources_list:
            _layouts = [lo[1] for lo in sources_list]
            logger.debug(f"Keyboard layouts: {_layouts}")
            return _layouts
        else:
            logger.error("Empty sources list returned from gsettings command")
            raise ValueError

    except Exception as e:
        logger.error(f"An error occurred while retrieving keyboard layouts: {e}", exc_info=True)
        raise


def switch_layout_generator():
    """
    Функция генератор. Должна вызываться в хэндлере, который
    отслеживает хот-кеи системы, для переключения языка. Внутри
    генератора, переключение происходит внутри своей коробочки, и
    ни как не влияет на настройки gnome. Нужно, чтобы экономить ресурс
    и не запрашивать каждый раз вызов нового процесса.
    """
    _lang_layouts = get_keyboard_layouts()
    n, i = len(_lang_layouts), 0
    while True:
        yield _lang_layouts[i]
        i = (i + 1) % n


def is_caps_lock_on() -> bool:
    """
    Команда проверяет включен ли caps lock. Вызовет исключение если,
    не получит результат.
    """
    try:
        result = subprocess.run(
            ["bash", "-c", "xset q | grep 'Caps Lock' | awk '{print $4}'"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()

        if output not in {"on", "off"}:
            logger.error(f"Parsing error: expected 'on' or 'off', but got '{output}'")
            raise ValueError(f"Unexpected output from command: '{output}'")

        return output == "on"
    except subprocess.CalledProcessError as e:
        # Логируем полный трейсбек ошибки
        logger.error("An error occurred while checking Caps Lock status", exc_info=True)
        raise
