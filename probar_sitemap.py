"""Paso 6: leer el índice del sitemap y sus mapas hijos con código."""

import time
from collections import Counter

from scraper import leer_sitemap

# Se pide ya la dirección final (https y con www) para evitar la redirección.
INDICE = "https://www.viviendoporelmundo.com/sitemap_index.xml"
inicio = time.time()

print("--- 1. EL ÍNDICE ---")
mapas, sueltas = leer_sitemap(INDICE)
print(f"Mapas hijos: {len(mapas)}   Páginas sueltas en el índice: {len(sueltas)}")
for m in mapas:
    print(f"  {m['url']}   (última modificación: {m['lastmod']})")

todas = []
for m in mapas:
    print(f"\n--- 2. EL MAPA {m['url']} ---")
    _, paginas = leer_sitemap(m["url"])
    print(f"Direcciones en este mapa: {len(paginas)}")
    todas += paginas

print("\n--- 3. EL RESULTADO ---")
urls = [p["url"] for p in todas]
print(f"Total de direcciones:     {len(urls)}")
print(f"Direcciones distintas:    {len(set(urls))}")
for mapa, cuantas in Counter(p["mapa"] for p in todas).items():
    print(f"  {cuantas:>4}  {mapa}")

fechas = sorted(p["lastmod"] for p in todas if p["lastmod"])
if fechas:
    print(f"Modificación más antigua: {fechas[0]}")
    print(f"Modificación más reciente: {fechas[-1]}")
print("Por año de modificación:")
for anio, cuantas in sorted(Counter(f[:4] for f in fechas).items()):
    print(f"  {anio}: {cuantas}")

print("\nLas 5 primeras:")
for u in urls[:5]:
    print("  ", u)
print("Las 5 últimas:")
for u in urls[-5:]:
    print("  ", u)

print(f"\nPeticiones al sitio: {1 + len(mapas)} (más el robots.txt)")
print(f"Tiempo total: {time.time() - inicio:.0f} s")
