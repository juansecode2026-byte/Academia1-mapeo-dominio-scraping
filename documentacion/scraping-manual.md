Guía 1 de 2 8 de octubre de 2026 Python Nivel: principiante · v5 con ejercicio

> Fuente original: `scraping-manual_2026-10-08_v5.html` (respaldo, no leer). Esta guía tiene dos partes: la guía de 7 pasos con código y, al final, el **Ejercicio práctico** sobre viviendoporelmundo.com.

# Scraping manual

Vas a descargar una página web, quedarte solo con el texto del artículo (sin menús ni publicidad) y guardarlo ordenado. Escribes cada paso tú mismo para entender qué pasa por dentro. En la guía 2 le entregas ese trabajo a agentes de IA.

### Lo que descarga tu código (HTML crudo)
```
<nav>Inicio | Blog | Contacto</nav>
<div class="ad">¡Suscríbete ya!</div>
<article>
  <h1>Cómo la IA reduce costos</h1>
  <p>Las empresas que automatizan...</p>
</article>
<footer>© 2026 · Cookies</footer>
```

### Lo que te queda (texto limpio)  **Cómo la IA reduce costos** Las empresas que automatizan...

## La idea general

Hacer scraping es automatizar lo que haría una persona: abrir una página, leerla y copiar lo importante. La diferencia es que tu programa lo hace en segundos y para cientos de páginas. El proceso siempre sigue la misma cadena:

1. **Permiso** Revisas robots.txt y los términos del sitio.código
1. **Descarga** Pides la página y recibes HTML.código
1. **Estructura** Entiendes cómo está armado ese HTML.tú
1. **Extracción** Separas el artículo del ruido.código
1. **Mapa** Descubres qué otras páginas existen.código
1. **Guardado** Almacenas título, fecha, texto y fuente.código
1. **Reescritura** Escribes con tus palabras y citas.tú

>  **Por qué empezar manual**

Cuando un agente falle (y va a fallar a veces), necesitas saber en qué eslabón de la cadena está el problema. Quien entendió el proceso a mano depura en minutos; quien solo usó la herramienta queda a ciegas. Además, lo que aprendes aquí es lo que después conviertes en las herramientas del agente.

## Qué información puedes obtener

De una sola página de artículo salen estos datos. Algunos vienen de la etiqueta del HTML, otros de los metadatos que el sitio publica para Google y redes sociales.

| Dato | De dónde sale | Para qué te sirve |
|---|---|---|
| Título | `<h1>` o `og:title` | Identificar y citar la fuente |
| Texto del artículo | `<article>`, `<p>` | Materia prima para resumir y analizar |
| Autor | Metadatos o firma del artículo | Citar correctamente |
| Fecha de publicación | `article:published_time` | Saber si la información está vigente |
| Descripción | `meta description` | Resumen rápido para decidir si vale la pena |
| Enlaces internos | `<a href>` | Descubrir más páginas del dominio |
| Lista de URLs del sitio | `sitemap.xml` | Mapear todo el dominio sin recorrerlo a ciegas |

## Antes de empezar: reglas del juego

El scraping es legal en muchos contextos, pero no todo vale. Estas cinco reglas te mantienen del lado correcto y evitan que te bloqueen.

- **Lee robots.txt.** Es el archivo donde el sitio dice qué partes no quiere que automatices (`sitio.com/robots.txt`). Si una ruta está prohibida, no la visitas.
- **Lee los términos de uso.** Algunos sitios prohíben el scraping aunque robots.txt no lo diga. Si lo prohíben, busca una API oficial o pide permiso.
- **Nada detrás de login o paywall.** Si hay que iniciar sesión o pagar para verlo, no lo extraes.
- **Ve despacio.** Espera 2 a 3 segundos entre páginas. Un servidor pequeño puede caerse con ráfagas de peticiones.
- **Reescribe y cita.** Usa la información como insumo. Escríbela con tus palabras y nombra la fuente con su enlace. No copies el texto.

>  **Para practicar sin riesgo**

Existen sitios hechos para aprender scraping: `quotes.toscrape.com` y `books.toscrape.com`. Haz todos los ejercicios de esta guía ahí primero y luego pasas a sitios reales.

## Herramientas que necesitas

| Herramienta | Qué hace | Analogía |
|---|---|---|
| Python 3.10 o superior | El lenguaje donde escribes todo | La cocina |
| `requests` | Descarga páginas por HTTP | El mensajero que trae el paquete |
| `beautifulsoup4` + `lxml` | Lee el HTML y te deja buscar etiquetas | Abrir el paquete y mirar lo que hay |
| `trafilatura` | Deja solo el texto principal del artículo | Quedarte con la carne y tirar el empaque |
| DevTools del navegador (F12) | Te muestra el HTML de cualquier página | Rayos X de la página |
| `playwright` (opcional) | Abre un navegador real para páginas que cargan con JavaScript | Un robot que usa Chrome por ti |
| VS Code | Editor donde escribes y corres el código | La mesa de trabajo |

### Preparar el proyecto

Crea una carpeta y un entorno virtual (una "burbuja" para que las librerías de este proyecto no se mezclen con las de otros):

**terminal**

