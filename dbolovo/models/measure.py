from django.db import models

from dbolovo.models.parameter import Parameter
from dbolovo.models.sample import Sample

class Measure(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.FloatField()
    non_measurable_value = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Měření"
        verbose_name_plural = "Měření"