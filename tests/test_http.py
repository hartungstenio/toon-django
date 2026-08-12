from http import HTTPStatus

import pytest
import toon_format as toon

from toon_django.http import ToonResponse


class TestToonResponse:
    def test_default_args(self) -> None:
        response = ToonResponse({"key": "value"})

        assert response.status_code == HTTPStatus.OK
        assert response["Content-Type"] == "application/x-toon"
        assert toon.decode(response.content.decode()) == {"key": "value"}

    def test_custom_content_type(self) -> None:
        response = ToonResponse({}, content_type="application/x-toon; charset=utf-8")

        assert response["Content-Type"] == "application/x-toon; charset=utf-8"

    def test_custom_status_code(self) -> None:
        response = ToonResponse({}, status=HTTPStatus.CREATED)

        assert response.status_code == HTTPStatus.CREATED

    def test_non_dict_not_safe(self) -> None:
        with pytest.raises(TypeError):
            ToonResponse([1, 2, 3])

    def test_list(self) -> None:
        response = ToonResponse([1, 2, 3], safe=False)

        assert toon.decode(response.content.decode()) == [1, 2, 3]

    def test_options(self) -> None:
        response = ToonResponse([{"a": 1}, {"b": 2}], safe=False, options={"delimiter": "|", "indent": 1})
        assert response.content == b"[2|]:\n - a: 1\n - b: 2"
