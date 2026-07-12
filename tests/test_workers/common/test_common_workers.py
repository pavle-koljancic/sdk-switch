import os
from unittest.mock import patch

import pytest

from workers.common.export_to_local_disk import WorkerOutput
from workers.common.export_to_local_disk import export_to_local_disk


class TestExportToLocalDisk:
    @pytest.mark.parametrize(
        "data_to_save,file_name,directory,workflow_id,pop_name,expected_content",
        [
            # Scenario 1: Test with multiple command sets
            (
                """devices device MI_16-E-NPE-02 config
                no interface TenGigE0/2/0/13.1123 l2transport
                devices device MI_16-E-NPE-02 config l2vpn
                no xconnect group MI1602_UD0101_12239
                commit
                devices device MI_16-E-NPE-03 config
                no interface TenGigE0/0/0/4.1123 l2transport
                devices device MI_16-E-NPE-03 config l2vpn
                no xconnect group MI1603_AN0101_7406
                commit""",
                "Discover_SVLANs_configurations_ROUTER",
                "test_temp",
                "dummy_id",
                "PG_01",
                """devices device MI_16-E-NPE-02 config
                no interface TenGigE0/2/0/13.1123 l2transport
                devices device MI_16-E-NPE-02 config l2vpn
                no xconnect group MI1602_UD0101_12239
                commit
                devices device MI_16-E-NPE-03 config
                no interface TenGigE0/0/0/4.1123 l2transport
                devices device MI_16-E-NPE-03 config l2vpn
                no xconnect group MI1603_AN0101_7406
                commit""",
            ),
            # Scenario 2: Test with a simple string
            (
                "Hello World!",
                "Hello",
                "test_temp",
                "dummy_id",
                "PG_01",
                "Hello World!",
            ),
            # Scenario 3: Test with empty data set
            (
                [],
                "Empty_File",
                "test_temp",
                "dummy_id",
                "PG_01",
                "",
            ),
        ],
    )
    @patch("workers.common.export_to_local_disk.get_workflow_data")
    @patch("workers.common.export_to_local_disk.generate_timestamp")
    def test_success(
        self,
        mock_generate_timestamp,
        mock_get_workflow_data,
        data_to_save,
        file_name,
        directory,
        workflow_id,
        pop_name,
        expected_content: str,
    ):
        mock_get_workflow_data.return_value = {"createTime": 1710000000000, "parentWorkflowId": None}
        mock_generate_timestamp.return_value = "20250317-120000-CET"

        result: WorkerOutput = export_to_local_disk(
            data_to_save=data_to_save,
            file_name=file_name,
            directory=directory,
            workflow_id=workflow_id,
            pop_name=pop_name,
        )

        assert result.saved is True
        assert os.path.isfile(result.output_file_path)

        with open(result.output_file_path) as file:
            file_content = file.read().strip()
            assert file_content == expected_content.strip(), "File content does not match expected data"

        # Clean up after the test to avoid leaving test artifacts
        os.remove(result.output_file_path)

    @pytest.mark.parametrize(
        "data_to_save,file_name,directory,workflow_id,pop_name,file_type,expected_content",
        [
            # Scenario 4: test multiple bash commands to save
            (
                {
                    "cookieJar": "bash /var/opt/ncs/scripts/siae/cookie.sh https://onc-coll:8443 nsoadmin Dummy%%",
                    "services": [
                        {
                            "1": "curl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/1",
                            "2": "curl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/2",
                            "3": "curl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/3",
                            "4": "curl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/4",
                            "5": "curl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/5",
                            "6": "curl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/6",
                        },
                    ],
                },
                "Discover_SVLANs_configurations_WDM",
                "test_temp",
                "dummy_id",
                "PG_01",
                "bash",
                """bash /var/opt/ncs/scripts/siae/cookie.sh https://onc-coll:8443 nsoadmin Dummy%%\ncurl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/1\ncurl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/2\ncurl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/3\ncurl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/4\ncurl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/5\ncurl -k -b .cookieJar -X DELETE https://onc-coll:8443/onc/connection/6""",
            ),
        ],
    )
    @patch("workers.common.export_to_local_disk.get_workflow_data")
    @patch("workers.common.export_to_local_disk.generate_timestamp")
    def test_success_bash(
        self,
        mock_generate_timestamp,
        mock_get_workflow_data,
        data_to_save,
        file_name,
        directory,
        workflow_id,
        pop_name,
        file_type,
        expected_content: str,
    ):
        mock_get_workflow_data.return_value = {"createTime": 1710000000000, "parentWorkflowId": None}
        mock_generate_timestamp.return_value = "20250317-120000-CET"

        result: WorkerOutput = export_to_local_disk(
            data_to_save=data_to_save,
            file_name=file_name,
            directory=directory,
            workflow_id=workflow_id,
            pop_name=pop_name,
            filetype=file_type,
        )

        assert result.saved is True
        assert os.path.isfile(result.output_file_path)

        with open(result.output_file_path) as file:
            file_content = file.read().strip()
            assert file_content == expected_content.strip(), "File content does not match expected data"

        # Clean up after the test to avoid leaving test artifacts
        os.remove(result.output_file_path)
