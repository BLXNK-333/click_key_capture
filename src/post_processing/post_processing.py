import logging
import multiprocessing

from ..config.recorder_config import Config
from ..event_handlers.events import Macro
from ..file_io.file_io import write_macro
from .processing_functions import post_process_input_events


class PostProcessing:
    def __init__(self, config: Config):
        """
        В конструкторе класса запускается отдельный процесс, для постобработки.
        Требует обязательного вызова, метода wait_macro_processing в конце
        работы, чтобы освободить ресурсы.
        :param config: (Config) Объект конфигурации.
        """
        self._logger = logging.getLogger(__name__)
        self._toggle_recording_key = config.hot_keys.toggle_recording
        self._macros_directory = config.paths.macros_directory
        self._macro_queue = multiprocessing.Queue()
        self._post_processor = self.__start_post_process()

    def __process_macro(self, macro: Macro):
        """
        Функция обрабатывает макрос, в соответствии с настройками из
        конфигурации.
        """
        _post_event_list = post_process_input_events(macro.event_list)
        if _post_event_list:
            write_macro(
                filename=macro.filename,
                data=_post_event_list,
                path=self._macros_directory
            )

    def __process_tasks(self):
        """Процесс, который обрабатывает задачи из очереди."""
        try:
            while True:
                task = self._macro_queue.get()
                if task is None:
                    break
                self.__process_macro(task)
        except KeyboardInterrupt:
            pass

    def __start_post_process(self):
        processor = multiprocessing.Process(target=self.__process_tasks)
        processor.start()
        return processor

    def put_macro(self, macro: Macro):
        """
        Функция, для постобработки записанного макроса.
        :param macro: (Macro) Макрос, который нужно обработать.
        """
        self._macro_queue.put(macro)

    def wait_macro_processing(self):
        """
        Функция посылает сигнал завершения процессу постобработки,
        и ждет его завершения. Нужно обязательно вызвать в конце программы,
        чтобы освободить ресурсы.
        """
        self._macro_queue.put(None)
        self._logger.info("Waiting for post-processing task to terminate...")
        self._post_processor.join()  # Ждем завершения процесса постобработки
        self._logger.info("Post-processing task has terminated.")
