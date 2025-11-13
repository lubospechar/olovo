# python
from django.core.management.base import BaseCommand
from pandas import describe_option

from dbolovo.models import Location, LocationType, Parameter, Sample
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
                original_name = row[4]
                sample_number = row[2]
                description = row[5]




                location = Location.objects.get(pk=pk_value)

                sample = Sample.objects.create(
                    location=location,
                    year=year,
                    original_name=original_name,
                    sample_number=sample_number,
                    description=description,
                )