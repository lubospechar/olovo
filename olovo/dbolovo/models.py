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


from django.contrib.gis.db import models
from dbolovo.models import LocationType

class Sample(models.Model):
    """
    Model reprezentující vzorky odebraných sedimentů s rokem, názvem lokality, typem lokality a nepovinným bodem (souřadnice).
    """

    year = models.IntegerField(verbose_name="Rok", help_text="Rok, kdy byl vzorek odebrán")
    location_name = models.CharField(max_length=200, verbose_name="Název lokality", help_text="Zadejte název lokality, kde byl vzorek odebrán")
    location_type = models.ForeignKey(LocationType, on_delete=models.CASCADE, verbose_name="Typ lokality", help_text="Vyberte typ lokality, ze které byl vzorek odebrán")
    point = models.PointField(null=True, blank=True, verbose_name="Bod", help_text="Zadejte souřadnice odběru vzorku", srid=4326)

    class Meta:
        verbose_name = "Vzorek"
        verbose_name_plural = "Vzorky"
        ordering = ['location_name', 'year']

    def __str__(self):
        return f"{self.location_name} ({self.year})"

