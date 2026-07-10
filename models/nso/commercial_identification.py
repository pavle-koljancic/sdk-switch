from typing import Annotated
from typing import cast

from pydantic import StringConstraints

from models.nso.nso_base_result import NsoBaseResult
from models.nso.nso_base_result import Select
from models.nso.nso_query_strategy import NsoBaseParameters
from models.nso.nso_query_strategy import NsoQueryStrategy


class CommercialIdentification(NsoBaseResult):
    kit: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Select("kit")]
    svlan: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1), Select("s-vlan")]
    nome_circuito: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
        Select("Nome-circuito"),
    ]
    pop_name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
        Select("pop-name-collect"),
    ]
    profile_mkt_bea: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
        Select("profile_MKT_BEA"),
    ]


class CommercialIdentificationParameters(NsoBaseParameters):
    resource_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def _build_commercial_identification_foreach(params: NsoBaseParameters) -> str:
    commercial_params = cast(CommercialIdentificationParameters, params)
    return f"/bs-oss/svlan_status[resource-id='{commercial_params.resource_id}']"


CommercialIdentificationQuery = NsoQueryStrategy(
    name="CommercialIdentificationQuery",
    result_model=CommercialIdentification,
    parameters_model=CommercialIdentificationParameters,
    build_foreach=_build_commercial_identification_foreach,
)
