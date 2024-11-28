from django.db import models


class Parameter(models.Model):
    """
    Model reprezentující měřený parametr, jako například pH, obsah těžkých kovů apod.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Název parametru",
        help_text="Zadejte název měřeného parametru, například pH nebo obsah těžkých kovů",
    )

    class Meta:
        verbose_name = "Parametr"
        verbose_name_plural = "Parametry"
        ordering = ["name"]

    def __str__(self):
        return self.name
