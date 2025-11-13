from django.db.models import Prefetch
from rest_framework import viewsets, permissions

from .models import Location, Sample, Measure
from .serializers import (
    MeasureSerializer,
    LocationWithSamplesSerializer,
)


class MeasureViewSet(viewsets.ModelViewSet):
    """
    Základní CRUD API pro jednotlivá měření.
    (můžeš dál rozšiřovat – filtrování, permissions, validace…)
    """
    queryset = Measure.objects.select_related("sample", "parameter")
    serializer_class = MeasureSerializer
    permission_classes = [permissions.AllowAny]  # nebo IsAuthenticated


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API, které vrací lokality se vzorky a měřeními.

    Location → Samples → Measures
    A ZÁROVEŇ:
    - vynechá lokality, které nemají žádný Sample.
    """
    serializer_class = LocationWithSamplesSerializer
    permission_classes = [permissions.AllowAny]

    queryset = (
        Location.objects
        # jen lokality, které mají aspoň jeden Sample
        .filter(sample__isnull=False)
        .distinct()
        .prefetch_related(
            Prefetch(
                "sample_set",
                queryset=Sample.objects.prefetch_related(
                    "measure_set__parameter"
                ),
            )
        )
    )
