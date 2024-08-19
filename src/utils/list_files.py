import os.path


def list_all_files(directory: str, ext: str):
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


def interactive_selection(directory: str, ext: str):
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
