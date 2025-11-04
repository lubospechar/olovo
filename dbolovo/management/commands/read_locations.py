# dbolovo/management/commands/import_locations.py
import re
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from dbolovo.models import Location  # uprav cestu na tvoji app


def dms_to_decimal(dms_str):
    """
    Převede souřadnice ve formátu D°M'S"X na desetinné stupně.
    Podporuje i varianty s mezerou místo čárky.
    Vrací (lat, lon) nebo (None, None) při chybě.
    """
    if not isinstance(dms_str, str):
        return None, None

    s = dms_str.replace(",", " ").replace("  ", " ").strip()
    pattern = re.compile(
        r"(\d+)[°\s]+(\d+)'?[\s]*(\d+(?:\.\d+)?)?\"?([NSEW])",
        re.IGNORECASE,
    )
    parts = pattern.findall(s)
    if len(parts) < 2:
        return None, None

    def single_to_decimal(deg, minute, second, hemi):

        deg = float(deg)
        minute = float(minute)
        second = float(second) if second else 0.0
        dec = deg + minute / 60 + second / 3600
        if hemi.upper() in ["S", "W"]:
            dec = -dec
        return dec

    lat = single_to_decimal(*parts[0])
    lon = single_to_decimal(*parts[1])
    return lat, lon


class Command(BaseCommand):
    help = "Importuje lokality z ODS souboru do modelu Location, včetně nastavení PK podle sloupce ID."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            nargs="?",
            type=str,
            default="lokality.ods",
            help="Cesta k souboru ODS s lokalitami (výchozí: lokality.ods)",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        self.stdout.write(f"Načítám soubor: {file_path}")

        try:
            df = pd.read_excel(file_path, engine="odf", sheet_name="List1")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Chyba při čtení {file_path}: {e}"))
            return

        # očistíme názvy sloupců
        df.columns = [col.strip() for col in df.columns]

        expected_cols = {"ID", "lokalita", "GPS"}
        if not expected_cols.issubset(set(df.columns)):
            self.stderr.write(
                self.style.ERROR(
                    f"Neočekávané sloupce: {set(df.columns)} — očekáváno {expected_cols}"
                )
            )
            return

        created = 0
        skipped = 0

        for _, row in df.iterrows():
            if pd.isna(row["ID"]) or pd.isna(row["lokalita"]) or pd.isna(row["GPS"]):
                skipped += 1
                continue

            pk = int(row["ID"])
            name = str(row["lokalita"]).strip()
            gps_raw = str(row["GPS"]).strip()

            lat, lon = dms_to_decimal(gps_raw)
            if lat is None or lon is None:
                self.stdout.write(
                    self.style.WARNING(f"Přeskočeno (neplatné GPS): {name} – {gps_raw}")
                )
                skipped += 1
                continue

            point = Point(lon, lat, srid=4326)

            # protože je tabulka prázdná, můžeme rovnou vkládat s id=pk
            Location.objects.create(
                id=pk,
                name=name,
                gps=point,
                location_type=None,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS("Import dokončen."))
        self.stdout.write(f"Vytvořeno: {created}")
        self.stdout.write(f"Přeskočeno: {skipped}")
