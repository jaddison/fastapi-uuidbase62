import uuid

import pytest
from pydantic import BaseModel

from uuidbase62 import UUIDBase62ModelMixin, con_uuidbase62


@pytest.mark.parametrize(
    "value",
    [
        # tests serialization in both directions (from uuid -> str, str -> uuid)
        uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8"),
        "f8711c37-c1d1-4961-ba3c-98cdc5b4fda8",
        "my_prefix_7yNMTpVy8ddRxYKGJqtk7e",
    ],
)
def test_to_uuidbase62_method_in_model__with_valid_uuid__yields_correct_values(value):
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    class ValidPrefixModel(UUIDBase62ModelMixin, BaseModel):
        id: con_uuidbase62(prefix=prefix)

    uuidbase62_value = ValidPrefixModel.to_uuidbase62("id", value)

    assert uuidbase62_value.startswith(f"{prefix}_")
    assert uuidbase62_value == encoded_value
    assert uuidbase62_value.value == encoded_value
    assert uuidbase62_value.uuid == uuid_
    assert uuidbase62_value.prefix == prefix
    assert uuidbase62_value.base62_str == encoded_value.rsplit("_", 1)[1]
