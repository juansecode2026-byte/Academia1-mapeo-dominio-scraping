"""Paso 3: preguntarle al robots.txt de viviendoporelmundo.com qué podemos hacer."""

from scraper import USER_AGENT, _robots, espera_del_sitio, puede_visitar

SITIO = "https://www.viviendoporelmundo.com"

rutas = [
    "/",
    "/un-articulo/",
    "/wp-admin/",
    "/wp-admin/login.php",
    "/wp-includes/js/jquery.js",
    "/wp-content/uploads/2025/foto.jpg",
    "/wp-content/plugins/algo/",
    "/xmlrpc.php",
    "/readme.html",
]

print(f"Nuestro nombre (User-agent): {USER_AGENT}\n")

print("¿Puedo visitar esta ruta?")
for ruta in rutas:
    resultado = puede_visitar(SITIO + ruta)
    print(f"  {'SÍ' if resultado else 'NO':<3} {ruta}")

print(f"\n¿Cuántos segundos esperar entre páginas? {espera_del_sitio(SITIO)}")
print(f"¿Dónde está el mapa del sitio? {_robots(SITIO).site_maps()}")
