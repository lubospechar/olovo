from rest_framework.viewsets import ReadOnlyModelViewSet
from dbolovo.models import CollectedSample
from dbolovo.serializers import CollectedSampleSerializer

class CollectedSampleViewSet(ReadOnlyModelViewSet):
    """
    API endpoint, který poskytuje data odebraných vzorků ve formátu GeoJSON.
    Vrací pouze vzorky, které mají vyplněné souřadnice (pole `point` není null).
    """
    queryset = CollectedSample.objects.filter(point__isnull=False).filter(measurements__isnull=False).distinct()
    serializer_class = CollectedSampleSerializer

