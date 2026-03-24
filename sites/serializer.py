from rest_framework import serializers # type: ignore
from .models import Site

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"
