import uuid

import pytest
from pydantic import BaseModel

from uuidbase62 import UUIDBase62, base62, con_uuidbase62


@pytest.mark.parametrize(
    "uuid_,str_",
    [
        (uuid.UUID("3fbae77c-5852-47cb-a82f-aeebc6ee3f43"), "1WfVMU43m1UQUtAHULNBzd"),
        (uuid.UUID(int=0), "0"),
    ],
)
def test_type_encode_decode__with_valid_uuid__works_correctly(uuid_, str_):
    encoded_str = base62.encode(uuid_)
    decoded_uuid = base62.decode(encoded_str)

    assert isinstance(encoded_str, str)
    assert encoded_str == str_
    assert isinstance(decoded_uuid, uuid.UUID)
    assert decoded_uuid == uuid_


def test_type_encode__with_valid_uuidbase62__works_correctly():
    original_uuid = uuid.UUID("3fbae77c-5852-47cb-a82f-aeebc6ee3f43")
    original_str = "1WfVMU43m1UQUtAHULNBzd"

    class ValidPrefixModel(BaseModel):
        id: con_uuidbase62(prefix="my_prefix")

    instance = ValidPrefixModel(id=original_uuid)
    value = instance.id

    encoded_str = base62.encode(value)

    assert isinstance(value, UUIDBase62)
    assert isinstance(encoded_str, str)
    assert encoded_str == original_str


def test_type_decode__with_valid_uuidbase62__works_correctly():
    original_uuid = uuid.UUID("3fbae77c-5852-47cb-a82f-aeebc6ee3f43")

    class ValidPrefixModel(BaseModel):
        id: con_uuidbase62(prefix="my_prefix")

    instance = ValidPrefixModel(id=original_uuid)
    value = instance.id

    decoded_uuid = base62.decode(value)

    assert isinstance(value, UUIDBase62)
    assert isinstance(decoded_uuid, uuid.UUID)
    assert decoded_uuid == original_uuid


def test_type_decode__with_valid_uuid__works_correctly():
    uuid_ = uuid.UUID("3fbae77c-5852-47cb-a82f-aeebc6ee3f43")

    decoded_uuid = base62.decode(uuid_)

    assert isinstance(decoded_uuid, uuid.UUID)
    assert decoded_uuid == uuid_


def test_type_encode__with_invalid_uuid_str__raises_error():
    with pytest.raises(ValueError):
        base62.encode("invalid-value")


def test_type_encode__with_invalid_uuid_any__raises_error():
    with pytest.raises(ValueError):
        base62.encode(None)
