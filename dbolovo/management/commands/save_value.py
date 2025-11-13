# python
from django.core.management.base import BaseCommand

from dbolovo.models import Location, LocationType, Parameter, Sample, Measure
import pandas as pd
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        file = '/home/lubos/enki/olovo/zdroj_1.ods'
        list = 'A'
        first_row = 3

        parameter = Parameter.objects.get(pk=1)
        print(parameter)

        df = pd.read_excel(file, sheet_name=list, engine="odf")

        with transaction.atomic():
            for row in df.iloc[first_row:].itertuples(index=False):
                pk_value = row[0]
                year = row[3]
                sample_number = row[2]

                data = row[8]




                location = Location.objects.get(pk=pk_value)

                sample = Sample.objects.get(
                    location=location,
                    year=year,
                    sample_number=sample_number,
                )

                print(data)

