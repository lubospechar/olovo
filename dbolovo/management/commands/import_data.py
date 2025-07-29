import pandas as pd
from django.core.management.base import BaseCommand
from dbolovo.models import CollectedSample, SampleMeasurement, Parameter, Unit


class Command(BaseCommand):
    help = 'Načte vzorky z ODS souboru, pokusí se je najít v databázi a uloží hodnoty Pb.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Cesta k ODS souboru se vzorky')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Ověření, že soubor má příponu .ods
        if not file_path.endswith('.ods'):
            self.stderr.write(self.style.ERROR('Podporovány jsou pouze soubory ODS.'))
            return

        # Načtení ODS souboru pomocí pandas a engine 'odf'
        try:
            df = pd.read_excel(file_path, engine='odf')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Chyba při načítání souboru: {str(e)}'))
            return

        # Ověření, že soubor obsahuje potřebné sloupce
        required_columns = ['ROK', 'LOKALITA', 'Pb']
        for column in required_columns:
            if column not in df.columns:
                self.stderr.write(self.style.ERROR(f'Soubor musí obsahovat sloupec s názvem "{column}".'))
                return

        # Parametr a jednotka pro Pb
        parameter_id = 2  # ID parametru Pb
        unit_id = 1       # ID jednotky

        for index, row in df.iterrows():
            year = row.get('ROK')
            location_name = row.get('LOKALITA')
            pb_value = row.get('Pb')

            if not year or not location_name:
                self.stderr.write(
                    self.style.WARNING(f'Řádek {index + 1}: Chybí hodnota pro "ROK" nebo "LOKALITA", přeskočeno.')
                )
                continue

            # Najdi vzorek
            sample = CollectedSample.objects.filter(year=year, location_name=location_name).first()
            if sample:
                self.stdout.write(self.style.SUCCESS(f'Řádek {index + 1}: Nalezen vzorek: {sample}'))

                if pb_value is not None:  # Zkontroluj, jestli Pb není prázdné
                    # Ulož měření do SampleMeasurement
                    measurement, created = SampleMeasurement.objects.get_or_create(
                        sample=sample,
                        parameter_id=parameter_id,
                        defaults={'value': pb_value, 'unit_id': unit_id}
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Přidána hodnota Pb: {pb_value} (Vzorek: {sample.identifier})')
                        )
                    else:
                        # Pokud měření existuje, aktualizuj hodnotu
                        measurement.value = pb_value
                        measurement.unit_id = unit_id
                        measurement.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'Aktualizována hodnota Pb: {pb_value} (Vzorek: {sample.identifier})')
                        )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Řádek {index + 1}: Vzorek nenalezen pro {location_name} ({year}).')
                )

        self.stdout.write(self.style.SUCCESS('Zpracování ODS souboru dokončeno.'))
