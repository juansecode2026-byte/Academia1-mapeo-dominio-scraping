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

- **Última revisión:** 8 de octubre de 2026 (robots.txt).
- **URL base:** `https://www.viviendoporelmundo.com/`
- **Método:** sitemap. Si fallara, rastreo desde la portada (`rastrear()`, paso 5B de la guía 1).
- **Términos de uso:** **pendiente.** No se extrae contenido hasta revisarlos.
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
- **Parece WordPress** (rutas `wp-`). Es una deducción, no un dato confirmado. Si se confirma, esperar mapas hijos separados para entradas, páginas y categorías.
- **`descargar()` de la guía 1 espera 2 s por defecto:** en este sitio es poco; usar `espera_del_sitio()`.

### Estado del ejercicio

| Etapa | Estado |
|---|---|
| 1. Permisos (robots.txt) | Hecho (8 oct 2026) |
| 2. Mapeo (sitemap) | Siguiente |
| 3. Filtrado | Pendiente |
| 4. Scraping (extracción) | Pendiente |
| 5. Archivo, reescritura y cita | Pendiente |
