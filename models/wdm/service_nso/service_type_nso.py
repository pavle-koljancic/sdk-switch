from enum import Enum


class ServiceTypeNso(Enum):
    PW3_HUAWEI_OPTICAL = "pw3-huawei-optical"
    VPLS_HUAWEI_OPTICAL = "vpls-huawei-optical"
    ETH_HUAWEI_NATIVE = "eth-huawei-native"
    PW3_SIAE_OPTICAL = "pw3-siae-optical"
    VPLS_SIAE_OPTICAL = "vpls-siae-optical"
    PW3_HUAWEI_OPTICAL_RD = "pw3-huawei-optical-rd"
    VPLS_HUAWEI_OPTICAL_RD = "vpls-huawei-optical-rd"
    ETH_HUAWEI_NATIVE_RD = "eth-huawei-native-rd"
    PW3_SIAE_OPTICAL_RD = "pw3-siae-optical-rd"
    VPLS_SIAE_OPTICAL_RD = "vpls-siae-optical-rd"

    @classmethod
    def get_rd_map(cls) -> dict["ServiceTypeNso", "ServiceTypeNso"]:
        return {
            cls.PW3_HUAWEI_OPTICAL: cls.PW3_HUAWEI_OPTICAL_RD,
            cls.VPLS_HUAWEI_OPTICAL: cls.VPLS_HUAWEI_OPTICAL_RD,
            cls.ETH_HUAWEI_NATIVE: cls.ETH_HUAWEI_NATIVE_RD,
            cls.PW3_SIAE_OPTICAL: cls.PW3_SIAE_OPTICAL_RD,
            cls.VPLS_SIAE_OPTICAL: cls.VPLS_SIAE_OPTICAL_RD,
        }