```
mkdir scraping-manual && cd scraping-manual
python3 -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install requests beautifulsoup4 lxml trafilatura
```

Crea un archivo vacío llamado `scraper.py`. En los siguientes pasos le vas agregando funciones, una por cada eslabón de la cadena.

## 1. Revisar robots.txt desde el código

Python trae una herramienta que lee robots.txt y te responde sí o no para cada URL.

**scraper.py (parte 1)**

```
from functools import lru_cache
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

# Identifícate con honestidad: nombre del bot y un correo de contacto.
USER_AGENT = "MiBotInvestigacion/1.0 (contacto: tu-correo@dominio.com)"

@lru_cache(maxsize=None)
def _robots(base: str) -> RobotFileParser:
    rp = RobotFileParser()
    rp.set_url(f"{base}/robots.txt")
    rp.read()
    return rp

def puede_visitar(url: str) -> bool:
    p = urlparse(url)
    return _robots(f"{p.scheme}://{p.netloc}").can_fetch(USER_AGENT, url)

# Prueba rápida
if __name__ == "__main__":
    print(puede_visitar("https://quotes.toscrape.com/"))
```

>  **Por qué lo hacemos así**

Así el permiso queda dentro del código y no depende de que te acuerdes de revisarlo. `lru_cache` evita volver a descargar robots.txt en cada página del mismo sitio.

>  **Qué obtienes**

`True` si puedes visitar esa URL y `False` si el sitio lo prohíbe. Si da `False`, te detienes.

## 2. Descargar el HTML

Ahora pides la página. Tu código se presenta con un `User-Agent`, espera un poco antes de pedir y maneja los errores comunes.

**scraper.py (parte 2)**

```
import time
import requests

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.5",
}

def descargar(url: str, espera: float = 2.0, solo_html: bool = True) -> str | None:
    """Devuelve el contenido de la URL como texto, o None si algo falla."""
    time.sleep(espera)                      # buena educación: no saturar el servidor
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()                # lanza error si el código es 4xx o 5xx
    except requests.RequestException as e:
        print(f"No se pudo descargar {url}: {e}")
        return None
    if solo_html and "text/html" not in r.headers.get("Content-Type", ""):
        return None                         # ignora PDFs, imágenes, etc.
    if r.encoding in (None, "ISO-8859-1"):
        r.encoding = r.apparent_encoding    # arregla tildes y eñes mal leídas
    return r.text
```

>  **Qué obtienes**

Un texto largo con todo el HTML de la página. Es el "paquete cerrado": todavía contiene menús, scripts, publicidad y pie de página mezclados con el artículo.

## 3. Leer la estructura del HTML

Antes de extraer nada, mira cómo está armada la página. En tu navegador abre un artículo, haz clic derecho sobre el título y elige **Inspeccionar** . Verás algo así:

**HTML de ejemplo**

```
<html>
  <head>
    <title>Cómo la IA reduce costos | Sitio</title>
    <meta name="description" content="Resumen del artículo">
    <meta property="article:published_time" content="2026-09-30">
  </head>
  <body>
    <nav>...</nav>
    <article>
      <h1>Cómo la IA reduce costos</h1>
      <p class="autor">Por Ana Pérez</p>
      <p>Las empresas que automatizan...</p>
    </article>
    <footer>...</footer>
  </body>
</html>
```

La lógica: el HTML es un árbol de etiquetas. El artículo casi siempre vive dentro de `<article>` o de un contenedor con una clase reconocible. Con BeautifulSoup le dices "dame todos los `<p>` que estén dentro de `<article>`".

**scraper.py (parte 3)**

```
from bs4 import BeautifulSoup

def leer_metadatos(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    def meta(**attrs):
        tag = soup.find("meta", attrs=attrs)
        return tag["content"].strip() if tag and tag.get("content") else None

    h1 = soup.find("h1")
    return {
        "titulo": h1.get_text(strip=True) if h1 else (soup.title.string.strip() if soup.title else None),
        "descripcion": meta(name="description"),
        "fecha": meta(property="article:published_time"),
        "autor": meta(name="author"),
        "parrafos": [p.get_text(" ", strip=True) for p in soup.select("article p")],
        "enlaces": [a["href"] for a in soup.find_all("a", href=True)],
    }
```

>  **Por qué este método tiene límite**

Los selectores como `article p` funcionan en un sitio, pero cada sitio arma su HTML distinto. Si tienes que escribir uno por cada página que visites, no escala. Por eso el paso 4 usa una librería que adivina dónde está el texto principal.

## 4. Extraer solo el texto del artículo

`trafilatura` analiza la página y descarta menús, publicidad, comentarios y pie de página. Además intenta rescatar título, autor y fecha.

**scraper.py (parte 4)**

```
import json
import trafilatura

def extraer_articulo(html: str, url: str) -> dict | None:
    resultado = trafilatura.extract(
        html,
        url=url,
        output_format="json",
        with_metadata=True,
        include_comments=False,
        include_tables=False,
        favor_precision=True,     # prefiere perder algo de texto antes que traer ruido
    )
    if not resultado:
        return None               # la página no parece un artículo
    d = json.loads(resultado)
    return {
        "url": url,
        "titulo": d.get("title"),
        "autor": d.get("author"),
        "fecha_publicacion": d.get("date"),
        "sitio": d.get("hostname"),
        "descripcion": d.get("description"),
        "texto": d.get("text"),
    }
```

