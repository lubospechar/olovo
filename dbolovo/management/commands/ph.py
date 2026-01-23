from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from dbolovo.models import *

REQUIRED_COLS = ["ROK", "jmeno", "typ", "olovo", "ph", "sample"]


class Command(BaseCommand):
    help = "Read XLSX and iterate rows with columns: ROK, jmeno, typ, olovo, ph."

    def add_arguments(self, parser):
        parser.add_argument("xlsx_path", type=str, help="Path to the XLSX file")
        parser.add_argument(
            "--sheet",
            type=str,
            default=0,
            help="Sheet name or index (default: 0 = first sheet)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Print only first N rows (0 = all)",
        )

    def handle(self, *args, **options):
        xlsx_path: str = options["xlsx_path"]
        sheet_opt = options["sheet"]
        limit: int = options["limit"]

        # sheet: "0" -> 0, jinak název
        try:
            sheet = int(sheet_opt)
        except (TypeError, ValueError):
            sheet = sheet_opt

        try:
            df = pd.read_excel(
                xlsx_path,
                sheet_name=sheet,
                engine="openpyxl",
                dtype=object,  # nesahej pandasem na typy, zatím chceme "co je v buňce"
            )
        except Exception as e:
            raise CommandError(f"Cannot read XLSX '{xlsx_path}': {e}")

        # Normalizace názvů sloupců (kvůli mezerám apod.)
        df.columns = [str(c).strip() for c in df.columns]

        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            raise CommandError(
                f"Missing columns: {missing}. Available columns: {list(df.columns)}"
            )

        # Vyber jen potřebné sloupce (v správném pořadí)
        df = df[REQUIRED_COLS]

        # Projdi řádky (rychlé a čitelné)
        count = 0
        for row in df.itertuples(index=False, name=None):
            rok, jmeno, typ, olovo, ph, sample = row


            s = Sample.objects.get(pk=sample)
            p = Parameter.objects.get(pk=2)

            new_m = Measure(sample=s, parameter=p, value=ph)
            new_m.save()



            print(p, s, ph)
            count += 1
            if limit and count >= limit:
                break

        self.stdout.write(self.style.SUCCESS(f"Done. Processed {count} row(s)."))
