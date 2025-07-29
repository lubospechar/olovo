import pandas as pd
from django.core.management.base import BaseCommand
from dbolovo.models import Sample, LocationType

class Command(BaseCommand):
    help = 'Načte vzorky z ODS souboru a uloží je do databáze'

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

        # Předpokládáme, že soubor obsahuje sloupce 'ROK', 'LOKALITA' a 'TYP'
        if not {'ROK', 'LOKALITA', 'TYP'}.issubset(df.columns):
            self.stderr.write(self.style.ERROR('Soubor musí obsahovat sloupce "ROK", "LOKALITA" a "TYP".'))
            return

        # Iterujeme přes všechny řádky a naplníme model Sample
        for index, row in df.iterrows():
            year = int(row['ROK'])
            location_name = str(row['LOKALITA']).strip()
            location_type_value = str(row['TYP']).strip()

            # Najdeme nebo vytvoříme typ lokality
            location_type, created = LocationType.objects.get_or_create(location_type=location_type_value)

            # Vytvoříme nový záznam pro vzorek bez kontroly na unikátnost
            Sample.objects.create(
                year=year,
                location_name=location_name,
                location_type=location_type
            )

            self.stdout.write(self.style.SUCCESS(f'Přidán vzorek: {location_name} ({year})'))

        self.stdout.write(self.style.SUCCESS('Import vzorků dokončen.'))
