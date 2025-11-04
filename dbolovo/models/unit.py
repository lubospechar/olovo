from django.db import models


class Unit(models.Model):
    """
    Model reprezentující jednotku měření, jako například mg/l, pH apod.
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Jednotka",
        help_text="Zadejte jednotku měření, například mg/l nebo pH",
    )

    symbol = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Jednotka"
        verbose_name_plural = "Jednotky"
        ordering = ["name"]


    def __str__(self) -> str:
        if self.symbol:
            return f"{self.name} ({self.symbol})"
        return self.name
