from dataclasses import dataclass
from recorder_settings import recorder_settings


@dataclass
class Config:
    path_to_start_sound: str
    path_to_stop_sound: str
    path_to_exit_sound: str
    path_to_macros_directory: str
    hot_key_start_record: str
    hot_key_stop_record: str
    hot_key_exit_the_program: str


def load_config():
    return Config(
        path_to_start_sound=recorder_settings["path_to_start_sound"],
        path_to_stop_sound=recorder_settings["path_to_stop_sound"],
        path_to_exit_sound=recorder_settings["path_to_exit_sound"],
        path_to_macros_directory=recorder_settings["path_to_macros_directory"],
        hot_key_start_record=recorder_settings["hot_key_start_record"],
        hot_key_stop_record=recorder_settings["hot_key_stop_record"],
        hot_key_exit_the_program=recorder_settings["hot_key_exit_the_program"]
    )