>  **Qué obtienes**

Un diccionario con el texto limpio, listo para leer o para entregárselo a un modelo de IA. Ejemplo de resultado:

**resultado de ejemplo**

```
{
  "url": "https://sitio-ejemplo.com/blog/ia-reduce-costos",
  "titulo": "Cómo la IA reduce costos",
  "autor": "Ana Pérez",
  "fecha_publicacion": "2026-09-30",
  "sitio": "sitio-ejemplo.com",
  "texto": "Las empresas que automatizan sus procesos..."
}
```

## 5. Mapear el dominio: descubrir qué páginas existen

Hasta ahora trabajaste con una URL que ya conocías. Para un sitio completo necesitas una lista de páginas. Hay dos formas, y son justo lo que herramientas como Firecrawl llaman **map** y **crawl** .

### Forma A. Leer el sitemap.xml (rápida y limpia)

Muchos sitios publican un archivo con todas sus URLs, normalmente en `sitio.com/sitemap.xml`. También suele estar mencionado dentro de robots.txt.

**scraper.py (parte 5A)**

```
import xml.etree.ElementTree as ET

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

def urls_desde_sitemap(sitemap_url: str, limite: int = 500) -> list[str]:
    contenido = descargar(sitemap_url, solo_html=False)
    if not contenido:
        return []
    raiz = ET.fromstring(contenido.encode("utf-8"))
    urls: list[str] = []
    # Un sitemap puede ser un índice que apunta a otros sitemaps
    for loc in raiz.findall(".//sm:sitemap/sm:loc", NS):
        urls += urls_desde_sitemap(loc.text.strip(), limite)
        if len(urls) >= limite:
            break
    for loc in raiz.findall(".//sm:url/sm:loc", NS):
        urls.append(loc.text.strip())
    return urls[:limite]
```

### Forma B. Seguir los enlaces (crawl propio)

Si no hay sitemap, empiezas en la portada y sigues los enlaces internos, como haría una persona. Siempre con un tope de páginas.

**scraper.py (parte 5B)**

```
from collections import deque
from urllib.parse import urljoin, urldefrag

def rastrear(inicio: str, max_paginas: int = 30) -> list[str]:
    dominio = urlparse(inicio).netloc
    pendientes, vistas, encontradas = deque([inicio]), set(), []
    while pendientes and len(vistas) < max_paginas:
        url = pendientes.popleft()
        if url in vistas or not puede_visitar(url):
            continue
        vistas.add(url)
        html = descargar(url)
        if not html:
            continue
        encontradas.append(url)
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            enlace = urldefrag(urljoin(url, a["href"]))[0]   # quita el #ancla
            if urlparse(enlace).netloc == dominio and enlace not in vistas:
                pendientes.append(enlace)
    return encontradas
```

### Decidir cuáles páginas valen la pena

Un sitio tiene páginas de contacto, políticas, etiquetas y categorías que no te sirven. En modo manual filtras con reglas que tú escribes:

**scraper.py (parte 5C)**

```
PATRONES_UTILES = ("/blog/", "/noticias/", "/articulo/")
PATRONES_RUIDO = ("/tag/", "/categoria/", "/autor/", "/contacto", "/politica")

def vale_la_pena(url: str) -> bool:
    if any(p in url for p in PATRONES_RUIDO):
        return False
    return any(p in url for p in PATRONES_UTILES)
```

>  **Por qué esto es el punto débil del modo manual**

Las reglas son rígidas: solo ven la forma de la URL, no el contenido. Una página llamada `/blog/novedades-2026` puede ser pura propaganda y otra en `/recursos/` puede ser justo lo que buscas. Un agente de IA puede leer el título y decidir con criterio. Eso lo construimos en la guía 2.

## 6. Guardar los datos

Guarda cada artículo con sus metadatos y la fecha en que lo consultaste. JSON conserva todo el texto; CSV te sirve para abrirlo en Excel.

**scraper.py (parte 6)**

```
import csv
from datetime import date

def guardar(fichas: list[dict], ruta_base: str = "resultados") -> None:
    hoy = date.today().isoformat()
    for f in fichas:
        f.setdefault("fecha_consulta", hoy)
    with open(f"{ruta_base}.json", "w", encoding="utf-8") as fh:
        json.dump(fichas, fh, ensure_ascii=False, indent=2)
    columnas = ["url", "titulo", "autor", "fecha_publicacion", "sitio", "fecha_consulta", "cita"]
    with open(f"{ruta_base}.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        w.writerows(fichas)
```

>  **Qué obtienes**

Dos archivos: `resultados.json` con el texto completo y `resultados.csv` con un índice para revisar rápido. Usamos `utf-8-sig` para que Excel muestre bien las tildes.

## 7. Reescribir con tus palabras y citar

Este paso no lo hace el código: lo haces tú. El texto que descargaste es insumo de trabajo, no el producto final. Lo que publiques o entregues a un cliente debe ser tu análisis, escrito con tus palabras, con la fuente claramente indicada.

