from http import HTTPStatus
from unittest.mock import MagicMock

import toon_format as toon
from dmr.test import DMRRequestFactory

from toon_django.contrib.dmr import ToonParser, ToonRenderer


class TestToonParser:
    def test_content_type(self) -> None:
        assert ToonParser().content_type == "application/x-toon"

    def test_parse_dict(self, dmr_rf: DMRRequestFactory) -> None:
        request = dmr_rf.post("/", content_type="application/x-toon")
        payload = toon.encode({"key": "value"}).encode()

        result = ToonParser().parse(payload, request=request, model=dict)

        assert result == {"key": "value"}

    def test_parse_list(self, dmr_rf: DMRRequestFactory) -> None:
        request = dmr_rf.post("/", content_type="application/x-toon")
        payload = toon.encode([1, 2, 3]).encode()

        result = ToonParser().parse(payload, request=request, model=list)

        assert result == [1, 2, 3]

    def test_parse_nested_structure(self, dmr_rf: DMRRequestFactory) -> None:
        request = dmr_rf.post("/", content_type="application/x-toon")
        data = {"user": {"name": "Jane", "age": 30}}
        payload = toon.encode(data).encode()

        result = ToonParser().parse(payload, request=request, model=dict)

        assert result == data

    def test_parse_ignores_deserializer_hook(self, dmr_rf: DMRRequestFactory) -> None:
        request = dmr_rf.post("/", content_type="application/x-toon")
        payload = toon.encode({"x": 1}).encode()
        hook = MagicMock()

        ToonParser().parse(payload, deserializer_hook=hook, request=request, model=dict)

        hook.assert_not_called()

    def test_provide_response_specs_returns_empty(self) -> None:
        specs = ToonParser().provide_response_specs(
            MagicMock(),
            MagicMock(),
            {HTTPStatus.OK: MagicMock()},
        )

        assert specs == []


class TestToonRenderer:
    def test_content_type(self) -> None:
        assert ToonRenderer().content_type == "application/x-toon"

    def test_render_returns_bytes(self) -> None:
        result = ToonRenderer().render({"key": "value"}, serializer_hook=lambda x: x)

        assert isinstance(result, bytes)

    def test_render_dict(self) -> None:
        result = ToonRenderer().render({"key": "value"}, serializer_hook=lambda x: x)

        assert toon.decode(result.decode()) == {"key": "value"}

    def test_render_list(self) -> None:
        result = ToonRenderer().render([1, 2, 3], serializer_hook=lambda x: x)

        assert toon.decode(result.decode()) == [1, 2, 3]

    def test_render_roundtrip(self, dmr_rf: DMRRequestFactory) -> None:
        data = {"id": 1, "name": "test"}
        rendered = ToonRenderer().render(data, serializer_hook=lambda x: x)
        request = dmr_rf.post("/", content_type="application/x-toon")

        parsed = ToonParser().parse(rendered, request=request, model=dict)

        assert parsed == data

    def test_validation_parser_is_toon_parser(self) -> None:
        assert isinstance(ToonRenderer().validation_parser, ToonParser)

    def test_validation_parser_returns_new_instance(self) -> None:
        renderer = ToonRenderer()
        first = renderer.validation_parser
        second = renderer.validation_parser

        assert first is not second
