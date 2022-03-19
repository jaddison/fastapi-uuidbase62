import uuid

import fastapi
import pytest
from pydantic import BaseModel

from uuidbase62 import (
    UUIDBase62,
    UUIDBase62ModelMixin,
    con_uuidbase62,
    get_validated_uuidbase62,
    get_validated_uuidbase62_by_model,
)


class Item(UUIDBase62ModelMixin, BaseModel):
    client_id: con_uuidbase62(prefix="my_prefix")  # type: ignore


def test_get_validated_uuidbase62_by_model_function__returns_callable():
    func = get_validated_uuidbase62_by_model(Item, "client_id", "item_id")

    assert callable(func)


def test_get_validated_uuidbase62_by_model_function__with_valid_input__returns_valid_uuidbase62_value():
    prefix = "my_prefix"
    value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"
    func = get_validated_uuidbase62_by_model(Item, "client_id", "item_id")
    uuidbase62_value = func(value)

    assert isinstance(uuidbase62_value, UUIDBase62)
    assert uuidbase62_value.value == value
    assert uuidbase62_value.prefix == prefix
    assert isinstance(uuidbase62_value.uuid, uuid.UUID)


def test_get_validated_uuidbase62_function__returns_callable():
    func = get_validated_uuidbase62("item_id")

    assert callable(func)


def test_get_validated_uuidbase62_function__with_valid_input__returns_valid_uuidbase62_value():
    prefix = "my_prefix"
    value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"
    func = get_validated_uuidbase62("item_id", prefix)
    uuidbase62_value = func(value)

    assert isinstance(uuidbase62_value, UUIDBase62)
    assert uuidbase62_value.value == value
    assert uuidbase62_value.prefix == prefix
    assert isinstance(uuidbase62_value.uuid, uuid.UUID)


def test_get_validated_uuidbase62_function__with_invalid_input__returns_valid_uuidbase62_value():
    value = f"my_prefix_7yNMTpVy8ddRxYKGJqtk7e"

    func = get_validated_uuidbase62("item_id", "different_prefix")
    with pytest.raises(fastapi.exceptions.HTTPException) as e:
        func(value)

    assert e.value.status_code == 404


def test_get_validated_uuidbase62_by_model_function__with_invalid_input__returns_valid_uuidbase62_value():
    value = f"different_prefix_7yNMTpVy8ddRxYKGJqtk7e"

    func = get_validated_uuidbase62_by_model(Item, "client_id", "item_id")
    with pytest.raises(fastapi.exceptions.HTTPException) as e:
        func(value)

    assert e.value.status_code == 404
