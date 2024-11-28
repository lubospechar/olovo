from django.db import models
from .collected_sample import CollectedSample
from .parameter import Parameter
from .unit import Unit


class SampleMeasurement(models.Model):
    """
    Model reprezentující naměřená data ze vzorků, jako například pH, obsah těžkých kovů apod.
    """

    sample = models.ForeignKey(
        CollectedSample,
        on_delete=models.CASCADE,
        related_name="measurements",
        verbose_name="Vzorek",
        help_text="Vyberte vzorek, ke kterému tato měření patří",
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        verbose_name="Parametr",
        help_text="Vyberte měřený parametr",
    )
    value = models.FloatField(
        verbose_name="Hodnota",
        help_text="Zadejte naměřenou hodnotu parametru",
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name="Jednotka",
        help_text="Vyberte jednotku měření",
    )

    class Meta:
        verbose_name = "Měření vzorku"
        verbose_name_plural = "Měření vzorků"
        ordering = ["sample", "parameter"]

    def __str__(self):
        return f"{self.parameter} ({self.value} {self.unit}) - {self.sample.identifier}"
