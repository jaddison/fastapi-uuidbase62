import uuid

import pytest
from pydantic import BaseModel, ValidationError

from uuidbase62 import Base62MissingPrefix, con_uuidbase62
from uuidbase62.types import UUIDBase62, to_uuidbase62


@pytest.mark.parametrize(
    "value",
    [
        # tests serialization in both directions (from uuid -> str, str -> uuid)
        uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8"),
        "f8711c37-c1d1-4961-ba3c-98cdc5b4fda8",
        "7yNMTpVy8ddRxYKGJqtk7e",
    ],
)
def test_to_uuidbase62_function__with_no_prefix__works(value):
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    encoded_value = f"7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(value)

    assert isinstance(result, UUIDBase62)
    assert encoded_value == result
    assert encoded_value == result.value
    assert result.prefix is None
    assert uuid_ == result.uuid


@pytest.mark.parametrize(
    "value",
    [
        # tests serialization in both directions (from uuid -> str, str -> uuid)
        uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8"),
        "f8711c37-c1d1-4961-ba3c-98cdc5b4fda8",
        "my_prefix_7yNMTpVy8ddRxYKGJqtk7e",
    ],
)
def test_to_uuidbase62_function__with_prefix__works(value):
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(value, prefix)

    assert isinstance(result, UUIDBase62)
    assert encoded_value == result
    assert encoded_value == result.value
    assert result.prefix == prefix
    assert uuid_ == result.uuid


def test_to_uuidbase62_function__with_uuidbase62_no_prefix__works():
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(uuid_, prefix)
    result2 = to_uuidbase62(result)

    assert result is result2
    assert result2 == encoded_value


def test_to_uuidbase62_function__with_uuidbase62_same_prefix__works():
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(uuid_, prefix)
    result2 = to_uuidbase62(result, prefix)

    assert result is result2
    assert result2 == encoded_value


def test_to_uuidbase62_function__with_uuidbase62_different_prefix__fails():
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")

    result = to_uuidbase62(uuid_, prefix)
    with pytest.raises(ValueError) as e:
        to_uuidbase62(result, "different_prefix")

    assert "Field's expected 'different_prefix' prefix does not match given prefix 'my_prefix'" in str(e)


def test_to_uuidbase62_function__with_invalid_value__fails():
    with pytest.raises(ValueError) as e:
        to_uuidbase62("invalid-value")

    assert "Value contains invalid characters" in str(e)


def test_con_uuidbase62_function__with_no_prefix__raises_error():
    with pytest.raises(Base62MissingPrefix):
        con_uuidbase62()


def test_con_uuidbase62_function_in_model__with_no_prefix__raises_error():
    with pytest.raises(Base62MissingPrefix):

        class ValidPrefixModel(BaseModel):
            id: con_uuidbase62()


def test_con_uuidbase62_function_in_model__with_invalid_uuid_invalid_prefix__raises_error():
    class ValidPrefixModel(BaseModel):
        id: con_uuidbase62(prefix="my_prefix")

    with pytest.raises(ValidationError) as e:
        ValidPrefixModel(id="invalid-value")

    assert "Field's expected 'my_prefix' prefix does not match given prefix ''" in str(e)


def test_con_uuidbase62_function_in_model__with_invalid_uuid_valid_prefix__raises_error():
    class ValidPrefixModel(BaseModel):
        id: con_uuidbase62(prefix="my_prefix")

    with pytest.raises(ValidationError) as e:
        ValidPrefixModel(id="my_prefix_invalid-value")

    assert "Value contains invalid characters" in str(e)


@pytest.mark.parametrize(
    "value",
    [
        # tests serialization in both directions (from uuid -> str, str -> uuid)
        uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8"),
        "f8711c37-c1d1-4961-ba3c-98cdc5b4fda8",
        "my_prefix_7yNMTpVy8ddRxYKGJqtk7e",
    ],
)
def test_con_uuidbase62_function_in_model__with_valid_uuid__yields_correct_values(
    value,
):
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    class ValidPrefixModel(BaseModel):
        id: con_uuidbase62(prefix=prefix)

    model_instance = ValidPrefixModel(id=value)

    assert model_instance.id.startswith(f"{prefix}_")
    assert model_instance.id == encoded_value
    assert model_instance.id.value == encoded_value
    assert model_instance.id.uuid == uuid_
    assert model_instance.id.prefix == prefix
    assert model_instance.id.base62_str == encoded_value.rsplit("_", 1)[1]


def test_uuidbase62_len__with_valid_value__works_correctly():
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(uuid_, prefix=prefix)

    assert len(result) == len(encoded_value)


def test_uuidbase62_repr__with_valid_value__works_correctly():
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(uuid_, prefix=prefix)

    assert repr(result) == f"UUIDBase62('{encoded_value}')"


def test_uuidbase62_str__with_valid_value__works_correctly():
    prefix = "my_prefix"
    uuid_ = uuid.UUID("f8711c37-c1d1-4961-ba3c-98cdc5b4fda8")
    # base62 encoded prefixed value of the above uuid_
    encoded_value = f"{prefix}_7yNMTpVy8ddRxYKGJqtk7e"

    result = to_uuidbase62(uuid_, prefix=prefix)

    assert str(result) == encoded_value
