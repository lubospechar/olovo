from rest_framework import serializers

from .models import Location, Sample, Measure


class MeasureSerializer(serializers.ModelSerializer):
    parameter_name = serializers.SerializerMethodField()
    sample_year = serializers.SerializerMethodField()
    unit = serializers.CharField(source="parameter.unit.symbol")

    class Meta:
        model = Measure
        fields = (
            "id",
            "value",
            "non_measurable_value",
            "parameter_name",
            "sample_year",
            "unit"
        )

    def get_sample_year(self, obj):
        return obj.sample.year if obj.sample else None

    def get_parameter_name(self, obj):
        return obj.parameter.name if obj.parameter else None

class SampleWithMeasuresSerializer(serializers.ModelSerializer):
    # reverzní vztah z Measure.sample → Sample.measure_set
    measures = MeasureSerializer(
        source="measure_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Sample
        fields = (
            "id",
            "year",
            #"original_name",
            #"sample_number",
            #"description",
            "measures",
        )


class LocationWithSamplesSerializer(serializers.ModelSerializer):
    location_type = serializers.SerializerMethodField()
    samples = SampleWithMeasuresSerializer(
        source="sample_set",
        many=True,
        read_only=True
    )

    class Meta:
        model = Location
        fields = (
            "id",
            #"name",
            "location_type",
            "gps",
            "samples",
        )

    def get_location_type(self, obj):
        return obj.location_type.name if obj.location_type else None