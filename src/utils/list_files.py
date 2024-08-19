import os.path
from typing import Optional, Dict


def list_all_files(directory: str, ext: str) -> Dict[int, str]:
    ext = "." + ext.strip(",.")
    file_dict, cnt = {}, 1
    for root, _, files in os.walk(directory):
        for file in files:
            # Формируем полный путь к файлу
            if file.endswith(ext):
                file_path = os.path.join(root, file)
                file_dict[cnt] = file_path

                cnt += 1
    if file_dict:
        print("List of macros:")
        for cnt, file_path in file_dict.items():
            print(f"{(str(cnt)+')').ljust(4)}{file_path}")
    return file_dict


def interactive_selection(directory: str, ext: str) -> Optional[str]:
    """
    Функция для интерактивного диалога с пользователем, где он
    может выбрать макрос для воспроизведения.

    :param directory: (str) Путь к каталогу с макросами.
    :param ext: (str) Указывает на то, с какими расширениями,
        выводить файлы на экран. Например, если передать txt,
        сделает рекурсивный обход и выведет все файлы с расширением "txt".
    :return: (Optional[str]) Путь к файлу или None.
    """
    files = list_all_files(directory, ext)
    if not files:
        print(f"There are no recorded macros in the directory {directory}")
        return None

    choice = input("\nEnter the macro number to play: ")
    if choice.isdigit():
        choice = int(choice)
        if choice in files:
            return files[choice]
    else:
        print("This key is not in the list")
        return None
