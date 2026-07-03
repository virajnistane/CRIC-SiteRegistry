# src/rucio/serializers.py
from rest_framework import serializers

from sites.models import Site
from .models import RSE


class RSESerializer(serializers.ModelSerializer):
    """
    Full RSE serializer.

    - `site_id`   — writable FK (integer); used when creating/updating via API.
    - `site_name` — read-only convenience field so clients don't need a second request.
    - `total_tb` and `utilisation_pct` — computed, read-only.
    """

    site_name       = serializers.CharField(source="site.name", read_only=True)
    total_tb        = serializers.FloatField(read_only=True)
    utilisation_pct = serializers.FloatField(read_only=True)

    class Meta:
        model  = RSE
        fields = [
            "id",
            "name",
            "site",       # writable FK integer
            "site_name",  # read-only string
            "protocol",
            "deterministic",
            "free_tb",
            "used_tb",
            "total_tb",
            "utilisation_pct",
            "enabled",
        ]


class RSENestedSerializer(serializers.ModelSerializer):
    """
    Compact read-only serializer, used when embedding RSE lists inside Site responses.
    """
    class Meta:
        model  = RSE
        fields = ["id", "name", "protocol", "enabled", "free_tb", "used_tb"]