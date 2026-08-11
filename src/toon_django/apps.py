"""Django app configuration for :mod:`toon_django`.

This module is auto-discovered by Django and registers the ``toon_django``
application with the project's app registry.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ToonConfig(AppConfig):
    """Configuration for the ``toon_django`` Django application.

    Registers the app under the ``toon_django`` label and exposes it in the
    admin and other Django internals as *TOON*.
    """

    name = "toon_django"
    verbose_name = _("TOON")
