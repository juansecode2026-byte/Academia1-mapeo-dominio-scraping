"""Paso 8: marcar las direcciones guardadas con reglas fijas (opciones A, B, C y D).

No hace peticiones al sitio: trabaja solo sobre datos/scraping.db.
Solo pisa marcas puestas por reglas (motivo que empieza por «regla:»); las marcas manuales se respetan.
"""

from collections import Counter
from urllib.parse import urlparse

from scraper import abrir_base

SITIO = "viviendoporelmundo.com"

# B. Lugares que cuentan como Colombia (se buscan como palabras sueltas del nombre de la dirección)
LUGARES_COLOMBIA = {
    "colombia", "colombiano", "colombiana", "medellin", "bogota", "cartagena", "cali",
    "tayrona", "palomino", "taganga", "guatape", "cafetero", "cipriano",
}

# C. Familias que no son información tipo blog, según pistas en el nombre
FAMILIAS = [
    ("vídeo o fotomontaje", ("video", "fotomontaje")),
    ("podcast", ("podcast",)),
    ("entrevista", ("entrevista",)),
    ("venta o afiliación", ("seguro", "hosting", "siteground", "curso", "afiliado", "afiliados",
                            "monetiza", "descuento", "criptomonedas", "ingresos", "regalos")),
]


def clasificar(url: str, mapa: str) -> tuple[int, str]:
    """Devuelve (vale_la_pena, motivo) para una dirección, aplicando las reglas en orden."""
    partes = [p for p in urlparse(url).path.split("/") if p]
    carpeta = partes[0] if len(partes) > 1 else ""
    slug = partes[-1] if partes else ""
    palabras = set(slug.split("-"))

    # A + D. Las páginas fijas no son artículos, salvo las guías por país
    if mapa.endswith("page-sitemap.xml") and carpeta != "paises":
        return 0, "regla: página fija, no es un artículo"

    # C. Familias que no son información tipo blog
    for familia, pistas in FAMILIAS:
        if palabras & set(pistas):
            return 0, f"regla: {familia}"
    if slug.endswith("-2"):
        return 0, "regla: posible duplicado (termina en -2)"

    # B. Tema: Colombia
    encontradas = sorted(palabras & LUGARES_COLOMBIA)
    if encontradas:
        tipo = "guía por país" if carpeta == "paises" else "entrada"
        return 1, f"regla: Colombia ({', '.join(encontradas)}) · {tipo}"
    return 0, "regla: otro tema (no nombra Colombia en la dirección)"


con = abrir_base()
filas = con.execute(
    "SELECT url, mapa FROM urls WHERE sitio = ? AND (motivo IS NULL OR motivo LIKE 'regla:%')", (SITIO,)
).fetchall()
marcas = [(*clasificar(url, mapa), url) for url, mapa in filas]
con.executemany("UPDATE urls SET vale_la_pena = ?, motivo = ? WHERE url = ?", marcas)
con.commit()
print(f"Direcciones marcadas por reglas: {len(marcas)}")

print("\n--- RESUMEN ---")
for vale, cuantas in con.execute("SELECT vale_la_pena, COUNT(*) FROM urls WHERE sitio = ? GROUP BY 1 ORDER BY 1 DESC", (SITIO,)):
    print(f"  {'SÍ' if vale == 1 else 'NO' if vale == 0 else 'sin decidir'}: {cuantas}")

print("\n--- POR MOTIVO ---")
motivos = Counter(m.split(" (")[0] if m.startswith("regla: Colombia") else m
                  for (m,) in con.execute("SELECT motivo FROM urls WHERE sitio = ?", (SITIO,)))
for motivo, cuantas in motivos.most_common():
    print(f"  {cuantas:>4}  {motivo}")

print("\n--- LAS QUE VALEN LA PENA (SÍ) ---")
for url, motivo in con.execute("SELECT url, motivo FROM urls WHERE vale_la_pena = 1 ORDER BY url"):
    print(f"  {urlparse(url).path:<60} {motivo}")

print("\n--- PARA REVISAR: DONDE LAS REGLAS PUEDEN EQUIVOCARSE ---")
print("Descartadas por terminar en -2:")
for (url,) in con.execute("SELECT url FROM urls WHERE motivo LIKE '%duplicado%' ORDER BY url"):
    print("  ", urlparse(url).path)
print("Descartadas por venta o afiliación:")
for (url,) in con.execute("SELECT url FROM urls WHERE motivo LIKE '%venta%' ORDER BY url"):
    print("  ", urlparse(url).path)
print("Descartadas por ser de Colombia pero de otra familia:")
for url, motivo in con.execute("SELECT url, motivo FROM urls WHERE vale_la_pena = 0 ORDER BY url"):
    partes = [p for p in urlparse(url).path.split("/") if p]
    palabras = set(partes[-1].split("-")) if partes else set()   # la portada no tiene nombre
    if palabras & LUGARES_COLOMBIA:
        print(f"   {urlparse(url).path}  ->  {motivo}")

con.close()
