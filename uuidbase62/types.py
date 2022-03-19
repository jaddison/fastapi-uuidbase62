import re
import typing
import uuid

from . import base62
from .exceptions import Base62MissingPrefix


class UUIDBase62(str):
    def __new__(cls, value="", prefix="", base62_str="", uuid_=None):
        return super().__new__(cls, value)

    def __init__(self, value="", prefix="", base62_str="", uuid_=None):
        self.prefix = prefix
        self.base62_str = base62_str
        self.uuid = uuid_
        self.value = value

    @classmethod
    def validate(cls, value: typing.Any) -> "UUIDBase62":
        return to_uuidbase62(value, cls.prefix)

    @classmethod
    def __get_validators__(cls) -> typing.Generator[typing.Callable, None, None]:
        yield cls.validate

    def __repr__(self) -> str:
        return f"UUIDBase62('{self.value}')"

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, str) and self.value == other

    def __len__(self) -> int:
        return len(self.value)


def con_uuidbase62(
    *,
    prefix: str = "",
):
    results = re.search(r"^[a-zA-Z0-9_]+$", prefix)
    if not results:
        raise Base62MissingPrefix

    namespace = dict(
        prefix=prefix,
    )
    return type("UUIDBase62Value", (UUIDBase62,), namespace)


def to_uuidbase62(value: typing.Union[str, uuid.UUID, UUIDBase62], prefix: str = None) -> UUIDBase62:
    if isinstance(value, UUIDBase62):
        if prefix is not None and prefix != value.prefix:
            raise ValueError(
                f"Field's expected '{prefix}' prefix does not match given prefix '{value.prefix}'"
            )
        return value

    if not isinstance(value, uuid.UUID):
        try:
            value = uuid.UUID(value)
        except:
            pass

    if isinstance(value, uuid.UUID):
        base62_str = base62.encode(value)
        uuid_ = value
        if prefix:
            prefixed_base62_id = f"{prefix}_{base62_str}"
        else:
            prefixed_base62_id = base62_str
    elif isinstance(value, str):
        prefixed_base62_id = value
        parts = prefixed_base62_id.rsplit("_", 1)
        if len(parts) == 2:
            found_prefix, base62_str = parts
        else:
            found_prefix = ""
            base62_str = parts[0]

        if prefix is not None and prefix != found_prefix:
            raise ValueError(
                f"Field's expected '{prefix}' prefix does not match given prefix '{found_prefix}'"
            )

        try:
            uuid_ = base62.decode(base62_str)
        except ValueError:
            raise ValueError("Value contains invalid characters")

    return UUIDBase62(value=prefixed_base62_id, prefix=prefix, base62_str=base62_str, uuid_=uuid_)
