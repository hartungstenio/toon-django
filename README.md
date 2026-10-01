# toon-django

[![PyPI - Version](https://img.shields.io/pypi/v/toon-django.svg)](https://pypi.org/project/toon-django)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/toon-django.svg)](https://pypi.org/project/toon-django)

Django integration for the [Token-Oriented Object Notation (TOON)](https://pypi.org/project/toon-format) format. Provides a `ToonResponse` for plain Django views and parsers/renderers for Django REST Framework, Django Ninja, and Django Modern REST, so you can accept and emit `text/toon` alongside your existing content types with minimal setup.

---

## Installation

The base package works with plain Django out of the box:

```console
pip install toon-django
```

Install optional extras for the frameworks you use:

```console
# Django Modern REST
pip install "toon-django[dmr]"

# Django Ninja
pip install "toon-django[ninja]"

# Django REST Framework
pip install "toon-django[drf]"
```

## Usage

### Plain Django

Use `ToonResponse` in any view the same way you would use `JsonResponse`:

```python
from toon_django.http import ToonResponse


def my_view(request):
    return ToonResponse({"hello": "world"})
```

Pass `safe=False` to serialize non-dict objects such as lists:

```python
def my_list_view(request):
    return ToonResponse([1, 2, 3], safe=False)
```

### Django Modern REST

Register `ToonParser` and `ToonRenderer` on a controller:

```python
from dmr.controller import Controller
from toon_django.contrib.dmr import ToonParser, ToonRenderer


class MyController(Controller):
    parsers = [ToonParser()]
    renderers = [ToonRenderer()]
```

### Django Ninja

Pass `ToonParser` and `ToonRenderer` to the `NinjaAPI` constructor:

```python
from ninja import NinjaAPI
from toon_django.contrib.ninja import ToonParser, ToonRenderer


api = NinjaAPI(parser=ToonParser(), renderer=ToonRenderer())
```

The API will then accept and emit `Content-Type: text/toon`.

### Django REST Framework

Register `ToonParser` and `ToonRenderer` on a view or viewset:

```python
from rest_framework.viewsets import ModelViewSet
from toon_django.contrib.rest_framework import ToonParser, ToonRenderer


class MyViewSet(ModelViewSet):
    parser_classes = [ToonParser]
    renderer_classes = [ToonRenderer]
```

The parser accepts `Content-Type: text/toon` requests; the renderer responds to `Accept: text/toon`.

You can also set them globally in `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "toon_django.contrib.rest_framework.ToonParser",
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "toon_django.contrib.rest_framework.ToonRenderer",
        "rest_framework.renderers.JSONRenderer",
    ],
}
```

## License

`toon-django` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
