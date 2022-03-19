from __future__ import annotations

import typing
import uuid

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE62_LENGTH = len(BASE62)

if typing.TYPE_CHECKING:  # pragma: no cover
    from .types import UUIDBase62


def encode(value: typing.Union[uuid.UUID, str, "UUIDBase62"]) -> str:
    from .types import UUIDBase62

    if isinstance(value, UUIDBase62):
        return value.base62_str
    elif isinstance(value, str):
        try:
            value = uuid.UUID(value)
        except:
            raise ValueError("Base62 encoding requires a UUID value")
    elif not isinstance(value, uuid.UUID):
        raise ValueError("Base62 encoding requires a UUID value")

    num = value.int
    if num == 0:
        return BASE62[0]

    arr = []
    while num:
        num, rem = divmod(num, BASE62_LENGTH)
        arr.append(BASE62[rem])

    arr.reverse()
    return "".join(arr)


def decode(value: typing.Union[str, uuid.UUID, "UUIDBase62"]) -> uuid.UUID:
    from .types import UUIDBase62

    if isinstance(value, UUIDBase62):
        return value.uuid
    elif isinstance(value, uuid.UUID):
        return value

    # Decode a Base 62 encoded string into a UUID.
    strlen = len(value)
    num = 0

    for idx, char in enumerate(value):
        power = strlen - (idx + 1)
        num += BASE62.index(char) * (BASE62_LENGTH**power)

    return uuid.UUID(int=num)
