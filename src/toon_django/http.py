from collections.abc import Mapping
from typing import Any, NotRequired, TypedDict, Unpack

import toon_format as toon
from django.http import HttpResponse


class _HttpResponseBaseParams(TypedDict):
    content_type: NotRequired[str | None]
    status: NotRequired[int | None]
    reason: NotRequired[str | None]
    charset: NotRequired[str | None]
    headers: NotRequired[Mapping[str, str] | None]


class ToonResponse(HttpResponse):
    def __init__(
        self,
        data: Any,
        *,
        safe: bool = True,
        options: toon.EncodeOptions | None = None,
        **kwargs: Unpack[_HttpResponseBaseParams],
    ):
        if safe and not isinstance(data, dict):
            msg = "In order to allow non-dict objects to be serialized set the safe parameter to False."
            raise TypeError(msg)

        kwargs.setdefault("content_type", "application/x-toon")
        data = toon.encode(data, options=options)
        super().__init__(content=data, **kwargs)
