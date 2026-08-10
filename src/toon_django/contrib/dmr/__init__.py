from collections.abc import Mapping
from http import HTTPStatus
from typing import Any, Callable, override

import toon_format as toon
from django.http import HttpRequest
from dmr.controller import Controller
from dmr.metadata import EndpointMetadata, ResponseSpec
from dmr.parsers import DeserializeFunc, Parser, Raw
from dmr.renderers import Renderer
from dmr.serializer import BaseSerializer


class ToonParser(Parser):
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
    __slots__ = ()

    content_type = "application/x-toon"

    @override
    def render(
        self,
        to_serialize: Any,
        serializer_hook: Callable[[Any], Any],
    ) -> bytes:
        return toon.encode(to_serialize).encode()

    @property
    @override
    def validation_parser(self) -> Parser:
        return ToonParser()
