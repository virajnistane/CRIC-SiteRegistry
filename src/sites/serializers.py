from rest_framework import serializers # type: ignore
from .models import Site

class SiteSerializer(serializers.ModelSerializer):

    rses = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ["id", "name", "region", "status",
                  "cpu_capacity", "storage_tb", "rses"] # "__all__"

    def get_rses(self, obj):
        from rucio.serializers import RSENestedSerializer
        return RSENestedSerializer(obj.rses.all(), many=True).data