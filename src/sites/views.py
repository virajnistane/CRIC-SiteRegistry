from django.shortcuts import render # type: ignore
from rest_framework.viewsets import ModelViewSet # type: ignore
from .models import Site
from .serializers import SiteSerializer # type: ignore

# Create your views here.
class SiteViewSet(ModelViewSet):
    # queryset = Site.objects.all()
    queryset = Site.objects.prefetch_related("rses").all()
    serializer_class = SiteSerializer