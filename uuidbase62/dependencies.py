import enum
import http
import typing

import fastapi
from fastapi import Body, Header, Path, Query

from .models import UUIDBase62ModelMixin
from .types import UUIDBase62, to_uuidbase62


class ParamSource(enum.Enum):
    PATH = Path
    QUERY = Query
    HEADER = Header
    BODY = Body


def get_validated_uuidbase62_by_model(
    model: UUIDBase62ModelMixin, field: str, param: str, param_source: ParamSource = ParamSource.PATH
) -> typing.Callable:
    """
    Useful FastAPI dependency injection function to retrieve and validate an inbound param from a Request to a
    UUIDBase62 value
    :param model: Pydantic model containing the desired field
    :param field: the field on the Pydantic model to validate against
    :param param: the name of the inbound Request parameter containing the value to validate
    :param param_source: typically one of Path (default), Header, Query, Body; where the param is expected to be
    found within the Request
    :return: UUIDBase62 value representation of the param from the Request
    """

    def _inner(item_id: str = param_source(..., alias=param)) -> "UUIDBase62":  # type: ignore # noqa: B008
        try:
            return model.to_uuidbase62(field, item_id)
        except ValueError as e:
            status_code = 404
            detail = f"{http.HTTPStatus(status_code).phrase}; {e}"
            raise fastapi.exceptions.HTTPException(status_code=status_code, detail=detail)

    return _inner


def get_validated_uuidbase62(
    param: str, prefix: str = None, param_source: ParamSource = ParamSource.PATH
) -> typing.Callable:
    """
    Useful FastAPI dependency injection function to retrieve and validate an inbound param from a Request to a
    UUIDBase62 value
    :param param: the name of the inbound Request parameter containing the value to validate
    :param prefix: the prefix expected for the UUIDBase62 value
    :param param_source: typically one of Path (default), Header, Query, Body; where the param is expected to be
    found within the Request
    :return: UUIDBase62 value representation of the param from the Request
    """

    def _inner(item_id: str = param_source(..., alias=param)) -> "UUIDBase62":  # type: ignore # noqa: B008
        try:
            return to_uuidbase62(item_id, prefix)
        except ValueError as e:
            status_code = 404
            detail = f"{http.HTTPStatus(status_code).phrase}; {e}"
            raise fastapi.exceptions.HTTPException(status_code=status_code, detail=detail)

    return _inner
