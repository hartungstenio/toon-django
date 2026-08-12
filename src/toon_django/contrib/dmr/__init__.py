"""DMR integration for :mod:`toon_django`.

Provides a :class:`ToonParser` and a :class:`ToonRenderer` that plug the
Token-Oriented Object Notation (TOON) format into the DMR content-negotiation
pipeline.  Register them on a controller to accept and emit ``application/x-toon``
alongside any other formats DMR already supports.

Example::

    from toon_django.contrib.dmr import ToonParser, ToonRenderer


    class MyController(Controller):
        parsers = [ToonParser()]
        renderers = [ToonRenderer()]
"""

from collections.abc import Callable, Mapping
from http import HTTPStatus
from typing import Any

import toon_format as toon
from django.http import HttpRequest
from dmr.controller import Controller
from dmr.metadata import EndpointMetadata, ResponseSpec
from dmr.parsers import DeserializeFunc, Parser, Raw
from dmr.renderers import Renderer
from dmr.serializer import BaseSerializer

from toon_django._compat import override


class ToonParser(Parser):
    """DMR parser that deserializes ``application/x-toon`` request bodies.

    Decodes raw TOON bytes into a Python object using
    :func:`toon_format.decode`.  The resulting value is then handed to the
    controller's deserializer exactly as any other parser's output would be.
    """

    __slots__ = ()

    content_type = "application/x-toon"

    @override
    def parse(
        self,
        to_deserialize: Raw,
        deserializer_hook: DeserializeFunc | None = None,
        *,
        request: HttpRequest,
        model: Any,
    ) -> Any:
        """Decode a raw TOON payload into a Python object.

        Args:
            to_deserialize: The raw request body bytes to decode.
            deserializer_hook: Optional callable for custom post-decode
                transformation (not used by this parser).
            request: The current Django HTTP request.
            model: The target model class the parsed data will be coerced into.

        Returns:
            The Python object produced by :func:`toon_format.decode`.
        """
        return toon.decode(to_deserialize.decode())

    @override
    def provide_response_specs(
        self,
        metadata: EndpointMetadata,
        controller_cls: type[Controller[BaseSerializer]],
        existing_responses: Mapping[HTTPStatus, ResponseSpec],
    ) -> list[ResponseSpec]:
        """Provide responses that can happen when data can't be parsed."""
        return []


class ToonRenderer(Renderer):
    """DMR renderer that serializes response data as ``application/x-toon``.

    Encodes any Python object to TOON bytes using :func:`toon_format.encode`,
    applying the controller's serializer hook before encoding so that model
    instances are properly converted to plain Python structures first.
    """

    __slots__ = ()

    content_type = "application/x-toon"

    @override
    def render(
        self,
        to_serialize: Any,
        serializer_hook: Callable[[Any], Any],
    ) -> bytes:
        """Encode *to_serialize* to TOON bytes.

        Args:
            to_serialize: The Python object to encode.
            serializer_hook: Callable that converts the object (e.g. a model
                instance) to a plain Python structure before encoding.

        Returns:
            The TOON-encoded response body as :class:`bytes`.
        """
        return toon.encode(to_serialize).encode()

    @property
    @override
    def validation_parser(self) -> Parser:
        """Return a :class:`ToonParser` used to validate round-trip encoding."""
        return ToonParser()
