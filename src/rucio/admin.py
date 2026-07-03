from django.contrib import admin

from .models import RSE


@admin.register(RSE)
class RSEAdmin(admin.ModelAdmin):
    list_display  = ("name", "site", "protocol", "enabled",
                     "free_tb", "used_tb", "utilisation_pct")
    list_filter   = ("protocol", "enabled", "deterministic")
    search_fields = ("name", "site__name")
    raw_id_fields = ("site",)