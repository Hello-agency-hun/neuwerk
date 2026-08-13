/* NYITOTT POZICIOK
   ================================================================
   Uj pozicio hozzaadasa: masolj le egy blokkot, es ird at a mezoket.
   A lista sorrendje nem szamit: a career.html munkacsalad szerint
   csoportositva jeleniti meg.

   Mezok:
     title      - a pozicio neve
     jobFamily  - munkacsalad. Ez adja a csoportositast az oldalon.
                  Hasznalt ertekek: Engineering, Manufacturing, Sales,
                  Quality, Supply Chain, Corporate
     location   - varos, orszag
     country    - orszag onmagaban, a szurohoz
     type       - pl. "Full-time", "Part-time", "Internship"
     url        - jelentkezesi link. Ha nincs, hagyd "" erteken.

   A jobFamily es a country mezo azert van kulon, mert az ugyfel altal
   kuldott benchmarkok (Netflix About, Mercedes-Benz Group Careers)
   pontosan e ket tengely menten szervezik a karrieroldalt. Valos adat
   nelkul is igy epul a struktura, hogy az adat megerkezesekor csak a
   lista cserelodjon.

   TODO(client): a valos nyitott poziciok listaja bekerendo -->
*/
window.NEUWERK_JOBS = [
  {
    title: "Placeholder - Development Engineer, Thermal Systems",
    jobFamily: "Engineering",
    location: "Example City, Example Country",
    country: "Example Country",
    type: "Full-time",
    url: "",
    placeholder: true
  },
  {
    title: "Placeholder - Simulation Engineer, Fluid Handling",
    jobFamily: "Engineering",
    location: "Example City, Example Country",
    country: "Example Country",
    type: "Full-time",
    url: "",
    placeholder: true
  },
  {
    title: "Placeholder - Process Engineer, Multi-Material",
    jobFamily: "Manufacturing",
    location: "Example City, Example Country",
    country: "Example Country",
    type: "Full-time",
    url: "",
    placeholder: true
  },
  {
    title: "Placeholder - Key Account Manager",
    jobFamily: "Sales",
    location: "Example City, Example Country",
    country: "Example Country",
    type: "Full-time",
    url: "",
    placeholder: true
  }
];
