from django.contrib import admin
from dbolovo.models import LocationType, CollectedSample
from django.contrib.gis.admin import GISModelAdmin


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ('location_type',)
    search_fields = ('location_type',)
    ordering = ('location_type',)

@admin.register(CollectedSample)
class CollectedSampleAdmin(GISModelAdmin):
    gis_widget_kwargs = {
        'attrs': {
            'default_lon': 15.5,
            'default_lat': 49.8,
            'default_zoom': 7,
        },
    }
    list_display = ('identifier', 'location_name', 'year', 'location_type', 'get_coordinates')
    search_fields = ('location_name', 'year')
    list_filter = ('location_type',)
    ordering = ('location_name', 'year')
    fields = ('year', 'location_name', 'location_type', 'point')
