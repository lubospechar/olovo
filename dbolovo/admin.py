from django.contrib import admin
from dbolovo.models import (
    LocationType,
    CollectedSample,
    Parameter,
    Unit,
    SampleMeasurement,
)
from django.contrib.gis.admin import GISModelAdmin


class SampleMeasurementInline(admin.TabularInline):
    model = SampleMeasurement
    extra = 1


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ("location_type",)
    search_fields = ("location_type",)
    ordering = ("location_type",)


@admin.register(CollectedSample)
class CollectedSampleAdmin(GISModelAdmin):
    gis_widget_kwargs = {
        "attrs": {
            "default_lon": 15.5,
            "default_lat": 49.8,
            "default_zoom": 7,
        },
    }
    list_display = (
        "location_name",
        "identifier",
        "year",
        "location_type",
        "get_coordinates",
    )
    search_fields = ("location_name", "year")
    list_filter = ("location_type",)
    ordering = ("location_name", "year")
    fields = ("year", "location_name", "location_type", "point")
    inlines = [SampleMeasurementInline]


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(SampleMeasurement)
class SampleMeasurementAdmin(admin.ModelAdmin):
    list_display = ("sample", "parameter", "value", "unit")
    search_fields = ("sample__identifier", "parameter__name")
    list_filter = ("parameter", "unit")
    ordering = ("sample", "parameter")


admin.site.site_header = "Olovo Administrace"
admin.site.site_title = "Olovo Admin Portal"
admin.site.index_title = "Vítejte v administraci Olovo"
