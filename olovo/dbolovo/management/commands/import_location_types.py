import pandas as pd
from django.core.management.base import BaseCommand
from dbolovo.models import LocationType

class Command(BaseCommand):
    help = 'Načte typy lokalit z ODS souboru a uloží je do databáze'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Cesta k ODS souboru s typy lokalit')

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

        # Předpokládáme, že první sloupec obsahuje typy lokalit
        if 'TYP' not in df.columns:
            self.stderr.write(self.style.ERROR('Soubor musí obsahovat sloupec s názvem "TYP".'))
            return

        # Načteme jednotlivé typy lokalit a vložíme je do databáze
        for index, row in df.iterrows():
            location_type_value = str(row['TYP']).strip()

            if location_type_value:
                location_type, created = LocationType.objects.get_or_create(
                    location_type=location_type_value
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Přidán typ lokality: {location_type_value}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Typ lokality již existuje: {location_type_value}'))

        self.stdout.write(self.style.SUCCESS('Import typů lokalit dokončen.'))
