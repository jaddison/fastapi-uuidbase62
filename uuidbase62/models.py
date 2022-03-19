import typing
import uuid

from .types import UUIDBase62


class UUIDBase62ModelMixin:
    @classmethod
    def to_uuidbase62(cls, field: str, value: typing.Union[str, uuid.UUID, UUIDBase62]) -> UUIDBase62:
        return cls.__fields__[field].type_.validate(value)  # type: ignore
