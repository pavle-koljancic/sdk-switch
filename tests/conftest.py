from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


# Fixture created to be auto loaded for every test since task_logger
# depends on task context which needs to be mocked.
@pytest.fixture(autouse=True)
def mock_task_context():
    with patch("task_logging.task_logger.get_task_context") as mock_context:
        mock_context.return_value = MagicMock(
            get_task_id=lambda: "test-task",
            get_retry_count=lambda: 0,
            get_poll_count=lambda: 1,
        )
        yield mock_context
