import os
from pathlib import Path

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from dotenv import load_dotenv

from helper.utils import check_env_vars
from task_logging.task_execution_logger import TaskExecutionLogger


def validate_env() -> None:
    # Load environment variables from config/.env
    env_path = Path("config") / ".env"
    load_dotenv(dotenv_path=env_path)

    # Ensure required environment variables are set
    check_env_vars(
        [
            "CONDUCTOR_URL_BASE",
            "OPENFB_DB_USER",
            "OPENFB_DB_PASSWORD",
            "OPENFB_DB_NAME",
            "OPENFB_DB_HOST",
            "OPENFB_NSO_USER",
            "OPENFB_NSO_PASSWORD",
            "OPENFB_NSO_HOST",
            "OPENFB_NSO_PORT",
            "OPENFB_ACCEADIAN_USER",
            "OPENFB_ACCEADIAN_PASSWORD",
            "OPENFB_ACCEADIAN_HOST",
            "OPENFB_ACCEADIAN_PORT",
            "HUAWEI_SERVICES_INTERFACES_CSV_FILE",
            "HUAWEI_SERVICES_INTERFACES_VPLS_CSV_FILE",
            "SIAE_UNI_CSV_FILE",
            "SIAE_ALL_SERVICES_CSV_FILE",
            "HUAWEI_LAG_CSV_FILE",
            "NETH_INTERFACES_CSV_FILE",
            "HUAWEI_MEID_CSV_FILE",
            "TR_ROUTER_USER",
            "TR_ROUTER_PASSWORD",
        ]
    )


def main() -> None:
    validate_env()

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
