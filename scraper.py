"""Funciones del scraper manual (guía 1). Se va completando paso a paso."""

import time
from functools import lru_cache
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

# Identifícate con honestidad: nombre del bot y un correo de contacto.
USER_AGENT = "MiBotInvestigacion/1.0 (contacto: juansecode2026@gmail.com)"


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


HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.5",
}


def pedir(url: str, espera: float | None = None) -> requests.Response | None:
    """Pide una URL y devuelve la respuesta completa, o None si no se puede o no se debe."""
    if not puede_visitar(url):
        print(f"El robots.txt no permite visitar {url}")
        return None
    time.sleep(espera_del_sitio(url) if espera is None else espera)   # no saturar el servidor
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()                # lanza error si el código es 4xx o 5xx
    except requests.RequestException as e:
        print(f"No se pudo descargar {url}: {e}")
        return None
    return r


def descargar(url: str, espera: float | None = None, solo_html: bool = True) -> str | None:
    """Devuelve el contenido de la URL como texto, o None si algo falla."""
    r = pedir(url, espera)
    if r is None:
        return None
    if solo_html and "text/html" not in r.headers.get("Content-Type", ""):
        return None                         # ignora PDFs, imágenes, etc.
    if r.encoding in (None, "ISO-8859-1"):
        r.encoding = r.apparent_encoding    # arregla tildes y eñes mal leídas
    return r.text
