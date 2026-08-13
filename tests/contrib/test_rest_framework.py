import io
from unittest.mock import patch

import pytest
import toon_format as toon

pytest.importorskip("rest_framework")

from rest_framework.exceptions import ParseError

from toon_django.contrib.rest_framework import ToonParser, ToonRenderer


class TestToonParser:
    def test_media_type(self) -> None:
        assert ToonParser.media_type == "application/x-toon"

    def test_parse_dict(self) -> None:
        data = {"key": "value"}
        stream = io.BytesIO(toon.encode(data).encode())

        result = ToonParser().parse(stream)

        assert result == data

    def test_parse_list(self) -> None:
        data = [1, 2, 3]
        stream = io.BytesIO(toon.encode(data).encode())

        result = ToonParser().parse(stream)

        assert result == data

    def test_parse_custom_encoding(self) -> None:
        data = {"key": "value"}
        stream = io.BytesIO(toon.encode(data).encode("latin-1"))

        result = ToonParser().parse(stream, parser_context={"encoding": "latin-1"})

        assert result == data

    def test_parse_raises_parse_error_on_invalid_toon(self) -> None:
        stream = io.BytesIO(b"any payload")

        with (
            patch("toon_django.contrib.rest_framework.toon.decode", side_effect=ValueError("bad")),
            pytest.raises(ParseError),
        ):
            ToonParser().parse(stream)


class TestToonRenderer:
    def test_media_type(self) -> None:
        assert ToonRenderer.media_type == "application/x-toon"

    def test_render_returns_bytes(self) -> None:
        result = ToonRenderer().render({"key": "value"})

        assert isinstance(result, bytes)

    def test_render_dict(self) -> None:
        data = {"key": "value"}
        result = ToonRenderer().render(data)

        assert toon.decode(result.decode()) == data

    def test_render_list(self) -> None:
        data = [1, 2, 3]
        result = ToonRenderer().render(data)

        assert toon.decode(result.decode()) == data

    def test_render_none(self) -> None:
        result = ToonRenderer().render(None)

        assert result.decode() == ""
