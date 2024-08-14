from typing import Optional
import subprocess
import ast


def execute_gsettings_command(schema: str, key: str) -> Optional[str]:
    """
    Выполняет команду gsettings для получения значения указанного ключа
    из заданной схемы и возвращает результат в виде строки.

    :param schema: Схема настроек GNOME
    :param key: Ключ для получения значения
    :return: Значение ключа в виде строки, или None в случае ошибки
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
        return output

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
        return None


def get_active_keyboard_layout() -> Optional[str]:
    """
    Получает текущую активную раскладку клавиатуры из настроек GNOME
    и возвращает её буквенный код, например "ru" или "us".

    :return: Буквенный код текущей раскладки клавиатуры, или None в случае ошибки
    """
    schema = "org.gnome.desktop.input-sources"
    key = "mru-sources"
    try:
        gsettings_output = execute_gsettings_command(schema, key)
        if gsettings_output:
            sources_list = ast.literal_eval(gsettings_output)

            # Получаем первую раскладку в списке (текущую активную раскладку)
            if sources_list:
                current_layout = sources_list[0][1]
                return current_layout

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
