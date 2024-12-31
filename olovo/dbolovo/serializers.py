from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from dbolovo.models import CollectedSample, SampleMeasurement

class SampleMeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer pro model SampleMeasurement.
    """
    parameter_name = serializers.CharField(source='parameter.name')
    unit_name = serializers.CharField(source='unit.name', allow_null=True)

    class Meta:
        model = SampleMeasurement
        fields = ['id', 'parameter_name', 'value', 'unit_name']

class CollectedSampleSerializer(GeoFeatureModelSerializer):
    """
    Serializer pro model CollectedSample, exportující geografická data jako GeoJSON.
    """
    measurements = SampleMeasurementSerializer(many=True, read_only=True)

    class Meta:
        model = CollectedSample
        fields = ['id', 'year', 'location_name', 'location_type', 'measurements']  # Přidáno 'measurements'
        geo_field = 'point'  # Pole, které obsahuje geografická data