### No hacer Copiar párrafos del artículo, cambiar dos palabras y publicarlos sin mencionar de dónde salieron.

### Hacer Entender la idea, explicarla con tu estructura y tu lenguaje, y cerrar con la referencia a la fuente.

Una ficha de cita sencilla, que puedes generar con el código usando los datos que ya guardaste:

**scraper.py (parte 7)**

```
def referencia(f: dict) -> str:
    autor = f.get("autor") or "Autor no indicado"
    fecha = f.get("fecha_publicacion") or "s. f."
    return f'{autor}. "{f["titulo"]}". {f["sitio"]}, {fecha}. {f["url"]} (consultado el {f["fecha_consulta"]})'
```

Resultado: `Ana Pérez. "Cómo la IA reduce costos". sitio-ejemplo.com, 2026-09-30. https://sitio-ejemplo.com/blog/ia-reduce-costos (consultado el 2026-10-08)`

## Unir todo en un script

Con las funciones anteriores en `scraper.py`, agrega esta función al final. Recorre el sitio, filtra, descarga, extrae y guarda.

**scraper.py (parte final)**

```
def main(sitio: str = "https://quotes.toscrape.com/", max_articulos: int = 10) -> None:
    # 1. Mapa: primero sitemap, y si no hay, rastreo por enlaces
    urls = urls_desde_sitemap(f"{sitio.rstrip('/')}/sitemap.xml") or rastrear(sitio, max_paginas=30)
    # 2. Filtro de páginas útiles (en el sitio de práctica no hay /blog/, así que tomamos todas)
    candidatas = [u for u in urls if vale_la_pena(u)] or urls
    fichas = []
    for url in candidatas[:max_articulos]:
        if not puede_visitar(url):
            continue
        html = descargar(url)
        if not html:
            continue
        ficha = extraer_articulo(html, url)
        if ficha and ficha["texto"]:
            ficha["fecha_consulta"] = date.today().isoformat()
            ficha["cita"] = referencia(ficha)       # paso 7
            fichas.append(ficha)
            print("OK:", ficha["titulo"])
    guardar(fichas)
    print(f"Listo: {len(fichas)} páginas guardadas en resultados.json y resultados.csv")

if __name__ == "__main__":
    main()
```

Ejecútalo con `python scraper.py`. Elimina el bloque de prueba `if __name__ == "__main__": print(puede_visitar(...))` de la parte 1 para que no se ejecute dos veces.

## Cuando algo falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Error 403 o 429 | El sitio detectó demasiadas peticiones o rechaza bots | Aumenta la espera. No intentes esquivar el bloqueo: si el sitio no quiere bots, respeta eso. |
| El texto sale vacío | La página se arma con JavaScript en el navegador | Usa Playwright para renderizarla antes de extraer. |
| Tildes y eñes raras | Codificación mal detectada | El código del paso 2 ya la corrige; verifica con `r.apparent_encoding`. |
| Trae menús mezclados | La página tiene una estructura rara | Prueba `favor_precision=True` o usa un selector CSS propio. |
| Funcionaba y dejó de funcionar | El sitio cambió su HTML | Revisa los selectores. Este es el dolor que los agentes ayudan a reducir. |
| Pide login o suscripción | Contenido de pago o privado | Detente. No se extrae. |

### Páginas que cargan con JavaScript

**terminal**

```
pip install playwright
playwright install chromium
```

**renderizar.py**

```
from playwright.sync_api import sync_playwright

def descargar_renderizado(url: str) -> str:
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto(url, wait_until="networkidle")
        html = pagina.content()
        navegador.close()
    return html
```

El HTML que devuelve se usa igual que el del paso 2: se lo pasas a `extraer_articulo`.

## Checklist y siguiente paso

- Corriste el script en un sitio de práctica y revisaste `resultados.json`.
- Entiendes por qué cada eslabón existe: permiso, descarga, estructura, extracción, mapa, guardado.
- Probaste a mano el sitemap y el crawl con límite de páginas.
- Revisaste robots.txt y los términos del sitio que quieres usar.
- Tienes claro que lo que publicas va reescrito y con la fuente citada.

>  **Lo que sigue**

En la guía 2 tomas exactamente estas funciones (`puede_visitar`, `descargar`, `extraer_articulo`, `urls_desde_sitemap`) y se las das como herramientas a un agente de IA que decide qué leer, extrae datos estructurados y escribe resúmenes propios con cita. Conserva tu archivo `scraper.py`: lo vas a importar.

[Ir a la guía 2: scraping con agentes](scraping-con-agentes.md)

---

Ejercicio práctico · 8 de octubre de 2026 · Versión 5 de la guía 1

# Ejercicio: Scraping manual

Vamos a mapear un sitio real con el navegador, sin código: **viviendoporelmundo.com**. Este ejercicio es el primer eslabón de la cadena de la guía 1 (el permiso): abrir el robots.txt, entender qué dice y decidir si se puede seguir.

>  **Sitio del ejercicio**

`https://www.viviendoporelmundo.com/`

## La ruta del ejercicio

Todo el ejercicio sigue un mismo camino de cinco etapas. Cada una produce algo que necesita la siguiente. Este es el mapa completo, para que siempre sepas en cuál estás:

