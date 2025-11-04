# python
from django.core.management.base import BaseCommand
from dbolovo.models import Location, LocationType
import pandas as pd


class Command(BaseCommand):
    help = (
        "Přiřadí Location.location_type podle ODS. "
        "Očekává sloupce: ID (pk Location) a TYP (LocationType.name). "
        "Chybějící typy vytvoří."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            nargs="?",
            type=str,
            default="lokality.ods",
            help="Cesta k ODS souboru (výchozí: lokality.ods)",
        )
        parser.add_argument(
            "--sheet",
            type=str,
            default="List1",
            help="Název listu v ODS (výchozí: List1)",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        sheet_name = options["sheet"]

        self.stdout.write(f"Načítám soubor: {file_path} (list: {sheet_name})")
        try:
            df = pd.read_excel(file_path, engine="odf", sheet_name=sheet_name)
        except Exception as e:
            self.stderr.write(f"Chyba při čtení ODS: {e}")
            return

        # Najdeme názvy sloupců case-insensitive
        def find_col(df_cols, wanted_lower):
            for c in df_cols:
                if str(c).strip().lower() == wanted_lower:
                    return c
            return None

        id_col = find_col(df.columns, "id")
        typ_col = find_col(df.columns, "typ")

        if id_col is None or typ_col is None:
            self.stderr.write("V souboru musí být sloupce 'ID' a 'TYP' (nezáleží na velikosti písmen).")
            return

        total_rows = len(df)
        updated = 0
        created_types = 0
        skipped = 0
        not_found = 0
        errors = 0

        for idx, row in df[[id_col, typ_col]].iterrows():
            loc_id = row[id_col]
            typ_val = row[typ_col]

            # Přeskoč prázdné řádky
            if pd.isna(loc_id) or pd.isna(typ_val):
                skipped += 1
                continue

            # Připrav ID a název typu
            try:
                loc_id_int = int(loc_id)
            except Exception:
                self.stderr.write(f"Řádek {idx}: neplatné ID '{loc_id}' – přeskočeno.")
                errors += 1
                continue

            typ_name = str(typ_val).strip()
            if not typ_name:
                skipped += 1
                continue

            # Najdi Location
            try:
                location = Location.objects.get(pk=loc_id_int)
            except Location.DoesNotExist:
                self.stderr.write(f"ID {loc_id_int}: Location nenalezen – přeskočeno.")
                not_found += 1
                continue

            # Najdi nebo vytvoř LocationType
            lt, created = LocationType.objects.get_or_create(name=typ_name)
            if created:
                created_types += 1

            # Aktualizuj pouze pokud je změna potřeba
            if location.location_type_id == lt.id:
                skipped += 1
                continue

            location.location_type = lt
            location.save(update_fields=["location_type"])
            updated += 1

        self.stdout.write("Hotovo.")
        self.stdout.write(
            f"Řádků v souboru: {total_rows}, aktualizováno: {updated}, "
            f"vytvořené typy: {created_types}, přeskočeno: {skipped}, "
            f"nenalezené Location: {not_found}, chyby: {errors}"
        )