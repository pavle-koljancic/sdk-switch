import inspect
import logging
from logging import Logger
from logging import LogRecord

from conductor.client.context.task_context import TaskContext
from conductor.client.context.task_context import get_task_context


class ConductorHandler(logging.Handler):
    def emit(self, record: LogRecord) -> None:
        context: TaskContext = get_task_context()
        msg = self.format(record)
        context.add_log(msg)


def get_task_logger() -> Logger:
    frame = inspect.currentframe()
    if frame is None or frame.f_back is None:
        raise RuntimeError("Unable to determine caller module")

    try:
        module_name = frame.f_back.f_globals["__name__"]
    finally:
        del frame
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    handler = ConductorHandler()
    logger.addHandler(handler)
    return logger
