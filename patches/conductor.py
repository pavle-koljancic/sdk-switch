import inspect
import types
import typing
from collections.abc import Iterable
from typing import Any
from typing import cast

import conductor.client.automator.utils as automator_utils
from conductor.client.worker import worker
from pydantic import BaseModel


# Checks if the typing Union type
def is_union_type(cls: type) -> bool:
    return typing.get_origin(cls) in (
        typing.Union,
        types.UnionType,
    )


def extract_union_types_as_list(cls: type) -> list[type]:
    if not is_union_type(cls):
        raise ValueError(f"The class passed into union extraction is not a Union {cls}")
    return list(typing.get_args(cls))


# PYDANTIC V1 should not be supported
# Method to check if something is a pydantic v2 BaseModel
def is_pydantic_model(cls: type | type[None]) -> bool:
    return inspect.isclass(cls) and issubclass(cls, BaseModel) and hasattr(cls, "model_validate")


# Deserialization for pydantic BaseModels
def convert_to_pydantic(
    cls: type[BaseModel],
    data: dict[str, Any] | None,
) -> BaseModel | None:
    if data is None:
        return None
    return cls.model_validate(data)


_original_convert_from_dict = automator_utils.convert_from_dict


def patched_convert_from_dict(cls: type, data: dict[str, Any] | Any) -> object:
    if is_pydantic_model(cls=cls):
        return convert_to_pydantic(cls=cls, data=data)

    origin_type = typing.get_origin(cls)

    if origin_type and issubclass(origin_type, dict):
        key_args, value_args = typing.get_args(cls)
        result = {}
        for k, v in data.items():
            result[patched_convert_from_dict_or_list(cls=key_args, data=k)] = patched_convert_from_dict_or_list(
                cls=value_args, data=v
            )
        return result
    return _original_convert_from_dict(cls=cls, data=data)


def is_collection(t: type[Any]) -> bool:
    origin = typing.get_origin(t)
    if origin is not None:  # IF an origin type exist then it is a parametrized generic
        t = cast(type[Any], origin)
    return issubclass(t, Iterable) and not issubclass(t, str | bytes)


def convert_base_types(cls: type, data: Any) -> object:
    if cls is typing.Any:
        return data
    if cls is type(None) and data is None:
        return data
    if cls is type(None) and data is not None:
        raise TypeError("Type is None data is not None!")
    if cls in automator_utils.simple_types:
        if isinstance(data, cls):
            return data
        else:
            raise TypeError("Data typing and value mismatch")
    raise TypeError("Type does not match None, Any or simple types.")


def patched_convert_from_dict_or_list(cls: type, data: dict[str, Any] | list[Any] | Any) -> object:
    if cls is typing.Any or cls is type(None) or cls in automator_utils.simple_types:
        return convert_base_types(cls=cls, data=data)

    if is_union_type(cls=cls):
        for type_item in extract_union_types_as_list(cls=cls):
            try:
                return patched_convert_from_dict_or_list(cls=type_item, data=data)
            except (ValueError, TypeError):
                print(f"Attempted to convert data:{data} to type:{type_item}")
        raise ValueError("No Union type was effectively converted")

    is_list = type(data) in automator_utils.collection_types

    if is_list and not is_collection(t=cls):
        raise TypeError("Mismatch between data and expected type")

    if is_list:
        val_list = []
        for val in data:
            generic_types = typing.get_args(cls)[0]
            converted = patched_convert_from_dict(generic_types, val)
            val_list.append(converted)
        return cls(val_list)
    return patched_convert_from_dict(cls, data)


if automator_utils.convert_from_dict != patched_convert_from_dict:
    automator_utils.convert_from_dict = patched_convert_from_dict

if automator_utils.convert_from_dict_or_list != patched_convert_from_dict_or_list:
    automator_utils.convert_from_dict_or_list = patched_convert_from_dict_or_list
    worker.convert_from_dict_or_list = patched_convert_from_dict_or_list
