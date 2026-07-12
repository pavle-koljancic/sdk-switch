import pytest

from workers.common.map_interface_to_short_name import map_interface_to_short_name


class TestMapInterfaceToShortName:
    @pytest.mark.parametrize(
        "interface_full, os_version,expected",
        [
            ("TenGigabitEthernet", "cisco-ios", "Te"),
            ("GigabitEthernet", "cisco-ios", "Ge"),
            ("HundredGigE", "cisco-ios", "Hu"),
            ("TenGigE", "cisco-iosxr", "Te"),
            ("GigabitEthernet", "cisco-iosxr", "Ge"),
            ("HundredGigE", "cisco-ios", "Hu"),
        ],
    )
    def test_success(self, interface_full, os_version, expected):
        assert expected == map_interface_to_short_name(interface_full, os_version)

    @pytest.mark.parametrize(
        "interface_full, os_version",
        [
            ("UnknownInterface", "cisco-ios"),
            ("UnknownInterface", "cisco-iosxr"),
        ],
    )
    def test_failure(self, interface_full, os_version):
        with pytest.raises(ValueError):
            map_interface_to_short_name(interface_full, os_version)
