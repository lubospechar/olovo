from django.contrib.gis.db import models
from dbolovo.fields import SpecialYearField


class LocationType(models.Model):
    """
    Model reprezentující typ lokality, především mokřady jako např. rybník, tůň, stoka.
    """

    location_type = models.CharField(
        max_length=100,
        verbose_name="Typ lokality",
        help_text="Zadejte název typu mokřadu, například: rybník, tůň, stoka",
        unique=True,
    )

    class Meta:
        verbose_name = "Typ lokality"
        verbose_name_plural = "Typy lokalit"
        ordering = ["location_type"]

    def __str__(self):
        return self.location_type


class Location(models.Model):
    """
    Model reprezentující konkrétní lokalitu s jejím názvem, rokem a typem.
    Nepovinně je možné zadat i souřadnice jako bod.
    """

    year = SpecialYearField(
        verbose_name="Rok", help_text="Rok, kdy byla lokalita zaznamenána"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Název lokality",
        help_text="Zadejte název lokality",
    )
    location_type = models.ForeignKey(
        LocationType,
        on_delete=models.CASCADE,
        verbose_name="Typ lokality",
        help_text="Vyberte typ lokality",
    )
    point = models.PointField(
        null=True,
        blank=True,
        verbose_name="Bod",
        help_text="Zadejte souřadnice lokality",
        srid=4326,
    )

    class Meta:
        verbose_name = "Lokalita"
        verbose_name_plural = "Lokality"
        ordering = ["name", "year"]

    def __str__(self):
        return f"{self.name} ({self.year})"
