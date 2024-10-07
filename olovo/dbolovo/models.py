from django.db import models

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
        ordering = ['location_type']

    def __str__(self):
        return self.location_type