1. **Permisos** Leer el robots.txt. — hecho
1. **Mapeo** Listar las páginas del dominio. — siguiente
1. **Filtrado** Elegir las páginas útiles. — pendiente
1. **Scraping** Descargar y extraer el texto. — pendiente
1. **Archivo** Guardar, reescribir y citar. — pendiente

| Etapa | Qué es | Qué obtienes | Dónde está |
|---|---|---|---|
| 1. Revisión de permisos (reconocimiento previo) | Leer qué permite y qué prohíbe el sitio, y a qué ritmo. | Luz verde o parada, lista de rutas prohibidas, espera entre páginas y dirección del mapa. | Pasos 1 al 3 de este ejercicio. Paso 1 del código de la guía 1. |
| 2. Mapeo del dominio (descubrimiento de URLs) | Conseguir la lista de páginas que existen, sin leer su contenido. | Un listado de direcciones del sitio y cuántas son. | Paso 4 de este ejercicio. Paso 5 (5A y 5B) de la guía 1. |
| 3. Filtrado | Quedarte solo con las páginas que sirven, por ejemplo los artículos. | Una lista corta y priorizada. | Paso 5C de la guía 1. En la guía 2, lo hace un agente. |
| 4. Scraping (extracción) | Descargar cada página elegida y sacar su texto y datos. | Título, autor, fecha y texto limpio de cada artículo. | Pasos 2 al 4 de la guía 1. |
| 5. Almacenamiento y reescritura | Guardar con fuente y fecha, y redactar con tus palabras. | Fichas listas para usar, con la fuente citada. | Pasos 6 y 7 de la guía 1. |

>  **Los nombres, para no confundirse**

El proceso completo se llama **scraping web** o **web crawling**. Estrictamente, *crawling* es recorrer el sitio para descubrir páginas (etapa 2) y *scraping* es extraer los datos de cada una (etapa 4). En la práctica se usan casi como sinónimos. Ahora mismo estamos cerrando la etapa 1; mapear el dominio empieza en cuanto abras el sitemap.

## 1. Abrir el robots.txt en el navegador

El robots.txt siempre vive en el mismo lugar: la raíz del dominio, con el nombre exacto `robots.txt`. No hay que buscarlo; se escribe la dirección completa en la barra del navegador.

`https://www.viviendoporelmundo.com/robots.txt` — protocolo (`https://`, cómo se conecta) + dominio (`www.viviendoporelmundo.com`, dónde está el sitio) + ruta del archivo (`/robots.txt`).

- Abre una pestaña nueva en Chrome.
- Pega `https://www.viviendoporelmundo.com/robots.txt` y pulsa Enter.
- Si todo va bien, verás una página de texto plano, sin diseño, con líneas cortas.

>  **Por qué empezamos aquí**

Antes de mapear o leer una sola página hay que saber si el sitio lo permite. Es el mismo orden de la guía 1: primero permiso, después descarga.

## Si Chrome dice "This site can't be reached"

Es el error más común al empezar, y casi siempre es un detalle de escritura. Por ejemplo, si escribes la dirección sin la terminación del dominio:

**Dirección mal escrita**

```
viviendoporelmundo/robots.txt
```

| Qué dice el error | Qué significa |
|---|---|
| `This site can't be reached` | Chrome no pudo llegar a ningún servidor con esa dirección. |
| `Check if there is a typo in…` | Sugiere revisar cómo escribiste el dominio. |
| `DNS_PROBE_FINISHED_NXDOMAIN` | El dominio no existe. NX significa "no existe" y DNS es la "libreta de direcciones" de internet. |

>  **La causa y la solución**

Un dominio necesita su terminación (`.com`, `.co`, `.ai`…). `viviendoporelmundo` a secas no es un dominio; `viviendoporelmundo.com` sí. Copia y pega la dirección completa del paso 1 en vez de escribirla a mano.

Un **error 404** es distinto: significa que el sitio existe pero no tiene robots.txt. Eso no prohíbe nada, pero obliga a revisar los términos de uso del sitio.

## 2. Qué buscar: los 4 tipos de líneas

Un robots.txt se compone de solo cuatro tipos de líneas. Aprender a reconocerlas es el 90% de la lectura.

| Línea | Qué dice | Ejemplo |
|---|---|---|
| `User-agent:` | A qué bot se aplican las reglas que van debajo. `*` significa todos. | `User-agent: *` |
| `Disallow:` | Rutas prohibidas. Todo lo que cuelga de esa ruta también. | `Disallow: /wp-admin/` |
| `Allow:` | Permitido. Se usa como regla general o como excepción dentro de una ruta prohibida. | `Allow: /` |
| `Sitemap:` | La dirección del mapa del sitio. Es la que más nos importa. | `Sitemap: http://viviendoporelmundo.com/sitemap_index.xml` |

>  **Una regla que detiene todo**

Si encuentras `Disallow: /` a secas bajo `User-agent: *`, todo el sitio está prohibido para los bots y el ejercicio termina ahí. Con `Disallow:` vacío o con `Allow: /`, el sitio está abierto.

## Qué es un User-agent y qué tipos de bots existen

