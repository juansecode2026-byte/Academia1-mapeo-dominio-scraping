"""Funciones del scraper manual (guía 1). Se va completando paso a paso."""

import sqlite3
import time
import xml.etree.ElementTree as ET
from datetime import date
from functools import lru_cache
from pathlib import Path
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
    try:
        robots = _robots(f"{p.scheme}://{p.netloc}")
    except requests.RequestException as e:
        print(f"No se pudo leer el robots.txt de {p.netloc}: {e}")
        return False                        # sin poder comprobar el permiso, no se entra
    return robots.can_fetch(USER_AGENT, url)


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


NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def leer_sitemap(sitemap_url: str) -> tuple[list[dict], list[dict]]:
    """Lee un archivo de sitemap y devuelve (mapas, paginas).

    Si es un índice, `mapas` trae los mapas hijos y `paginas` va vacía; si es un mapa
    de páginas, pasa al revés. Cada elemento lleva su dirección (`url`), su fecha de
    última modificación (`lastmod`) y el mapa del que salió (`mapa`).
    """
    contenido = descargar(sitemap_url, solo_html=False)
    if not contenido:
        return [], []
    raiz = ET.fromstring(contenido.encode("utf-8"))

    def leer(etiqueta: str) -> list[dict]:
        return [
            {
                "url": e.findtext("sm:loc", "", NS).strip(),
                "lastmod": e.findtext("sm:lastmod", "", NS).strip(),
                "mapa": sitemap_url,
            }
            for e in raiz.findall(f"sm:{etiqueta}", NS)
        ]

    return leer("sitemap"), leer("url")


def urls_desde_sitemap(sitemap_url: str, limite: int = 500) -> list[dict]:
    """Recorre un sitemap (con sus mapas hijos, si es un índice) y devuelve las páginas.

    `limite` es el tope de páginas: protege contra sitios con miles de direcciones.
    """
    mapas, paginas = leer_sitemap(sitemap_url)
    for mapa in mapas:
        if len(paginas) >= limite:
            break
        paginas += urls_desde_sitemap(mapa["url"], limite - len(paginas))
    return paginas[:limite]


RUTA_BASE = Path(__file__).parent / "datos" / "scraping.db"


def abrir_base() -> sqlite3.Connection:
    """Abre la base de datos local del proyecto; si no existe, la crea con su tabla `urls`."""
    RUTA_BASE.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(RUTA_BASE)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            url          TEXT PRIMARY KEY,
            sitio        TEXT NOT NULL,
            origen       TEXT NOT NULL,
            mapa         TEXT,
            lastmod      TEXT,
            vale_la_pena INTEGER,
            motivo       TEXT,
            fecha_mapeo  TEXT NOT NULL
        )
        """
    )
    return con


def guardar_urls(con: sqlite3.Connection, paginas: list[dict], sitio: str, origen: str = "sitemap") -> int:
    """Guarda las direcciones sin duplicarlas. Si ya existían, actualiza su mapa y su fecha,
    pero no toca `vale_la_pena` ni `motivo`, que se rellenan en el paso del filtrado."""
    hoy = date.today().isoformat()
    con.executemany(
        """
        INSERT INTO urls (url, sitio, origen, mapa, lastmod, fecha_mapeo)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            mapa = excluded.mapa,
            lastmod = excluded.lastmod,
            fecha_mapeo = excluded.fecha_mapeo
        """,
        [(p["url"], sitio, origen, p["mapa"], p["lastmod"], hoy) for p in paginas],
    )
    con.commit()
    return len(paginas)
