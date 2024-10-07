from django.contrib import admin
from dbolovo.models import LocationType

@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ('location_type',)
    search_fields = ('location_type',)
    ordering = ('location_type',)
