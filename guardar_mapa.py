"""Paso 7: leer el sitemap y guardar las direcciones en la base de datos local."""

from collections import Counter
from urllib.parse import urlparse

from scraper import abrir_base, guardar_urls, urls_desde_sitemap

SITIO = "viviendoporelmundo.com"
# Se pide ya la dirección final (https y con www) para evitar la redirección.
INDICE = "https://www.viviendoporelmundo.com/sitemap_index.xml"


def corto(mapa: str) -> str:
    return mapa.rsplit("/", 1)[-1]


print("Leyendo el sitemap (3 peticiones, con espera entre cada una)...")
paginas = urls_desde_sitemap(INDICE)
if not paginas:
    raise SystemExit("No se leyó ninguna dirección: no se guarda nada. Revisa la conexión y vuelve a intentar.")

con = abrir_base()
guardadas = guardar_urls(con, paginas, SITIO)
print(f"Direcciones leídas y guardadas: {guardadas}")

print("\n--- LO QUE HAY EN LA BASE ---")
total = con.execute("SELECT COUNT(*) FROM urls WHERE sitio = ?", (SITIO,)).fetchone()[0]
print(f"Filas de {SITIO}: {total}")
for mapa, cuantas in con.execute("SELECT mapa, COUNT(*) FROM urls GROUP BY mapa ORDER BY 2 DESC"):
    print(f"  {cuantas:>4}  {corto(mapa)}")
sin_marcar = con.execute("SELECT COUNT(*) FROM urls WHERE vale_la_pena IS NULL").fetchone()[0]
print(f"Sin marcar todavía (vale_la_pena vacío): {sin_marcar}")

print("\n--- ¿CUÁNTAS USAN CARPETA EN LA DIRECCIÓN? ---")
carpetas = Counter()
for url, mapa in con.execute("SELECT url, mapa FROM urls"):
    partes = [p for p in urlparse(url).path.split("/") if p]
    carpetas[(corto(mapa), partes[0] if len(partes) > 1 else "(raíz)")] += 1
for (mapa, carpeta), cuantas in sorted(carpetas.items()):
    print(f"  {cuantas:>4}  {mapa:<18} {carpeta}")

print("\n--- UN VISTAZO PARA EL PASO 8 (solo mirar, no se marca nada) ---")
palabras = ["colombia", "medellin", "bogota", "cartagena", "cali", "tayrona", "palomino",
            "taganga", "guatape", "cafetero", "san-cipriano"]
condicion = " OR ".join(["url LIKE ?"] * len(palabras))
filas = con.execute(f"SELECT url, mapa FROM urls WHERE {condicion} ORDER BY mapa, url",
                    [f"%{p}%" for p in palabras]).fetchall()
print(f"Direcciones con alguna palabra de Colombia: {len(filas)}")
for url, mapa in filas:
    print(f"  [{corto(mapa)[:4]}] {url.replace('https://www.viviendoporelmundo.com', '')}")

con.close()
