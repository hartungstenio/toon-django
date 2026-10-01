"""Django Ninja integration for :mod:`toon_django`.

Provides a :class:`ToonParser` and a :class:`ToonRenderer` that plug the
Token-Oriented Object Notation (TOON) format into Django Ninja's
content-negotiation pipeline.  Pass them to the ``NinjaAPI`` constructor to
accept and emit ``application/x-toon`` alongside any other formats Ninja
already supports.

Example::

    from ninja import NinjaAPI
    from toon_django.contrib.ninja import ToonParser, ToonRenderer


    api = NinjaAPI(parser=ToonParser(), renderer=ToonRenderer())
"""

from typing import Any, cast

import toon_format as toon
from django.http import HttpRequest
from ninja.parser import Parser
from ninja.renderers import BaseRenderer
from ninja.types import DictStrAny

from toon_django._compat import override


class ToonParser(Parser):
    """Django Ninja parser that deserializes ``application/x-toon`` request bodies.

    Decodes raw TOON bytes into a plain Python dictionary using
    :func:`toon_format.decode`.  The result is returned as :class:`DictStrAny`
    so Ninja can coerce it into the declared schema exactly as it would with a
    JSON payload.
    """

    @override
    def parse_body(self, request: HttpRequest) -> DictStrAny:
        """Decode a raw TOON request body into a dictionary.

        Args:
            request: The current Django HTTP request whose body contains a
                TOON-encoded payload.

        Returns:
            The Python dictionary produced by :func:`toon_format.decode`.
        """
        return cast("DictStrAny", toon.decode(request.body.decode()))


class ToonRenderer(BaseRenderer):
    """Django Ninja renderer that serializes response data as ``application/x-toon``.

    Encodes any Python object to TOON bytes using :func:`toon_format.encode`,
    setting the response ``Content-Type`` to ``application/x-toon``.
    """

    media_type = "application/x-toon"

    @override
    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        """Encode *data* to TOON bytes.

        Args:
            request: The current Django HTTP request (unused, required by the
                base-class interface).
            data: The Python object to encode.
            response_status: The HTTP status code for the response (unused,
                required by the base-class interface).

        Returns:
            The TOON-encoded response body as :class:`bytes`.
        """
        return toon.encode(data).encode()
