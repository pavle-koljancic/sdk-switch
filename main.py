import os
from pathlib import Path

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from dotenv import load_dotenv

from task_logging.task_execution_logger import TaskExecutionLogger


def main() -> None:
    env_path = Path("config") / ".env"
    load_dotenv(dotenv_path=env_path)

    base_url = os.environ.get("CONDUCTOR_URL_BASE")
    config = Configuration(base_url=base_url)

    event_listeners = [TaskExecutionLogger()]
    import_modules: list[str] = []
    with TaskHandler(
        configuration=config,
        scan_for_annotated_workers=True,
        import_modules=import_modules,
        event_listeners=event_listeners,
    ) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == "__main__":
    main()
