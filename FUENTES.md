# Fuentes

Una ficha por sitio. Antes de mapear o descargar de un sitio, leer su ficha; si no existe, crearla primero (empezando por el robots.txt). Cada ficha lleva la fecha de su última revisión: el robots.txt y el HTML de un sitio cambian.

## Plantilla de ficha

```
## <dominio>
- Última revisión:
- URL base:
- Método: sitemap | rastreo | API
- robots.txt: permitido / prohibido, rutas prohibidas, Crawl-delay
- Sitemap:
- Términos de uso: revisados (fecha y resumen) | pendiente
- Campos que se extraen:
- Trampas conocidas:
- Estado del ejercicio:
```

---

## viviendoporelmundo.com

- **Última revisión:** 9 de octubre de 2026 (robots.txt, abierto con `www`: idéntico al del 8 de octubre).
- **URL base:** `https://www.viviendoporelmundo.com/`
- **Método:** sitemap. Si fallara, rastreo desde la portada (`rastrear()`, paso 5B de la guía 1).
- **Términos de uso:** **revisados el 9 oct 2026.** El aviso legal no prohíbe expresamente bots, scraping ni reproducción, pero la cláusula 1.7 anuncia acciones civiles y penales contra «cualquier utilización indebida». La numeración de la propia página salta de la 1.3 a la 1.4.2 (faltan la 1.4 y la 1.4.1; no sabemos qué decían). Que no prohíba no equivale a autorizar: rigen los derechos de autor por defecto. Titular: persona natural; el sitio se financia con afiliación y publicidad; rige la ley española. No se guardan los datos personales del titular.
- **Condiciones de uso para este proyecto:** muestra mínima (3 páginas), 10 s de espera, sin fotos ni enlaces de afiliado, texto reescrito con palabras propias y citas de máximo 15 palabras con enlace. Opcional: pedir permiso por el correo de contacto del aviso.
- **Campos que se extraen:** los de la ficha mínima del CLAUDE.md (`url`, `titulo`, `autor`, `fecha_publicacion`, `sitio`, `fecha_consulta`, `cita`) y el texto del artículo.

### robots.txt

A nuestro bot le aplica el bloque `User-agent: *`.

| Regla | Valor |
|---|---|
| ¿`Disallow: /` a secas? | No: el contenido público está permitido. |
| Rutas prohibidas | `/cgi-bin/`, `/wp-admin/`, `/wp-includes/`, `/xmlrpc.php`, `/readme.html`, `/wp-content/plugins/` |
| Permitida explícitamente | `/wp-content/uploads/` (fotos: permitido acceder, **no** reutilizar; tienen derechos de autor) |
| `Crawl-delay` | 10 s entre peticiones |
| Sitemap | `http://viviendoporelmundo.com/sitemap_index.xml` |
| Otros bloques | `User-Agent: Googlebot` (`Allow: .js`, `Allow: .css`); no nos aplica. |

### Trampas conocidas

- **Tiempo:** con 10 s por página, 50 páginas ≈ 8 min; 500 ≈ 1 h 23 min; 5.000 ≈ 14 h. Calcular antes de lanzar.
- **El sitemap está en `http://` y sin `www`;** el navegador redirige. Es un **índice** (`sitemap_index.xml`) que apunta a mapas hijos, no una lista directa de páginas.
- **Es WordPress** (confirmado el 9 oct 2026): el sitemap lo genera el plugin Yoast SEO.
- **El `sitemap_index.xml` solo tiene 2 mapas hijos:** `post-sitemap.xml` (entradas) y `page-sitemap.xml` (páginas), en `https://www.…`, ambos con última modificación el 2026-06-20. No hay mapa de categorías ni de etiquetas: el sitemap no es el plano completo del sitio, hay que compararlo con lo que se descubre siguiendo enlaces.
- **El índice se anuncia en `http://` sin `www` pero los hijos están en `https://www`:** hay una redirección que el código debe seguir.
- **Pedir `http://viviendoporelmundo.com/` provoca un 301 a `https://www.viviendoporelmundo.com/`** (verificado el 9 oct 2026): una página son dos peticiones y el código las hace seguidas. Pedir ya la dirección final, `https://www…`. La portada responde 200, `text/html; charset=UTF-8`, unos 240 KB de HTML y 1,86 s.
- **`post-sitemap.xml` tiene 244 URLs** (según su encabezado, 9 oct 2026; se recontarán con código), de 2015-10-26 a 2026-06-20, ordenadas por fecha de modificación, con una columna de número de imágenes. `page-sitemap.xml`: sin contar todavía.
- **Ninguna URL tiene carpeta** (`/blog/`, `/pais/`): todas cuelgan de la raíz. Las reglas por defecto de la guía 1 (`PATRONES_UTILES`) descartarían todas; el filtrado tendrá que usar otras pistas (el nombre de la página).
- **`Last Mod.` no es la fecha de publicación:** hay bloques con la misma fecha de edición (más de 50 entradas del 21 al 26 de julio de 2021; 9 del 20 de junio de 2026).
- **Familias de contenido por el nombre:** guías de lugares, vídeos, podcasts y entrevistas, contenido comercial o de afiliación (seguros, hosting, cursos) y posibles duplicados que terminan en `-2`.
- **`descargar()` de la guía 1 espera 2 s por defecto:** en este sitio es poco; usar `espera_del_sitio()`.
- **El robots.txt tiene una línea en blanco tras `Crawl-delay: 10`.** El lector de Python (`urllib.robotparser`) la toma como fin de bloque y descarta las reglas siguientes: `/xmlrpc.php`, `/readme.html` y `/wp-content/plugins/` salían como permitidas. Corregido en `scraper.py` con `_normalizar` (verificado el 9 oct 2026).

### Estado del ejercicio

| Etapa | Estado |
|---|---|
| 1. Permisos (robots.txt y términos) | Hecho (9 oct 2026): robots.txt verificado y leído con código; términos revisados |
| 2. Mapeo (sitemap) | En curso: índice y `post-sitemap.xml` vistos en el navegador (paso 4) y portada descargada con código (paso 5); sigue la lectura de los mapas hijos con código (paso 6) |
| 3. Filtrado | Pendiente |
| 4. Scraping (extracción) | Pendiente |
| 5. Archivo, reescritura y cita | Pendiente |