El **User-agent** es el nombre con el que un programa se presenta ante un sitio web. Cuando abres una página con Chrome, Chrome se presenta como navegador. Cuando Google rastrea el sitio, se presenta como `Googlebot`. Tu scraper también se presenta con un nombre: el `USER_AGENT` que definimos en el paso 1 del código de la guía 1. El robots.txt lee ese nombre y decide qué reglas le tocan.

| Tipo de bot | Nombres típicos | Qué hacen |
|---|---|---|
| Buscadores | `Googlebot`, `Bingbot` | Recorren sitios para que aparezcan en los resultados de búsqueda. |
| Rastreadores de IA | `GPTBot`, `ClaudeBot`, `CCBot` | Recogen texto para entrenar o alimentar modelos de IA. |
| Redes sociales | `facebookexternalhit`, `Twitterbot` | Leen la página para armar la vista previa cuando alguien comparte un enlace. |
| Herramientas SEO | `AhrefsBot`, `SemrushBot` | Analizan sitios para estudios de posicionamiento. |
| Scrapers propios | El nombre que tú inventes | Lo que tú programes, por ejemplo `MiBotInvestigacion`. |

### Cómo se ve un robots.txt con varios bloques

Este es un ejemplo genérico, solo para aprender a leer. No es el de ningún sitio real:

**Ejemplo genérico**

```
User-agent: Googlebot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: *
Disallow: /admin
```

Se lee así: Google puede entrar a todo. GPTBot tiene prohibido todo el sitio. Cualquier otro bot (el asterisco) solo tiene prohibido `/admin`.

>  **Qué regla te aplica a ti**

Un bot lee el bloque que lleva su propio nombre y, si no hay ninguno, usa el bloque `User-agent: *`. Como tu scraper tiene un nombre propio que casi ningún sitio menciona, normalmente te aplica el bloque `*`. Si el sitio tuviera un bloque con tu nombre exacto, ese sería el que manda.

## 3. Leer el robots.txt de viviendoporelmundo.com

Esto fue lo que apareció al abrir `viviendoporelmundo.com/robots.txt`. Con o sin `www` suele cargar lo mismo; tú abriste la versión sin `www`.

**robots.txt de viviendoporelmundo.com (8 de octubre de 2026)**

```
User-agent: *
Disallow: /cgi-bin/
Disallow: /wp-admin/
Disallow: /wp-includes/
Crawl-delay: 10

Disallow: /xmlrpc.php
Disallow: /readme.html
Allow: /wp-content/uploads/
Disallow: /wp-content/plugins/

Sitemap: http://viviendoporelmundo.com/sitemap_index.xml

User-Agent: Googlebot
Allow: .js
Allow: .css
```

### Cómo está organizado

El archivo tiene **dos bloques** y una línea suelta. Un bloque es un `User-agent:` seguido de sus reglas; la línea en blanco o un nuevo `User-agent:` marca dónde cambia de destinatario.

| Parte | Para quién es |
|---|---|
| Bloque 1: `User-agent: *` y todas sus reglas | Todos los bots. Incluye al tuyo. |
| Línea `Sitemap:` | Para cualquiera. No pertenece a ningún bloque: es un aviso general. |
| Bloque 2: `User-Agent: Googlebot` | Solo el bot de Google. |

### Bloque 1: las reglas para todos los bots

Piensa en el robots.txt como los carteles en la puerta de un edificio. Este bloque es el cartel de "visitantes en general".

| Línea | Qué significa | Para entender la lógica |
|---|---|---|
| `User-agent: *` | Las reglas de abajo aplican a cualquier bot. | El cartel dice "para todo visitante". |
| `Disallow: /cgi-bin/` | Carpeta técnica del servidor, con programas internos. No tiene artículos. | La sala de máquinas del edificio: no es para visitas. |
| `Disallow: /wp-admin/` | Panel de administración de WordPress, donde el dueño entra con su contraseña a publicar. | La oficina del administrador. La dirección `viviendoporelmundo.com/wp-admin/` no se visita. |
| `Disallow: /wp-includes/` | Archivos internos de WordPress. Es código, no contenido. | Los cables y tuberías detrás de la pared. |
| `Crawl-delay: 10` | Pide esperar 10 segundos entre una petición y la siguiente. | "Toca el timbre una vez cada 10 segundos, no diez veces seguidas." Con 50 páginas son unos 8 minutos; con 500, cerca de 1 hora 23 minutos; con 5.000, unas 14 horas. |
| `Disallow: /xmlrpc.php` | Puerta técnica antigua de WordPress para controlarlo a distancia. Los sitios la cierran porque suele ser blanco de ataques. | Una puerta trasera que prefieren mantener cerrada para todos. |
| `Disallow: /readme.html` | Archivo de instalación de WordPress. No tiene contenido útil y suele mostrar la versión instalada. | El manual de instrucciones que viene en la caja: no es parte de lo que se exhibe. |
| `Allow: /wp-content/uploads/` | Carpeta donde WordPress guarda las fotos y archivos que se suben a los artículos. Está permitida de forma explícita. | Una foto de un viaje quedaría en una dirección parecida a `…/wp-content/uploads/2025/03/foto.jpg`. Es un ejemplo, no una dirección real. |
| `Disallow: /wp-content/plugins/` | Carpeta de los plugins (extensiones) instalados. Es código, no contenido. | Las herramientas del taller, no lo que se vende. |

