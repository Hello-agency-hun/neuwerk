/* A neuwerk jelenlét 16 országa.

   ================================================================
   FIGYELEM — EZ NEM VALÓS ADAT.
   Az országok listáját sem a tartalmi spec, sem a brandbook nem
   tartalmazza. Az alábbi 16 tétel PLACEHOLDER: csak azért van itt,
   hogy a térkép működését és a hover-viselkedést be lehessen mutatni.
   A `placeholder: true` mező miatt a tooltip is jelöli.

   TODO(client): a 16 ország tényleges listája bekérendő -->
   ================================================================

   x, y: százalékos pozíció a world.svg viewBoxán belül (150 x 60 rács,
   equirectangular, 83°É és 60°D között vágva).
*/
window.NEUWERK_LOCATIONS = [
  { name: "Germany",        x: 50.6, y: 30.5, placeholder: true },
  { name: "Czech Republic", x: 52.3, y: 32.0, placeholder: true },
  { name: "Slovakia",       x: 53.4, y: 32.8, placeholder: true },
  { name: "Hungary",        x: 53.2, y: 34.2, placeholder: true },
  { name: "Romania",        x: 55.3, y: 34.6, placeholder: true },
  { name: "Italy",          x: 50.9, y: 36.4, placeholder: true },
  { name: "Spain",          x: 46.6, y: 37.8, placeholder: true },
  { name: "Portugal",       x: 45.0, y: 38.2, placeholder: true },
  { name: "Türkiye",        x: 57.6, y: 37.6, placeholder: true },
  { name: "United States",  x: 24.5, y: 33.5, placeholder: true },
  { name: "Mexico",         x: 21.8, y: 42.5, placeholder: true },
  { name: "Brazil",         x: 32.4, y: 58.0, placeholder: true },
  { name: "China",          x: 76.8, y: 35.5, placeholder: true },
  { name: "India",          x: 69.4, y: 43.0, placeholder: true },
  { name: "Japan",          x: 84.2, y: 34.0, placeholder: true },
  { name: "South Africa",   x: 55.4, y: 61.0, placeholder: true }
];
