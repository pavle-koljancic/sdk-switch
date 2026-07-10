from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import ClassVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import ValidationError

from exceptions.exceptions import NSOQueryResultError
from models.nso.nso_base_result import NsoBaseResult
from models.nso.nso_base_result import Select

logger = logging.getLogger(__name__)


class NsoBaseParameters(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


@dataclass(frozen=True)
class NsoQueryStrategy:
    name: str
    result_model: type[NsoBaseResult]
    parameters_model: type[NsoBaseParameters]
    build_foreach: Callable[[NsoBaseParameters], str]
    allow_empty_result: bool = False

    QUERY_REGISTRY: ClassVar[dict[str, NsoQueryStrategy]] = {}

    def __post_init__(self) -> None:
        self.QUERY_REGISTRY[self.name] = self
        logger.info("Registered NSO query: %s", self.name)

    def build_body(self, parameters: NsoBaseParameters, select: tuple[Select, ...]) -> dict[str, Any]:
        foreach = self.build_foreach(parameters)

        return {
            "immediate-query": {
                "foreach": foreach,
                "select": [item.to_dict() for item in select],
            }
        }

    def parse_response(self, response: dict[str, Any]) -> list[NsoBaseResult]:
        if "tailf-rest-query:query-result" not in response:
            raise NSOQueryResultError()

        results: list[NsoBaseResult] = []
        rows = response.get("tailf-rest-query:query-result", {}).get("result", [])

        for row in rows:
            props: dict[str, Any] = {}
            for item in row.get("select", []):
                props[item["label"]] = item.get("value", item.get("data"))

            try:
                results.append(self.result_model(**props))
            except ValidationError as error:
                logger.warning(f"Skipping invalid row for {self.name}: {props}\nReason: {error.errors()[0]['msg']}")

        if not results and not self.allow_empty_result:
            raise NSOQueryResultError(f"NSO query {self.name} returned no valid rows")

        return results
