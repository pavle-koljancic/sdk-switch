from models.wdm.service_nso.service_type_nso import ServiceTypeNso


# NSO
class NSOError(Exception):
    """when there is an issue when making a request to Cisco NSO"""


class NSOHttpError(NSOError):
    """when a status code of NSO response is not ok (less than 400)"""


class NSOQueryResultError(NSOError):
    """
    Exception raised for errors in the query result from Cisco NSO.
    """

    def __init__(
        self,
        message: str | None = "No query result key `tailf-rest-query:query-result` found in the NSO response",
    ) -> None:
        self.message = message
        super().__init__(self.message)


# WDM


class WdmHuaweiControllerError(Exception):
    """when there is an issue when making a request to WDM controller (Huawei)"""


class WdmHuaweiControllerHttpError(WdmHuaweiControllerError):
    """when a status code of WDM controller response is not ok (less than 400)"""


class DBError(ValueError):
    def __init__(self, message: str = "Fetched data from the database is invalid") -> None:
        super().__init__(message)


class OfOSVersionNotFoundError(ValueError):
    def __init__(self, os_version: str) -> None:
        self.os_version = os_version
        super().__init__(f"OS version '{os_version}' is not recognized as a valid Cisco OS version.")


class OfEmptyNsoReturnOSVersionError(ValueError):
    def __init__(self) -> None:
        super().__init__("Return from NSO was empty, could not retrieve the OS version.")


class OfEmptyNsoReturnIccpGroupError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            "MC Lag not correctly configured. Return from NSO was empty, could not retrieve the ICCP Group ID."
        )


class OfEmptyNsoReturnNeighborIpError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            "MC Lag not correctly configured. Return from NSO was empty, could not retrieve the neighbor IP."
        )


class OfEmptyNsoReturnTwinDeviceNameError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            "MC Lag not correctly configured. Return from NSO was empty, could not retrieve the MC-LAG twin router name from neighbor IP."
        )


class OfPortMismatchError(ValueError):
    def __init__(
        self,
        service_type: str,
        input_ports_a: list[str],
        input_ports_b: list[str],
        config_ports_a: list[str],
        config_ports_b: list[str],
    ) -> None:
        self.service_type = service_type
        self.input_ports_a = input_ports_a
        self.input_ports_b = input_ports_b
        self.config_ports_a = config_ports_a
        self.config_ports_b = config_ports_b
        super().__init__(
            f"Port mismatch error for service type '{service_type}'. "
            f"Input ports A: {input_ports_a}, B: {input_ports_b}. "
            f"Config ports A: {config_ports_a}, B: {config_ports_b}."
        )


class OfIncorrectSvlanDataError(ValueError):
    def __init__(self, message: str = "Fetched SVLAN data from the database is invalid") -> None:
        super().__init__(message)


class OfNoInterfaceIndexesFoundError(ValueError):
    def __init__(self, olo: str, node_a: str, node_b: str | None, svlan: int) -> None:
        self.olo = olo
        self.node_a = node_a
        self.node_b = node_b
        self.svlan = svlan
        super().__init__(
            f"No interface indexes found for OLO '{olo}' with node_a '{node_a}', node_b '{node_b}', and svlan '{svlan}'."
        )


class OfMissingResourceIdError(ValueError):
    def __init__(self, resource_id: str | None, service_type: ServiceTypeNso) -> None:
        super().__init__(f"Cannot make configuration service_type={service_type} resource_id={resource_id}.")


class OfOltConfigurationNotFoundError(ValueError):
    def __init__(self, svlan: int, olt_name: str) -> None:
        self.svlan = svlan
        self.olt_name = olt_name
        super().__init__(f"Query result is empty for olt_name={olt_name}, svlan={svlan}.")


class OfNoSvlaConfigurationDiscoveredError(ValueError):
    def __init__(self, path_to: str, path_from: str, svlan: str) -> None:
        message = (
            f"Could not discover SVLAN configuration on WDM layer. "
            f"Path to: {path_to}, Path from: {path_from}, SVLAN: {svlan}"
        )
        super().__init__(message)


class OfInvalidPathRegexError(ValueError):
    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"The provided path '{value}' does not match the expected regular expression.")


class OfMissingEnvironmentVariablesError(EnvironmentError):
    """Custom exception for missing environment variables."""

    def __init__(self, missing_variables: list[str]) -> None:
        self.missing_variables = missing_variables
        super().__init__(f"One or more environment variables are missing: {', '.join(missing_variables)}.")
