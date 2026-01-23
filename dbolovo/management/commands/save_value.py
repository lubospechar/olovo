# python
from django.core.management.base import BaseCommand

from dbolovo.models import Location, LocationType, Parameter, Sample, Measure
import pandas as pd
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        file = '/home/lubos/tmp/samplas.ods'
        list = 'List1'
        first_row = 0

        parameter = Parameter.objects.get(pk=1)
        print(parameter)

        df = pd.read_excel(file, sheet_name=list, engine="odf")

        with transaction.atomic():
            for row in df.iloc[first_row:].itertuples(index=False):
                pk_value = row[5]
                year = row[0]
                sample_number = row[2]

                data = row[4]




                location = Location.objects.get(pk=pk_value)

                sample = Sample.objects.get(
                    location=location,
                    year=year,
                    sample_number=sample_number,
                )

                if pd.isna(data):
                    continue

                non_measureable = False

                if type(data)==str and data.startswith("<"):
                    non_measureable = True
                    num = data[1:].strip().replace(",", ".")
                    value = float(num)
                else:
                    value = data

                print(value, sample_number)

                measure = Measure.objects.create(
                    sample=sample,
                    parameter=parameter,
                    value=value,
                    non_measurable_value=non_measureable,
                )

