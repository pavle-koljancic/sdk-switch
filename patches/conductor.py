import inspect
from typing import Any

import conductor.client.automator.utils as automator_utils
from pydantic import BaseModel


def is_pydantic_model(cls: type) -> bool:
    try:
        return inspect.isclass(cls) and issubclass(cls, BaseModel)
    except TypeError:
        return False


def convert_to_pydantic(cls: type, data: dict[str, Any]) -> object:
    if data is None:
        return None
    return cls(**data)


_original_convert_from_dict = automator_utils.convert_from_dict


def patched_pydantic_convert_from_dict(cls: type, data: dict[str, Any]) -> object:
    if is_pydantic_model(cls=cls):
        return convert_to_pydantic(cls=cls, data=data)
    return _original_convert_from_dict(cls=cls, data=data)


if automator_utils.convert_from_dict != patched_pydantic_convert_from_dict:
    automator_utils.convert_from_dict = patched_pydantic_convert_from_dict
