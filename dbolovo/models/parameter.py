# models/parameter.py
from django.db import models
from dbolovo.models.unit import Unit


class Parameter(models.Model):
    # Název měřeného parametru
    name = models.CharField(
        max_length=100,
        verbose_name="Název parametru",
        help_text="Zadejte název měřeného parametru, například pH nebo obsah těžkých kovů",
    )

    # Jednotka měření
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

    class Meta:
        # Čitelné názvy pro administraci
        verbose_name = "Parametr"
        verbose_name_plural = "Parametry"

        # Výchozí řazení seznamů podle názvu
        ordering = ["name"]

        # Zajištění unikátnosti kombinace názvu a jednotky
        # (např. nemůže existovat dvakrát „Teplota (°C)“)
        constraints = [
            models.UniqueConstraint(fields=["name", "unit"], name="unique_parameter_unit")
        ]

    def __str__(self):
        # Lidsky čitelná reprezentace objektu
        return f"{self.name} ({self.unit})"
