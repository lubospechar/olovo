import pandas as pd
from django.core.management.base import BaseCommand
from dbolovo.models import Sample
from Levenshtein import distance as levenshtein_distance

class Command(BaseCommand):
    help = 'Aktualizuje souřadnice pro existující záznamy v tabulce Sample na základě názvu lokalit s podporou tolerancí na překlepy.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Cesta k ODS souboru se souřadnicemi')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Načítání ODS souboru pomocí pandas a engine 'odf'
        try:
            df = pd.read_excel(file_path, engine='odf')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Chyba při načítání souboru: {str(e)}'))
            return

        # Ověření, že soubor obsahuje potřebné sloupce
        required_columns = {'LOKALITA', 'LAT', 'LON'}
        if not required_columns.issubset(df.columns):
            self.stderr.write(self.style.ERROR(f'Soubor musí obsahovat sloupce {", ".join(required_columns)}.'))
            return

        # Projdeme každou lokalitu v souboru
        for index, row in df.iterrows():
            file_location_name = str(row['LOKALITA']).replace('_', ' ').strip()
            lat = row['LAT']
            lon = row['LON']

            # Najdeme odpovídající lokality v databázi (ignorujeme podtržítka a tolerujeme překlepy)
            sample_matches = Sample.objects.all()
            possible_matches = []

            for sample in sample_matches:
                db_location_name = sample.location_name.replace('_', ' ').strip()

                # Porovnáme názvy pomocí Levenshteinovy vzdálenosti
                similarity = levenshtein_distance(file_location_name, db_location_name)
                if similarity <= 3:  # Tolerujeme 3 rozdíly
                    possible_matches.append(sample)

            # Pokud najdeme odpovídající záznamy, aktualizujeme všechny shody
            if possible_matches:
                for match in possible_matches:
                    match.point = f'POINT({lon} {lat})'
                    match.save()

                self.stdout.write(self.style.SUCCESS(f'Aktualizováno {len(possible_matches)} záznamů pro lokalitu: {file_location_name} (LAT: {lat}, LON: {lon})'))
            else:
                self.stdout.write(self.style.WARNING(f'Nebylo nalezeno odpovídající pro: {file_location_name}'))
