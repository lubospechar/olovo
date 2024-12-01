from rest_framework_gis.serializers import GeoFeatureModelSerializer
from dbolovo.models import CollectedSample

class CollectedSampleSerializer(GeoFeatureModelSerializer):
    """
    Serializer pro model CollectedSample, exportující geografická data jako GeoJSON.
    """

    class Meta:
        model = CollectedSample
        fields = ['id', 'year', 'location_name', 'location_type'] # vybráná pole do geojson
        geo_field = 'point'  # Pole, které obsahuje geografická data


