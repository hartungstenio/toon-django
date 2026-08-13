"""Django REST Framework integration for :mod:`toon_django`.

Provides a :class:`ToonParser` and a :class:`ToonRenderer` that plug the
Token-Oriented Object Notation (TOON) format into the DRF content-negotiation
pipeline.  Register them on a view or viewset to accept and emit
``application/x-toon`` alongside any other formats DRF already supports.

Example::

    from toon_django.contrib.rest_framework import ToonParser, ToonRenderer


    class MyViewSet(ModelViewSet):
        parser_classes = [ToonParser]
        renderer_classes = [ToonRenderer]
"""

import codecs
from collections.abc import Mapping
from typing import IO, Any, cast

import toon_format as toon
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser
from rest_framework.renderers import BaseRenderer

from toon_django._compat import override


class ToonParser(BaseParser):
    """DRF parser that deserializes ``application/x-toon`` request bodies.

    Decodes an incoming byte stream into a Python object using
    :func:`toon_format.decode`, respecting the encoding declared in the
    parser context (defaults to ``utf-8``).  A malformed payload raises
    :class:`rest_framework.exceptions.ParseError` so DRF can return a proper
    ``400 Bad Request`` response.
    """

    media_type = "application/x-toon"

    @override
    def parse(
        self,
        stream: IO[Any],
        media_type: str | None = None,
        parser_context: Mapping[str, Any] | None = None,
    ) -> Mapping[Any, Any]:
        """Decode a raw TOON payload into a Python object.

        Args:
            stream: The raw request body stream to read and decode.
            media_type: The media type of the incoming request (unused; the
                parser is only invoked when DRF has already matched
                ``application/x-toon``).
            parser_context: Optional dictionary supplied by DRF containing
                contextual information such as ``"encoding"`` (defaults to
                ``"utf-8"`` when absent).

        Returns:
            The Python object produced by :func:`toon_format.decode`.

        Raises:
            :class:`rest_framework.exceptions.ParseError`: If the stream
                cannot be decoded as valid TOON.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", "utf-8")

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            return cast("dict[str, Any]", toon.decode(decoded_stream.read()))
        except ValueError as exc:
            msg = f"TOON parse error - {exc}"
            raise ParseError(msg) from exc


class ToonRenderer(BaseRenderer):
    """DRF renderer that serializes response data as ``application/x-toon``.

    Encodes any Python object to TOON bytes using :func:`toon_format.encode`.
    The renderer is selected by DRF's content negotiation when the client
    sends ``Accept: application/x-toon`` or when it is the only renderer
    configured on the view.
    """

    media_type = "application/x-toon"

    @override
    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, Any] | None = None,
    ) -> str | bytes:
        """Encode *data* to TOON bytes.

        Args:
            data: The Python object to encode (typically the serializer's
                validated output).
            accepted_media_type: The media type accepted by the client
                (unused; already matched to ``application/x-toon`` by DRF).
            renderer_context: Optional dictionary supplied by DRF with
                request/response context (unused by this renderer).

        Returns:
            The TOON-encoded response body as :class:`bytes`.
        """
        if data is None:
            return b""

        encoded = toon.encode(data)
        return encoded.encode()
