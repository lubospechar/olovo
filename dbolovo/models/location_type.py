# models/location_type.py
from django.db import models  # stačí běžný model, pokud nepoužíváš GIS pole


class LocationType(models.Model):
    """
    Model reprezentující typ lokality, především mokřady.
    Např. rybník, tok, apod.
    """

    # Název typu lokality (unikátní – např. „rybník“, „tůň“)
    name = models.CharField(
        max_length=100,
        verbose_name="Typ lokality",
        help_text="Zadejte název typu mokřadu, například: rybník, tok, zemědělská půda",
        unique=True,
    )

    class Meta:
        # Nastavení pro administraci a ORM
        verbose_name = "Typ lokality"
        verbose_name_plural = "Typy lokalit"
        ordering = ["name"]  # výchozí řazení podle názvu

    def __str__(self):
        # Lidsky čitelná reprezentace objektu (zobrazuje se např. v adminu)
        return self.name
