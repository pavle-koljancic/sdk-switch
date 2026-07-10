import logging

from conductor.client.event.task_runner_events import PollCompleted
from conductor.client.event.task_runner_events import PollFailure
from conductor.client.event.task_runner_events import PollStarted
from conductor.client.event.task_runner_events import TaskExecutionCompleted
from conductor.client.event.task_runner_events import TaskExecutionFailure
from conductor.client.event.task_runner_events import TaskExecutionStarted

logger = logging.getLogger(__name__)


class TaskExecutionLogger:
    """
    Simple listener that logs all task execution events.

    Demonstrates basic pre/post processing:
    - on_task_execution_started: Pre-processing before task executes
    - on_task_execution_completed: Post-processing after successful execution
    - on_task_execution_failure: Error handling after failed execution
    """

    def on_task_execution_started(self, event: TaskExecutionStarted) -> None:
        """
        Called before task execution begins (pre-processing).

        Use this for:
        - Setting up context (tracing, logging context)
        - Validating preconditions
        - Starting timers
        - Recording audit events
        """
        logger.info(f"[PRE] Starting task '{event.task_type}' (task_id={event.task_id}, worker={event.worker_id})")

    def on_task_execution_completed(self, event: TaskExecutionCompleted) -> None:
        """
        Called after task execution completes successfully (post-processing).

        Use this for:
        - Logging results
        - Sending notifications
        - Updating external systems
        - Recording metrics
        """
        logger.info(
            f"[POST] Completed task '{event.task_type}' "
            f"(task_id={event.task_id}, duration={event.duration_ms:.2f}ms, "
            f"output_size={event.output_size_bytes} bytes)"
        )

    def on_task_execution_failure(self, event: TaskExecutionFailure) -> None:
        """
        Called when task execution fails (error handling).

        Use this for:
        - Error logging
        - Alerting
        - Retry logic
        - Cleanup operations
        """
        logger.error(
            f"[ERROR] Failed task '{event.task_type}' "
            f"(task_id={event.task_id}, duration={event.duration_ms:.2f}ms, "
            f"error={event.cause})"
        )

    def on_poll_started(self, event: PollStarted) -> None:
        """Called when polling for tasks begins."""
        logger.debug(f"Polling for {event.poll_count} '{event.task_type}' tasks")

    def on_poll_completed(self, event: PollCompleted) -> None:
        """Called when polling completes successfully."""
        if event.tasks_received > 0:
            logger.debug(f"Received {event.tasks_received} '{event.task_type}' tasks in {event.duration_ms:.2f}ms")

    def on_poll_failure(self, event: PollFailure) -> None:
        """Called when polling fails."""
        logger.warning(f"Poll failed for '{event.task_type}': {event.cause}")
