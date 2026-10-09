"""Funciones del scraper manual (guía 1). Se va completando paso a paso."""

from functools import lru_cache
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

# Identifícate con honestidad: nombre del bot y un correo de contacto.
# Cambia el correo de ejemplo por uno tuyo antes de descargar páginas (paso 5).
USER_AGENT = "MiBotInvestigacion/1.0 (contacto: tu-correo@dominio.com)"


def _normalizar(texto: str) -> list[str]:
    """Quita las líneas en blanco que parten un bloque en dos.

    El lector de Python da por terminado un bloque cuando ve una línea en blanco y
    descarta las reglas que vienen después. En el robots.txt de viviendoporelmundo.com
    hay una en blanco tras `Crawl-delay`, y eso hacía que se perdieran tres rutas
    prohibidas. Aquí solo se conserva una línea en blanco si lo que sigue es un
    nuevo `User-agent`.
    """
    lineas = [linea.strip() for linea in texto.splitlines()]
    resultado = []
    for i, linea in enumerate(lineas):
        if linea:
            resultado.append(linea)
        else:
            siguiente = next((x for x in lineas[i + 1:] if x), "")
            if siguiente.lower().startswith("user-agent"):
                resultado.append("")
    return resultado


@lru_cache(maxsize=None)
def _robots(base: str) -> RobotFileParser:
    """Descarga y lee el robots.txt de un sitio. lru_cache lo hace una sola vez por sitio."""
    rp = RobotFileParser()
    r = requests.get(f"{base}/robots.txt", headers={"User-Agent": USER_AGENT}, timeout=20)
    if r.status_code in (401, 403):
        rp.disallow_all = True      # nos cierran la puerta: no entramos a nada
    elif r.status_code >= 400:
        rp.allow_all = True         # no hay robots.txt (404): no prohíbe nada
    else:
        rp.parse(_normalizar(r.text))
    return rp


def puede_visitar(url: str) -> bool:
    """True si el robots.txt del sitio permite a nuestro bot visitar esa URL."""
    p = urlparse(url)
    return _robots(f"{p.scheme}://{p.netloc}").can_fetch(USER_AGENT, url)


def espera_del_sitio(url: str, por_defecto: float = 2.0) -> float:
    """Lee el Crawl-delay del robots.txt; si el sitio no lo indica, usa el valor por defecto."""
    p = urlparse(url)
    retraso = _robots(f"{p.scheme}://{p.netloc}").crawl_delay(USER_AGENT)
    return float(retraso) if retraso else por_defecto
