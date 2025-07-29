
# Olovo - TAČR Projekt

Tento projekt je součástí výzkumu v rámci **TAČR** na téma _"Metody screeningu a kvantifikace olova v mokřadech a na ZPF – návrh vhodných kritérií pro detekci rizikových lokalit"_.

## Olovo Django Projekt

Tento software je postaven na **Django** frameworku a používá **PostgreSQL** s rozšířením **PostGIS** pro zpracování geografických dat. Projekt umožňuje práci s databázemi, které obsahují geografická data, s cílem mapování a analýzy lokalit zatížených olovem.

## Klíčové funkce
- Správa lokalit zatížených olovem pomocí REST API.
- Export dat ve formátu GeoJSON.
- Podpora geografických dat pomocí **PostGIS**.
- Read-only API pro zajištění bezpečnosti dat.

## Požadavky

Pro úspěšné spuštění projektu jsou vyžadovány následující technologie a knihovny:

- **Python 3.10+**
- **Django 5.1.3**
- **PostgreSQL** s nainstalovaným rozšířením **PostGIS**
- **pip** pro správu balíčků Pythonu

## Instalace

1. **Klonování repozitáře:**
   ```bash
   git clone <url_repozitáře>
   cd <název_projektu>
   ```

2. **Nainstalujte závislosti:**
   Ujistěte se, že máte vytvořené a aktivované virtuální prostředí:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Nastavte databázi:**
   Upravte `.env` soubor s následujícími klíči:
   ```
   DB_NAME=<název_databáze>
   DB_USER=<uživatel>
   DB_PASSWORD=<heslo>
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

4. **Proveďte migrace:**
   ```bash
   python manage.py migrate
   ```

5. **Spusťte vývojový server:**
   ```bash
   python manage.py runserver
   ```

## Použité knihovny

Seznam hlavních knihoven, které projekt využívá:
- **Django**: Základní framework.
- **PostGIS**: Rozšíření pro PostgreSQL pro práci s geografickými daty.
- **Django REST Framework**: Tvorba REST API.
- **djangorestframework-gis**: Rozšíření pro práci s GeoJSON daty.
- **pandas**: Analýza dat.
- **numpy**: Výpočty s numerickými daty.

## Spuštění testů

Pro spuštění testů:
```bash
python manage.py test
```