### La línea Sitemap

| Línea | Qué significa |
|---|---|
| `Sitemap: http://viviendoporelmundo.com/sitemap_index.xml` | La dirección del mapa del sitio. Dos detalles: empieza con `http://` y no `https://` (el navegador normalmente te redirige solo), y se llama `sitemap_index`, o sea que es un **índice** que apunta a varios mapas más pequeños, no una lista directa de páginas. |

### Bloque 2: las reglas solo para Googlebot

| Línea | Qué significa |
|---|---|
| `User-Agent: Googlebot` | Lo que sigue es solo para el bot de Google. |
| `Allow: .js` y `Allow: .css` | Le permite cargar los archivos de scripts (`.js`) y de estilos (`.css`). Así Google ve la página con su diseño completo, como lo vería una persona en el navegador. |

>  **La lógica de tener un bloque aparte**

Un bot que encuentra un bloque con su propio nombre lee solo ese y deja de lado el bloque `*`. Googlebot tiene el suyo, así que sigue sus reglas y no las del bloque 1. Tu bot (`MiBotInvestigacion`) no aparece por nombre, así que te aplica el bloque 1 completo: las seis rutas prohibidas y la espera de 10 segundos.

## Cómo lo leería el código de la guía 1

No tienes que interpretar el archivo a mano cada vez: Python trae un lector de robots.txt (el mismo del paso 1 del código). Con tres líneas le preguntas si puedes visitar una ruta, cuánto esperar y dónde está el mapa:

**probar_robots.py**

```
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://viviendoporelmundo.com/robots.txt")
rp.read()

bot = "MiBotInvestigacion/1.0"
print(rp.can_fetch(bot, "https://viviendoporelmundo.com/wp-admin/"))   # ¿puedo visitar esta ruta?
print(rp.crawl_delay(bot))                                              # ¿cuántos segundos esperar?
print(rp.site_maps())                                                   # ¿dónde está el mapa?
```

Lo probé con el texto exacto de tu captura (Python 3.13; `site_maps()` requiere Python 3.8 o superior). Estos fueron los resultados:

| Pregunta | Respuesta |
|---|---|
| ¿Puedo visitar la portada `/`? | `True` |
| ¿Puedo visitar un artículo, por ejemplo `/un-articulo/`? | `True` |
| ¿Puedo visitar `/wp-content/uploads/foto.jpg`? | `True` |
| ¿Puedo visitar `/wp-admin/`? | `False` |
| ¿Puedo visitar `/wp-includes/…`? | `False` |
| ¿Puedo visitar `/xmlrpc.php` o `/readme.html`? | `False` |
| ¿Puedo visitar `/wp-content/plugins/…`? | `False` |
| ¿Cuánto esperar entre peticiones? | `10` segundos |
| ¿Dónde está el mapa? | `http://viviendoporelmundo.com/sitemap_index.xml` |

### Un ajuste que sí cambia el código

En el paso 2 de la guía 1, la función `descargar` espera 2 segundos por defecto. Este sitio pide 10. En vez de cambiar el número a mano en cada sitio, puedes pedirle el dato al robots.txt:

**scraper.py (función nueva)**

```
def espera_del_sitio(url: str, por_defecto: float = 2.0) -> float:
    """Lee el Crawl-delay del robots.txt; si el sitio no lo indica, usa el valor por defecto."""
    p = urlparse(url)
    retraso = _robots(f"{p.scheme}://{p.netloc}").crawl_delay(USER_AGENT)
    return float(retraso) if retraso else por_defecto

# Y dentro de descargar(), en lugar de time.sleep(espera):
#     time.sleep(espera_del_sitio(url))
```

## Qué obtienes de esta información, para qué sirve y a dónde lleva

El robots.txt no te da contenido. Te da **permisos, límites y pistas**. Esto es lo que sacamos de este archivo en concreto:

| Lo que descubriste | Qué obtienes | Para qué sirve |
|---|---|---|
| No hay `Disallow: /` para el bloque `*` | Permiso general: el contenido público (artículos y páginas) no está prohibido. | Es la luz verde para seguir con el mapeo. |
| Seis rutas prohibidas | Una lista de exclusión: `/cgi-bin/`, `/wp-admin/`, `/wp-includes/`, `/xmlrpc.php`, `/readme.html`, `/wp-content/plugins/`. | Tu código las evita solo con `puede_visitar()`. Además no pierdes tiempo en zonas que no tienen artículos. |
| `Crawl-delay: 10` | Tu ritmo de trabajo: una página cada 10 segundos. | Sirve para calcular cuánto tardará el trabajo antes de empezarlo y para configurar la espera del código. |
| Rutas que empiezan con `wp-` | Una pista fuerte de que el sitio está hecho con WordPress. Es una deducción, no un dato confirmado. | Sabes qué esperar: WordPress suele tener un sitemap en forma de índice, con mapas separados para artículos, páginas y categorías. |
| `Allow: /wp-content/uploads/` | Saber dónde viven las fotos del sitio. | Solo es un dato de ubicación. Que el robots.txt lo permita no significa que puedas reutilizar las fotos: tienen derechos de autor. |
| `Sitemap: …/sitemap_index.xml` | La dirección del mapa del dominio. | Es el siguiente archivo que abrimos. |
| Bloque aparte para Googlebot | Un ejemplo real de que un sitio puede tratar distinto a cada bot. | Te enseña a leer siempre qué bloque te toca a ti. |

