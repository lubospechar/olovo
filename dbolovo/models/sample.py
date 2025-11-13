from django.db import models

from dbolovo.fields import SpecialYearField
from dbolovo.models.location import Location

class Sample(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    year = SpecialYearField()
    original_name = models.CharField(max_length=100)
    sample_number = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ["year", "location"]
        unique_together = ["year", "location", "sample_number"]

