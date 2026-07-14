from conductor.client import worker_task

from models.wdm.wdm_device_vendor import WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS
from models.wdm.wdm_device_vendor import WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS
from task_logging.task_logger import get_task_logger
from conductor.client.http.models.task_def import TaskDef
task_logger = get_task_logger()


@worker_task(
    task_definition_name="is_kit_on_wdm",
    register_task_def=True,  # Auto-register on startup
        task_def=TaskDef(
                    description=(
                "Determine whether the kit is on WDM or not. We will do this by checking if the kit "
                "name contains any of the substrings from the lists "
                "WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS and WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS."
            ),
            timeout_seconds=  180)
)
def is_kit_on_wdm(kit: str) -> bool:
    matched_huawei = [sub for sub in WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS if sub in kit]
    matched_uni = [sub for sub in WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS if sub in kit]

    is_kit_on_wdm = bool(matched_huawei or matched_uni)

    task_logger.info(
        f"huawei_substrings={WDM_DEVICE_HUAWEI_NAME_SUBSTRINGS}, uni_substring={WDM_DEVICE_UNI_ACTIVATION_SUBSTRINGS}"
    )

    task_logger.info(
        f"Checking kit for WDM: kit='{kit}', matched_huawei_substring={matched_huawei}, matched_uni_substring={matched_uni}, is_kit_on_wdm={is_kit_on_wdm}"
    )

    return is_kit_on_wdm
