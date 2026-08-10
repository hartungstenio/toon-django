"""Read by Django to configure :mod:`toon_django`."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ToonConfig(AppConfig):
    """:mod:`toon` app configuration."""

    name = "toon_django"
    verbose_name = _("TOON")
