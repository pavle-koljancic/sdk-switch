import inspect
import typing
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


def is_instance_generic(cls: type, data: object) -> bool:
    origin = typing.get_origin(cls)
    if origin is not None:
        # cls is a parameterized generic like list[int] or dict[str, int]
        return isinstance(data, origin)
    return False


def patched_convert_from_dict(cls: type, data: dict[str, Any]) -> object:
    if is_pydantic_model(cls=cls):
        return convert_to_pydantic(cls=cls, data=data)
    if is_instance_generic(cls=cls, data=data):
        return data
    return _original_convert_from_dict(cls=cls, data=data)


if automator_utils.convert_from_dict != patched_convert_from_dict:
    automator_utils.convert_from_dict = patched_convert_from_dict
