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


class Sample(models.Model):
    """
    Model reprezentující vzorky odebraných sedimentů s názvem, rokem, typem a nepovinným bodem (souřadnice).
    """

    year = SpecialYearField(verbose_name="Rok", help_text="Rok, kdy byl vzorek odebrán")
    name = models.CharField(
        max_length=200, verbose_name="Název vzorku", help_text="Zadejte název vzorku"
    )
    location_type = models.ForeignKey(
        LocationType,
        on_delete=models.CASCADE,
        verbose_name="Typ lokality",
        help_text="Vyberte typ lokality, ze které byl vzorek odebrán",
    )
    point = models.PointField(
        null=True,
        blank=True,
        verbose_name="Bod",
        help_text="Zadejte souřadnice odběru vzorku",
        srid=4326,
    )

    class Meta:
        verbose_name = "Vzorek"
        verbose_name_plural = "Vzorky"
        ordering = ["name", "year"]

    def __str__(self):
        return f"{self.name} ({self.year})"
