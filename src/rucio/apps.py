# src/rucio/apps.py
from django.apps import AppConfig


class RucioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rucio"          # must match INSTALLED_APPS entry

    