>  **Lo que este archivo no te dice**

No dice nada sobre derechos de autor ni sobre los términos de uso del sitio, que pueden ser más estrictos que el robots.txt. Tampoco es un candado: es una petición de cortesía que nosotros respetamos siempre. Por eso, antes de extraer contenido, se leen los términos de uso, y no se extrae nada detrás de login o paywall.

### A dónde te lleva

Cada dato abre el paso siguiente. Este es el camino que sigue desde aquí:

1. **robots.txt** Permiso, límites y ritmo. — hecho
1. **sitemap_index.xml** Lista de mapas hijos. — siguiente
1. **Mapas hijos** Entradas, páginas, categorías. — navegador
1. **Lista de URLs** Todas las páginas del sitio. — navegador
1. **Filtro** Quedarte con los artículos útiles. — tú o código
1. **Lectura** Descargar cada una, esperando 10 s. — código
1. **Fichas** Texto, fuente y fecha de consulta. — código

Este mismo recorrido es el que, en la guía 2, se le entrega a un agente de IA: el robots.txt le marca los límites y él decide qué páginas leer.

## 4. Siguiente paso: abrir el sitemap

- Abre en una pestaña nueva `http://viviendoporelmundo.com/sitemap_index.xml`, la dirección de la línea `Sitemap:`. Si el navegador te redirige a `https` o a `www`, es normal.
- Como se llama `sitemap_index`, espera un índice con etiquetas `<sitemap>` que apuntan a otros mapas, por ejemplo uno de entradas, otro de páginas y otro de categorías. Ábrelos uno por uno; los nombres exactos los confirmamos al verlos.
- Cuenta cuántas páginas hay y copia las primeras 10 direcciones.

Esa lista es el mapa del dominio. Después viene decidir cuáles páginas vale la pena leer. Si el sitio no tuviera sitemap, se mapea siguiendo los enlaces desde la portada (`rastrear()`, paso 5B de la guía 1).

## Registro del ejercicio: viviendoporelmundo.com

Resumen de lo que encontramos al abrir el robots.txt. Todas las filas están resueltas salvo la de términos de uso, que queda pendiente.

| Qué revisar | Lo que encontré |
|---|---|
| Fecha de la revisión | 8 de octubre de 2026 |
| Dirección abierta | `https://www.viviendoporelmundo.com/robots.txt` |
| ¿Cargó o dio error? (404, DNS…) | Cargó bien: texto plano, sin error. |
| Número de bloques `User-agent:` | 2: `*` y `Googlebot`. |
| Reglas del bloque `*` (`Disallow` / `Allow`) | Prohibidas: `/cgi-bin/`, `/wp-admin/`, `/wp-includes/`, `/xmlrpc.php`, `/readme.html`, `/wp-content/plugins/`. Permitida: `/wp-content/uploads/`. Espera: `Crawl-delay: 10`. |
| Línea `Sitemap:` | `http://viviendoporelmundo.com/sitemap_index.xml` |
| ¿Hay `Disallow: /` a secas? | No. |
| Términos de uso revisados | **Pendiente:** abrir y leer los términos del sitio. |
| Decisión: ¿seguimos con el mapeo? | Sí. El robots.txt lo permite, con 10 segundos de espera entre páginas. Falta revisar los términos de uso antes de extraer contenido. |

## Versiones de este archivo

| Versión | Fecha | Archivo | Qué contiene |
|---|---|---|---|
| v1 | 8 de octubre de 2026 | `scraping-manual_2026-10-08.html` | Guía de 7 pasos con código en Python. |
| v2 | 8 de octubre de 2026 | `scraping-manual_2026-10-08_v2.html` | Guía más ejercicio, con ejemplos de otro dominio. Reemplazada por la v3. |
| v3 | 8 de octubre de 2026 | `scraping-manual_2026-10-08_v3.html` | Guía más ejercicio centrado solo en viviendoporelmundo.com. Reemplazada por la v4. |
| v4 | 8 de octubre de 2026 | `scraping-manual_2026-10-08_v4.html` | Agrega la lectura real del robots.txt de viviendoporelmundo.com: explicación línea por línea, cómo lo lee el código, qué se obtiene y registro completado. Reemplazada por la v5. |
| v5 | 8 de octubre de 2026 | `scraping-manual_2026-10-08_v5.html` | Agrega al inicio del ejercicio la ruta de cinco etapas (permisos, mapeo, filtrado, scraping, archivo) con el estado de cada una. |

Cada vez que avancemos (sitemap, filtrado de páginas, primera extracción) se agrega una sección nueva aquí y se guarda una versión nueva con la fecha en el nombre.

Guía 1 de 2, scraping manual. Elaborada el 8 de octubre de 2026. Las librerías cambian de versión con frecuencia: si algún comando falla, revisa la documentación oficial de cada una.
