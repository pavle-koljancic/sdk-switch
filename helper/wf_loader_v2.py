import http.client
import json
from collections import deque
from functools import lru_cache
from http import HTTPStatus
from typing import Any
from typing import Union
from typing import cast
from urllib.parse import urlparse

from conductor.client.configuration.configuration import Configuration
from pydantic import BaseModel

config = Configuration()

FAILED_STATUSES = [
    "CANCELLED",
    "COMPLETED_WITH_ERRORS",
    "FAILED",
    "FAILED_WITH_TERMINAL_ERROR",
    "SKIPPED",
    "TIMED_OUT",
    "TERMINATED",
]


class TaskError(BaseModel):
    name: str
    task_id: str
    status: str
    info: str


class WorkflowError(BaseModel):
    workflow: str
    status: str
    failed_children: list[Union[TaskError, "WorkflowError"]] = []
    input: dict[str, Any] | None

    def is_failed_status(self) -> bool:
        return self.status in FAILED_STATUSES


WorkflowError.model_rebuild()


class WorkflowDataNode:
    def __init__(self, data: dict[str, Any]):
        # data = data.get("result", data)

        self.workflow_data = data or {}
        self.children: dict[str, WorkflowDataNode] = {}

    @property
    def child_ids(self) -> list[str]:
        ids: list[str] = []
        for task in self.workflow_data["tasks"]:
            # cast is added because of mypy
            task = cast(dict[str, Any], task)
            # In case of retried tasks we are interested only in status of final attempt.
            if task["retried"] is True:
                continue

            if task["taskType"] == "SUB_WORKFLOW":
                id = task.get("subWorkflowId", None)
                if id:
                    ids.append(task["subWorkflowId"])
        return ids

    def __str__(self) -> str:
        """Returns the id of the workflow as a string."""
        workflow_id: str = self.workflow_data["workflowId"]
        return workflow_id

    def add_child(self, data: "WorkflowDataNode") -> None:
        self.children[data.workflow_data["workflowId"]] = data

    @classmethod
    @lru_cache(maxsize=4096)
    def __inner_build_error_tree(cls, node: "WorkflowDataNode") -> WorkflowError:
        wrokflow_error = WorkflowError(
            workflow=node.workflow_data["workflowName"],
            status=node.workflow_data["status"],
            input=node.workflow_data["input"],
        )

        for task in node.workflow_data["tasks"]:
            # In case of retried tasks we are interested only in status of final attempt.
            if task["retried"] is True:
                continue

            if task["taskType"] == "SUB_WORKFLOW":
                if task.get("subWorkflowId") is None:
                    wrokflow_error.failed_children.append(
                        TaskError(
                            name=task.get("referenceTaskName", "unknown"),
                            task_id=task.get("taskId", "unknown"),
                            status=task.get("status", "unknown"),
                            info="SUB_WORKFLOW task has no subWorkflowId — may still be scheduled or was never started.",
                        )
                    )
                continue

            if task["status"] in FAILED_STATUSES:
                wrokflow_error.failed_children.append(
                    TaskError(
                        name=task["referenceTaskName"],
                        status=task["status"],
                        info=task["reasonForIncompletion"],
                        task_id=task["taskId"],
                    )
                )

            if task["taskType"] == "TERMINATE" and task["inputData"]["terminationStatus"] in FAILED_STATUSES:
                wrokflow_error.failed_children.append(
                    TaskError(
                        name=task["referenceTaskName"],
                        status=task["status"],
                        info=task["inputData"]["terminationReason"],
                        task_id=task["taskId"],
                    ),
                )

        for child in node.children.values():
            sub_tree = child.build_error_tree()
            if sub_tree.status in FAILED_STATUSES or len(sub_tree.failed_children) > 0:
                wrokflow_error.failed_children.append(sub_tree)

        return wrokflow_error

    def build_error_tree(self) -> WorkflowError:
        return WorkflowDataNode.__inner_build_error_tree(self)


@lru_cache(maxsize=2048)
def get_wrokflow_with_tasks(workflow_id: str) -> WorkflowDataNode:
    parsed_url = urlparse(config.host)
    conn = http.client.HTTPConnection(parsed_url.hostname, port=parsed_url.port)
    payload = ""
    # TODO SWITCH TO FRINX HEADERS LOADED FRON .env
    headers = {
        "Accept": "application/json",
        "x-tenant-id": "frinx",
        "from": "*frinx-rbac-admin-role",
        "x-auth-user-groups": "FRINXio",
    }
    conn.request("GET", f"/api/workflow/{workflow_id}?includeTasks=true", payload, headers)
    res = conn.getresponse()
    if res.status != HTTPStatus.OK:
        raise Exception("Status code not 200 OK")
    data = res.read()
    data_str = data.decode("utf-8")
    data_dict = json.loads(data_str)
    return WorkflowDataNode(data_dict)


def build_workflow_data_tree(root_workflow_id: str) -> WorkflowDataNode:
    root = get_wrokflow_with_tasks(workflow_id=root_workflow_id)
    queue: deque[WorkflowDataNode] = deque()
    queue.append(root)
    while len(queue) > 0:
        next = queue.popleft()
        ids = next.child_ids
        for sub_wokflow_id in ids:
            sub_workflow = get_wrokflow_with_tasks(workflow_id=sub_wokflow_id)
            next.add_child(sub_workflow)
            queue.append(sub_workflow)
    return root
