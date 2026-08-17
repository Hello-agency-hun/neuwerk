/* neuwerk telephelyek.

   Forras: Website_Countries_Locations_12.08.2026.xlsx (ugyfel, 2026-08-12).
   GENERALT FAJL -- ne ird at kezzel. A forras es a vetites:
   tools/build_locations.py

   x, y: szazalekos pozicio a world.svg rajzteruleten belul. A keplet a
   tools/build_map.py vetitesevel egyezik (equirectangular, 83 fok E es
   60 fok D kozott vagva).

   TODO(client): nyitott kerdesek a szallitott listahoz -- lasd docs/HANDOFF.md
*/
window.NEUWERK_LOCATIONS = [
  { area: "Americas", country: "USA", city: "Auburn Hills", x: 27.21, y: 29.02 },
  { area: "Americas", country: "USA", city: "Sun Prairie", x: 25.55, y: 28.68 },
  { area: "Americas", country: "USA", city: "Rochester Hills", x: 27.24, y: 29.04 },
  { area: "Americas", country: "USA", city: "Somersworth", x: 30.65, y: 28.62 },
  { area: "Americas", country: "Mexico", city: "Delicias", x: 21.04, y: 39.16 },
  { area: "Americas", country: "Mexico", city: "Monterrey", x: 22.47, y: 40.91 },
  { area: "Americas", country: "Mexico", city: "Montemorelos", x: 22.6, y: 41.26 },
  { area: "Americas", country: "Mexico", city: "San Luis Potosí", x: 22.28, y: 43.38 },
  { area: "Americas", country: "Mexico", city: "Tlalnepantla", x: 22.78, y: 45.21 },
  { area: "Americas", country: "Brazil", city: "Ponta Grossa", x: 36.4, y: 76.42 },
  { area: "EMEA West", country: "Germany", city: "Hann. Münden", x: 53.01, y: 22.92 },
  { area: "EMEA West", country: "Germany", city: "Waltershausen", x: 53.27, y: 23.28 },
  { area: "EMEA West", country: "Germany", city: "Hamburg", x: 53.11, y: 21.43 },
  { area: "EMEA West", country: "Germany", city: "Korbach", x: 52.8, y: 23.02 },
  { area: "EMEA West", country: "Germany", city: "Hannover", x: 53.04, y: 22.25 },
  { area: "EMEA West", country: "France", city: "Caluire-et-Cuire", x: 51.68, y: 26.85 },
  { area: "EMEA West", country: "France", city: "Andrézieux-Bouthéon", x: 51.52, y: 27.04 },
  { area: "EMEA West", country: "France", city: "Rennes", x: 49.87, y: 25.23 },
  { area: "EMEA West", country: "Austria", city: "Vienna", x: 54.88, y: 25.16 },
  { area: "EMEA West", country: "Morocco", city: "Tangier", x: 48.71, y: 33.87 },
  { area: "EMEA West", country: "Netherlands", city: "Maastricht", x: 51.91, y: 23.31 },
  { area: "EMEA West", country: "Portugal", city: "Porto", x: 47.94, y: 30.09 },
  { area: "EMEA East", country: "Hungary", city: "Makó", x: 56.02, y: 26.56 },
  { area: "EMEA East", country: "Hungary", city: "Vác", x: 55.65, y: 25.47 },
  { area: "EMEA East", country: "Romania", city: "Carei", x: 56.57, y: 25.53 },
  { area: "EMEA East", country: "Romania", city: "Timișoara", x: 56.22, y: 26.88 },
  { area: "EMEA East", country: "Slovenia", city: "Kranj", x: 54.32, y: 26.54 },
  { area: "EMEA East", country: "Slovakia", city: "Dolné Vestenice", x: 55.45, y: 24.8 },
  { area: "EMEA East", country: "Serbia", city: "Subotica", x: 55.8, y: 26.64 },
  { area: "EMEA East", country: "Czech Republic", city: "Ostrava", x: 55.41, y: 24.04 },
  { area: "APAC", country: "China", city: "Changchun", x: 85.15, y: 28.23 },
  { area: "APAC", country: "China", city: "Changshu", x: 83.88, y: 36.74 },
  { area: "APAC", country: "China", city: "Qingdao", x: 83.77, y: 33.65 },
  { area: "APAC", country: "China", city: "Shanghai", x: 84.08, y: 37.04 },
  { area: "APAC", country: "South Korea", city: "Jeonju", x: 85.65, y: 33.82 },
  { area: "APAC", country: "Japan", city: "Yokohama", x: 89.12, y: 34.09 },
];
