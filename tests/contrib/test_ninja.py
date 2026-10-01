import pytest
import toon_format as toon

pytest.importorskip("ninja")

from django.test import RequestFactory

from toon_django.contrib.ninja import ToonParser, ToonRenderer


class TestToonParser:
    def test_parse_body_dict(self, rf: RequestFactory) -> None:
        request = rf.post("/", data=toon.encode({"key": "value"}).encode(), content_type="application/x-toon")

        result = ToonParser().parse_body(request)

        assert result == {"key": "value"}

    def test_parse_body_list(self, rf: RequestFactory) -> None:
        request = rf.post("/", data=toon.encode([1, 2, 3]).encode(), content_type="application/x-toon")

        result = ToonParser().parse_body(request)

        assert result == [1, 2, 3]

    def test_parse_body_nested_structure(self, rf: RequestFactory) -> None:
        data = {"user": {"name": "Jane", "age": 30}}
        request = rf.post("/", data=toon.encode(data).encode(), content_type="application/x-toon")

        result = ToonParser().parse_body(request)

        assert result == data


class TestToonRenderer:
    def test_media_type(self) -> None:
        assert ToonRenderer.media_type == "application/x-toon"

    def test_render_returns_bytes(self, rf: RequestFactory) -> None:
        request = rf.get("/")

        result = ToonRenderer().render(request, {"key": "value"}, response_status=200)

        assert isinstance(result, bytes)

    def test_render_dict(self, rf: RequestFactory) -> None:
        request = rf.get("/")

        result = ToonRenderer().render(request, {"key": "value"}, response_status=200)

        assert toon.decode(result.decode()) == {"key": "value"}

    def test_render_list(self, rf: RequestFactory) -> None:
        request = rf.get("/")

        result = ToonRenderer().render(request, [1, 2, 3], response_status=200)

        assert toon.decode(result.decode()) == [1, 2, 3]

    def test_render_roundtrip(self, rf: RequestFactory) -> None:
        data = {"id": 1, "name": "test"}
        request = rf.get("/")
        rendered = ToonRenderer().render(request, data, response_status=200)

        parse_request = rf.post("/", data=rendered, content_type="application/x-toon")
        parsed = ToonParser().parse_body(parse_request)

        assert parsed == data
