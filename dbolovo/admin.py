from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from dbolovo.models import Parameter, LocationType, Location, Unit, Sample


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    # Sloupce zobrazené v přehledu objektů
    list_display = ("name", "unit")

    # Umožní fulltextové vyhledávání podle názvu a jednotky
    search_fields = ("name", "unit")

    # Boční filtr podle jednotky (praktické při menším počtu jednotek)
    list_filter = ("unit",)

    # Výchozí řazení a počet záznamů na stránku
    ordering = ("name",)
    list_per_page = 50

@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    # Sloupce zobrazené v přehledu
    list_display = ("name",)

    # Umožní fulltextové vyhledávání podle názvu typu lokality
    search_fields = ("name",)

    # Výchozí řazení a počet záznamů na stránku
    ordering = ("name",)
    list_per_page = 50

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ("name", "location_type", "lat_display", "lon_display")
    search_fields = ("name", "location_type__name")
    list_filter = ("location_type",)
    ordering = ("name",)
    list_per_page = 50

    def lat_display(self, obj):
        return obj.gps.y if obj.gps else None
    lat_display.short_description = "Lat"

    def lon_display(self, obj):
        return obj.gps.x if obj.gps else None
    lon_display.short_description = "Lon"

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 50


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    # Sloupce v přehledu
    list_display = ("original_name", "sample_number", "year", "location")

    # Vyhledávání
    search_fields = ("original_name", "sample_number", "description")

    # Filtry v postranním panelu
    list_filter = ("year",)

    # Výchozí řazení a optimalizace dotazů
    ordering = ("-year", "original_name")
    list_select_related = ("location",)

    # Ovládání FK pole (rychlejší při větším množství záznamů)
    raw_id_fields = ("location",)

    # Rozdělení do sekcí v detailu záznamu
    fieldsets = (
        (None, {"fields": ("location", "year")}),
        ("Identifikace", {"fields": ("original_name", "sample_number")}),
        ("Popis", {"fields": ("description",)}),
    )

    # Počet položek na stránku v changelistu
    list_per_page = 50

