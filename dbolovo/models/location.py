# models/location.py
from django.contrib.gis.db import models
from .location_type import LocationType


class Location(models.Model):
    """
    Model reprezentující konkrétní lokalitu, např. konkrétní rybník nebo tůň.
    Obsahuje název, typ lokality a její GPS souřadnice.
    """

    # Název lokality, např. „Rybník Hluboký“ nebo „Tůň u lesa“
    name = models.CharField(
        max_length=200,
        verbose_name="Název lokality",
        help_text="Zadejte název konkrétní lokality, například: Rybník Hluboký",
        unique=True,
    )

    # Typ lokality (např. rybník, tůň, stoka)
    location_type = models.ForeignKey(
        LocationType,
        on_delete=models.PROTECT,
        verbose_name="Typ lokality",
        help_text="Vyberte typ této lokality, např. rybník, tůň nebo stoka",
        related_name="locations",
        null=True,
    )

    # GPS souřadnice (v systému WGS84)
    gps = models.PointField(
        verbose_name="GPS souřadnice",
        help_text="Zadejte souřadnice lokality (ve formátu WGS84)",
        srid=4326,  # standardní souřadnicový systém GPS
    )

    class Meta:
        verbose_name = "Lokalita"
        verbose_name_plural = "Lokality"
        ordering = ["name"]

    def __str__(self):
        # Vrací čitelný název včetně typu lokality
        return f"{self.name} ({self.location_type})"