#!/usr/bin/env python3
"""A data/locations.js eloallitasa foldrajzi koordinatakbol.

Forras: Website_Countries_Locations_12.08.2026.xlsx (ugyfel, 2026-08-12),
34 sor, negy regioban.

Miert szkript es nem kezzel irt JS: a korabbi 16 placeholder-pont kezzel volt
belove, es lathatoan pontatlan lett -- a "Germany" pont pl. a 39. szelessegi
fokon ult, ami Szardinia magassaga. A vetites keplete egyetlen helyen (itt)
van leirva, es meg kell egyeznie a tools/build_map.py-beliVel, kulonben a
pontok elcsusznak a terkephez kepest.

Futtatas, ha a telephely-lista valtozik:
    python tools/build_locations.py
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "locations.js"

# --- Vetites. UGYANAZ, mint a tools/build_map.py-ban. -------------------
# A world.svg viewBox-a "-0.5 -0.5 150 60": a rajzterulet -0,5-tol 149,5-ig
# tart vizszintesen es -0,5-tol 59,5-ig fuggolegesen. A pontokat a CSS
# szazalekban helyezi el ezen a dobozon belul, ezert a fel egysegnyi
# eltolast bele kell szamolni -- enelkul minden pont 0,33%-kal balra es
# 0,83%-kal feljebb kerulne.
COLS, ROWS = 150, 60
VB_X, VB_Y = -0.5, -0.5
LAT_TOP, LAT_BOTTOM = 83.0, -60.0


def project(lon, lat):
    sx = (lon + 180.0) / 360.0 * COLS
    sy = (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * ROWS
    return round((sx - VB_X) / COLS * 100, 2), round((sy - VB_Y) / ROWS * 100, 2)


# --- Az adat. (terulet, orszag, varos, lat, lon, megjegyzes) -------------
# A megjegyzes NEM kerul a kimenetbe: azt jelzi, hol tertunk el az xlsx-tol
# vagy hol bizonytalan az azonositas. Ezek mind vissza vannak jelezve.
SITES = [
    # --- Americas ---
    ("Americas", "USA", "Auburn Hills", 42.6875, -83.2341,
     "xlsx: 'Auburn' -- Auburn Hills, megerositve 2026-08-14"),
    ("Americas", "USA", "Sun Prairie", 43.1836, -89.2137,
     "xlsx: egy cellaban 'Sun Prairie Rochester Hills' -- ketto"),
    ("Americas", "USA", "Rochester Hills", 42.6584, -83.1499, "ugyanabbol a cellabol"),
    ("Americas", "USA", "Somersworth", 43.2617, -70.8664, None),
    ("Americas", "Mexico", "Delicias", 28.1900, -105.4700, None),
    ("Americas", "Mexico", "Monterrey", 25.6866, -100.3161, None),
    ("Americas", "Mexico", "Montemorelos", 25.1889, -99.8283, "xlsx: 'Monteremorelos'"),
    ("Americas", "Mexico", "San Luis Potosí", 22.1565, -100.9855, "xlsx: '(2 locations)'"),
    ("Americas", "Mexico", "Tlalnepantla", 19.5400, -99.1950, None),
    ("Americas", "Brazil", "Ponta Grossa", -25.0950, -50.1619, None),

    # --- EMEA West ---
    ("EMEA West", "Germany", "Hann. Münden", 51.4167, 9.6500, "harom varos egy cellaban"),
    ("EMEA West", "Germany", "Waltershausen", 50.8983, 10.5583, "ugyanabbol a cellabol"),
    ("EMEA West", "Germany", "Hamburg", 53.5511, 9.9937, "ugyanabbol a cellabol"),
    ("EMEA West", "Germany", "Korbach", 51.2739, 8.8731, None),
    ("EMEA West", "Germany", "Hannover", 52.3759, 9.7320, None),
    ("EMEA West", "France", "Caluire-et-Cuire", 45.7947, 4.8464, "xlsx: 'Caluire'"),
    ("EMEA West", "France", "Andrézieux-Bouthéon", 45.5253, 4.2606, "xlsx: 'Andrézieux'"),
    ("EMEA West", "France", "Rennes", 48.1173, -1.6778, "xlsx: 'Renees' -- felteszem, Rennes"),
    ("EMEA West", "Austria", "Vienna", 48.2082, 16.3738, "xlsx: 'Wiena'"),
    ("EMEA West", "Morocco", "Tangier", 35.7595, -5.8340, "xlsx: 'Tanger'"),
    ("EMEA West", "Netherlands", "Maastricht", 50.8514, 5.6910, None),
    ("EMEA West", "Portugal", "Porto", 41.1579, -8.6291, None),

    # --- EMEA East ---
    ("EMEA East", "Hungary", "Makó", 46.2167, 20.4833, "xlsx: 'Mako'"),
    ("EMEA East", "Hungary", "Vác", 47.7756, 19.1364, "xlsx: 'Vac'"),
    ("EMEA East", "Romania", "Carei", 47.6833, 22.4667, None),
    ("EMEA East", "Romania", "Timișoara", 45.7489, 21.2087, "xlsx: 'Timisoara'"),
    ("EMEA East", "Slovenia", "Kranj", 46.2389, 14.3556, None),
    ("EMEA East", "Slovakia", "Dolné Vestenice", 48.7333, 18.4167, "xlsx: 'Dolne Vestenice'"),
    ("EMEA East", "Serbia", "Subotica", 46.1000, 19.6650, None),
    ("EMEA East", "Czech Republic", "Ostrava", 49.8209, 18.2625, "xlsx: 'Ostava'"),

    # --- APAC ---
    ("APAC", "China", "Changchun", 43.8171, 125.3235, None),
    ("APAC", "China", "Changshu", 31.6538, 120.7522, None),
    ("APAC", "China", "Qingdao", 36.0671, 120.3826, None),
    ("APAC", "China", "Shanghai", 31.2304, 121.4737, None),
    ("APAC", "South Korea", "Jeonju", 35.8242, 127.1480, None),
    ("APAC", "Japan", "Yokohama", 35.4437, 139.6380, None),
]

# Az xlsx 'Karbel' sora (Germany) SZANDEKOSAN nincs a listaban: nincs ilyen
# nevu nemet telepules. Valoszinuleg a 'Korbach' elgepelese -- az mar szerepel
# a listaban --, de lehet 'Karben' is. Visszakerdezve.

HEADER = '''/* neuwerk telephelyek.

   Forras: Website_Countries_Locations_12.08.2026.xlsx (ugyfel, 2026-08-12).
   GENERALT FAJL -- ne ird at kezzel. A forras es a vetites:
   tools/build_locations.py

   x, y: szazalekos pozicio a world.svg rajzteruleten belul. A keplet a
   tools/build_map.py vetitesevel egyezik (equirectangular, 83 fok E es
   60 fok D kozott vagva).

   TODO(client): nyitott kerdesek a szallitott listahoz -- lasd docs/HANDOFF.md
*/
window.NEUWERK_LOCATIONS = ['''


def main():
    rows = []
    for area, country, city, lat, lon, _note in SITES:
        x, y = project(lon, lat)
        rows.append(
            f'  {{ area: "{area}", country: "{country}", city: "{city}", '
            f'x: {x}, y: {y} }},'
        )

    body = HEADER + "\n" + "\n".join(rows) + "\n];\n"
    OUT.write_text(body, encoding="utf-8")

    countries = sorted({s[1] for s in SITES})
    print(f"  {OUT.relative_to(ROOT)}  {len(SITES)} telephely, {len(countries)} orszag")
    print("  orszagok:", ", ".join(countries))
    return 0


if __name__ == "__main__":
    sys.exit(main())
