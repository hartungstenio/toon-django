"""HTTP utilities for serving TOON-encoded responses from Django views.

This module provides :class:`ToonResponse`, a thin subclass of
:class:`~django.http.HttpResponse` that serializes Python objects to the
Token-Oriented Object Notation (TOON) format and sets the appropriate
``Content-Type`` header automatically.
"""

from collections.abc import Mapping
from typing import Any, TypedDict

import toon_format as toon
from django.http import HttpResponse

from ._compat import NotRequired, Unpack


class _HttpResponseBaseParams(TypedDict):
    """Keyword arguments forwarded verbatim to :class:`~django.http.HttpResponse`.

    All fields are optional and mirror the parameters accepted by Django's base
    response class.
    """

    content_type: NotRequired[str | None]
    status: NotRequired[int | None]
    reason: NotRequired[str | None]
    charset: NotRequired[str | None]
    headers: NotRequired[Mapping[str, str] | None]


class ToonResponse(HttpResponse):
    """An HTTP response that serializes *data* as TOON.

    Behaves exactly like :class:`~django.http.HttpResponse`, but encodes the
    payload with :func:`toon_format.encode` and defaults the ``Content-Type``
    to ``application/x-toon``.
    """

    def __init__(
        self,
        data: Any,  # noqa: ANN401
        *,
        safe: bool = True,
        options: toon.EncodeOptions | None = None,
        **kwargs: Unpack[_HttpResponseBaseParams],
    ) -> None:
        """Serialize *data* and initialize the HTTP response.

        Args:
            data: The Python object to encode.  Must be a :class:`dict` when
                *safe* is ``True`` (the default).
            safe: When ``True`` (default), raises :exc:`TypeError` if *data* is
                not a :class:`dict`, mirroring Django's ``JsonResponse``
                behaviour.  Pass ``False`` to allow any serializable object.
            options: Optional :class:`toon_format.EncodeOptions` passed through
                to :func:`toon_format.encode` to control encoding behaviour.
            **kwargs: Additional keyword arguments forwarded to
                :class:`~django.http.HttpResponse` (e.g. ``status``,
                ``headers``).

        Raises:
            TypeError: If *safe* is ``True`` and *data* is not a :class:`dict`.
        """
        if safe and not isinstance(data, dict):
            msg = "In order to allow non-dict objects to be serialized set the safe parameter to False."
            raise TypeError(msg)

        kwargs.setdefault("content_type", "application/x-toon")
        data = toon.encode(data, options=options)
        super().__init__(content=data, **kwargs)
