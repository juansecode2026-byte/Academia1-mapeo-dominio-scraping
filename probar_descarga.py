"""Paso 5: descargar UNA página (la portada) y ver qué responde el sitio."""

import re

from scraper import espera_del_sitio, pedir

# Se pide con http:// y sin www a propósito: así se ve la redirección que hace el sitio.
URL = "http://viviendoporelmundo.com/"

print(f"Espera antes de pedir: {espera_del_sitio(URL)} segundos...")
r = pedir(URL)
if r is None:
    raise SystemExit("No se pudo descargar la página.")

print("\n--- LA RESPUESTA ---")
print(f"Código de estado:      {r.status_code}")
print(f"Tipo de contenido:     {r.headers.get('Content-Type')}")
print(f"Tamaño del HTML:       {len(r.content):,} bytes")
print(f"Tiempo que tardó:      {r.elapsed.total_seconds():.2f} s")
print(f"Pedimos:               {URL}")
print(f"Terminamos en:         {r.url}")
for salto in r.history:
    print(f"  redirección {salto.status_code}: {salto.url} -> {salto.headers.get('Location')}")

titulo = re.search(r"<title>(.*?)</title>", r.text, re.S)
print(f"\nTítulo de la página:   {titulo.group(1).strip() if titulo else '(no encontrado)'}")
print(f"Enlaces <a href> que trae el HTML: {len(re.findall(r'<a [^>]*href=', r.text))}")

print("\n--- LOS PRIMEROS 500 CARACTERES DEL HTML CRUDO ---")
print(r.text[:500])
