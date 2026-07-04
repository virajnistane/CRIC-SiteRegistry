# src/rucio/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import RSE
from .serializers import RSESerializer


class RSEViewSet(ModelViewSet):
    queryset         = RSE.objects.select_related("site").all()
    serializer_class = RSESerializer

    def get_queryset(self):
        """
        Supports optional filtering:
          GET /api/rses/?site=<site_id>
          GET /api/rses/?protocol=xrootd
          GET /api/rses/?enabled=true
        """
        qs = super().get_queryset()
        site     = self.request.query_params.get("site")
        protocol = self.request.query_params.get("protocol")
        enabled  = self.request.query_params.get("enabled")

        if site:
            qs = qs.filter(site_id=site)
        if protocol:
            qs = qs.filter(protocol=protocol)
        if enabled is not None:
            qs = qs.filter(enabled=enabled.lower() == "true")
        return qs

    @action(detail=False, methods=["get"], url_path="by-site/(?P<site_id>[0-9]+)")
    def by_site(self, request, site_id=None):
        """
        Convenience endpoint: GET /api/rses/by-site/3/
        Returns all RSEs for site with pk=3.
        """
        rses = self.get_queryset().filter(site_id=site_id)
        serializer = self.get_serializer(rses, many=True)
        return Response(serializer.data)